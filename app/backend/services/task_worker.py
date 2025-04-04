from playwright.sync_api import sync_playwright
import json
import uuid
import logging
from datetime import date
from services.redis_config import store_result, store_task_status
from services.test_odd_calendar_scraper import navigate_odd_calendar
from services.test_even_calendar_scraper import navigate_even_calendar
from services.test_timetable_scraper import navigate_to_timetable, scrape_table_data, get_batch_number
from services.test_unified_timetable import navigate_batch1, navigate_batch2, scrape_batch1_data, scrape_batch2_data
from services.utils import get_current_date, process_calendar_data



logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("task_worker")


def get_user_name(email):
    email_parts = email.split("@")
    return email_parts[0]


def format_date(day_number):
    current_year, current_month, _ = get_current_date()
    return f"{current_year}-{current_month}-{str(day_number).zfill(2)}"


def perform_login(page, email, password):
    try:
        logger.info(f"{email} is logging in...")
        page.goto("https://academia.srmist.edu.in/#CIRCULAR")
        
        page.wait_for_selector("iframe[name=\"zohoiam\"]")
        iframe = page.frame(name="zohoiam")

        try:
            iframe.locator("input[placeholder='Email Address']").fill(email)
        except Exception:
            iframe.get_by_placeholder("Email Address", exact=True).fill(email)

        try:
            iframe.locator("button:has-text('Next')").nth(0).click()
        except Exception:
            iframe.get_by_role("button", name="Next").click()

        iframe.get_by_placeholder("Enter Password").wait_for(state="visible", timeout=5000)

        page.locator("iframe[name=\"zohoiam\"]").content_frame.get_by_placeholder("Enter Password").click()
        iframe.get_by_placeholder("Enter Password").fill(password)

        try:
            iframe.locator("button:has-text('Sign In')").click()
        except Exception:
            iframe.get_by_role("button", name="Sign In").click()

        page.get_by_role("link", name="Academic Reports").wait_for(state="visible")
        page.get_by_role("link", name="Academic Reports").click()
        
        return True
    except Exception as e:
        logger.error(f"Login process failed: {str(e)}")
        return False


def map_weekly_schedule(timetable_data, batch_data, weekly_data):
    slot_to_details = {row[1]: {"course": row[0], "room": row[2]} for row in timetable_data[1:]}
    time_slots = batch_data[0][1:]
    weekly_schedule = []

    for entry in weekly_data:
        if not isinstance(entry, list) or len(entry) != 3:
            logging.error(f"Invalid entry in weekly_data: {entry}")
            continue  

        day_number, day_name, day_order = entry  
        date = format_date(day_number)

        if day_order == 0:
            weekly_schedule.append([date, day_name, []])
            continue

        if day_order + 2 >= len(batch_data):  
            logging.error(f"Day order {day_order} out of bounds for batch_data")
            weekly_schedule.append([date, day_name, []])
            continue

        current_day_order_data = batch_data[day_order + 2]
        course_details = []

        for i in range(1, len(current_day_order_data)):
            slot = current_day_order_data[i].split('/')[0].strip()

            if slot not in slot_to_details:
                continue

            updated_time_slot = time_slots[i-1].replace('\t', '')

            try:
                start_time, end_time = map(str.strip, updated_time_slot.split('-'))
                course_info = [
                    slot_to_details[slot]["course"],
                    start_time,
                    end_time,
                    slot_to_details[slot]["room"]
                ]
                course_details.append(course_info)
            except ValueError as e:
                logging.error(f"Time slot error: {updated_time_slot}, {e}")
                continue

        weekly_schedule.append([date, day_name, course_details])

    return weekly_schedule


def process_login_task(task_id, email, password):
    logger.info(f"Processing task {task_id} for {email}")
    store_task_status(task_id, "processing", "Login in progress")
    
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-gpu",
            "--disable-dev-shm-usage",  
            "--no-sandbox",  
            "--disable-setuid-sandbox"
        ])
        context = browser.new_context()
        context.route("**/*.{png,jpg,jpeg,svg,gif,woff,woff2,ttf}", lambda route: route.abort())
        page = context.new_page()
        
        try:
            logger.info(f"Performing fresh login for {email}...")
            if not perform_login(page, email, password):
                store_task_status(task_id, "failed", "Login failed")
                logger.error(f"Login failed for {email}")
                return 
            
            store_task_status(task_id, "processing", "Scraping academic calendar")
            page.get_by_role("link", name="Academic Reports").wait_for(state="visible")
            page.get_by_role("link", name="Academic Reports").click()
            

            try: 
                navigate_even_calendar(page)
                weekly_data = process_calendar_data(page)
            except Exception as e:
                store_task_status(task_id, "failed", f"Error in calendar scraping: {str(e)}")
                logger.error(f"Error in even calendar scraping: {e}")
                return
            
            store_task_status(task_id, "processing", "Scraping timetable")
            page.get_by_role("link", name="Academic Reports").click()
            

            try:
                navigate_to_timetable(page)
                timetable_data = scrape_table_data(page)
            except Exception as e:
                store_task_status(task_id, "failed", f"Error in timetable scraping: {str(e)}")
                logger.error(f"Error in timetable scraping: {e}")
                return

            try:
                batch_number = get_batch_number(page)
                page.get_by_role("link", name="Academic Reports").click()
            except Exception as e:
                store_task_status(task_id, "failed", f"Error getting batch number: {str(e)}")
                logger.error(f"Error in getting batch number: {e}")
                return

            store_task_status(task_id, "processing", f"Processing batch {batch_number} data")

            if batch_number == 1:
                try:
                    navigate_batch1(page)
                    page.wait_for_selector("table[align='center']")
                    batch_data = scrape_batch1_data(page)
                except Exception as e:
                    store_task_status(task_id, "failed", f"Error in batch 1 processing: {str(e)}")
                    logger.error(f"Error in batch 1 processing: {str(e)}")
                    return
                
            elif batch_number == 2: 
                try:
                    navigate_batch2(page)
                    page.wait_for_selector("table[align='center']")
                    batch_data = scrape_batch2_data(page)
                except Exception as e:
                    store_task_status(task_id, "failed", f"Error in batch 2 processing: {str(e)}")
                    logger.error(f"Error in batch 2 processing: {str(e)}")
                    return
            else:
                store_task_status(task_id, "failed", f"Invalid batch number: {batch_number}")
                logger.error(f"Invalid batch number: {batch_number}")
                return
            
            try:
                weekly_schedule = map_weekly_schedule(timetable_data, batch_data, weekly_data)
            except Exception as e:
                store_task_status(task_id, "failed", f"Error mapping weekly schedule: {str(e)}")
                logger.error(f"Error in mapping weekly schedule: {str(e)}")
                return
            
            
            user_name = get_user_name(email)
            try:
                page.get_by_role("button", name=f"profile image {user_name}").click()
                page.locator("div").filter(has_text=f"{user_name} {email}").nth(3).wait_for(state="visible")
                page.locator('#portalLogout').click()
                page.wait_for_timeout(1000)
            except Exception as e:
                logger.warning(f"Logout process failed: {str(e)}")

            output_data = {
                "weekly_schedule": weekly_schedule,
                "email": email
            }
            

            store_result(task_id, json.dumps(output_data).encode('utf-8'))
            store_task_status(task_id, "completed", "Data scraping completed successfully")
            logger.info(f"Task {task_id} completed successfully for {email}")
            return True

        except Exception as e:
            store_task_status(task_id, "failed", f"Task failed: {str(e)}")
            logger.error(f"Task {task_id} failed for {email}: {str(e)}")
            return False
        finally:
            try:
                browser.close()
            except Exception as e:
                logger.error(f"Error closing browser: {str(e)}")



def login_and_scrape(email, password):
    task_id = str(uuid.uuid4())
    try:
        return process_login_task(task_id, email, password)
    
    except Exception as e:
        logger.error(f"unhandled error: {str(e)}")
        store_task_status(task_id, "failed", f"unhandled exception: {str(e)}")

        return False