from playwright.sync_api import Playwright, sync_playwright
import sys
import json
from bs4 import BeautifulSoup
from test_odd_calendar_scraper import navigate_odd_calendar
from test_even_calendar_scraper import navigate_even_calendar
from test_timetable_scraper import navigate_to_timetable, scrape_table_data, get_batch_number
from test_unified_timetable import navigate_batch1, navigate_batch2, scrape_batch1_data, scrape_batch2_data
from datetime import date
from utils import get_current_date, process_calendar_data
import logging


def get_user_name(email):
    email_parts = email.split("@")
    return email_parts[0]

def format_date(day_number):
    current_year, current_month, _ = get_current_date()
    return f"{current_year}-{current_month}-{str(day_number).zfill(2)}"

def perform_login(page, email, password):
    """Handles login process"""
    try:
        print(email , " logging in")
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

        page.get_by_role("link", name="Academic Reports").wait_for(state="visible", timeout=10000)
        page.get_by_role("link", name="Academic Reports").click()
        
        return True
    except Exception as e:
        print(f"Login process failed: {str(e)}")
        return False

def login_and_scrape(playwright: Playwright, email: str, password: str):
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
        print("Performing fresh login...")
        if not perform_login(page, email, password):
            print(f"Login failed for {email}")
            return False
        
        page.get_by_role("link", name="Academic Reports").wait_for(state="visible")
        page.get_by_role("link", name="Academic Reports").click()
        print("Clicked on 'Academic Reports'")
        
        try : 
            navigate_even_calendar(page)
            weekly_data = process_calendar_data(page)
        except Exception as e:
            print(f"Error in even calendar scraping: {e}")
            return False
        
        page.get_by_role("link", name="Academic Reports").click()
        
        try :
            navigate_to_timetable(page)
            timetable_data = scrape_table_data(page)
        except Exception as e:
            print(f"Error in timetable scraping: {e}")
            return False

        try:
            batch_number = get_batch_number(page)
            page.get_by_role("link", name="Academic Reports").click()
        except Exception as e:
            print(f"Error in getting batch number: {e}")

        if batch_number == 1:
            try:
                navigate_batch1(page)
            except Exception as e:
                print(f"Error in navigate_batch1: {str(e)}")
                return False

            try:
                page.wait_for_selector("table[align='center']")
            except Exception as e:
                print(f"Error in page.wait_for_selector: {str(e)}")
                return False
            
            batch_data = scrape_batch1_data(page)
        elif batch_number == 2: 
            try:
                navigate_batch2(page)
            except Exception as e:
                print(f"Error in navigate_batch2: {str(e)}")
                return False
            
            try:
                page.wait_for_selector("table[align='center']")
            except Exception as e:
                print(f"Error in page.wait_for_selector: {str(e)}")
                return False
            
            batch_data = scrape_batch2_data(page)
        else:
            logging.error(f"Invalid batch number: {batch_number}")
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

        try:
            weekly_schedule = map_weekly_schedule(timetable_data, batch_data, weekly_data)
        except Exception as e:
            print(f"Error in mapping weekly schedule: {str(e)}")
            return False
        
        user_name = get_user_name(email)
        page.get_by_role("button", name=f"profile image {user_name}").click()
        page.locator("div").filter(has_text=f"{user_name} {email}").nth(3).wait_for(state="visible")
        page.locator('#portalLogout').click()
        page.wait_for_timeout(1000)

        print("SUCCESS")
        print(json.dumps(weekly_schedule))
        return True

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False
    finally:
        if 'browser' in locals():
            browser.close()

def main():
    if len(sys.argv) != 3:
        print("ERROR: Email and password required")
        sys.exit(1)
        
    email = sys.argv[1]
    password = sys.argv[2]
    
    with sync_playwright() as playwright:
        if login_and_scrape(playwright, email, password):
            sys.exit(0)
        else:
            sys.exit(1)

if __name__ == "__main__":
    main()
