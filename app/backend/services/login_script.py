from playwright.sync_api import Playwright, sync_playwright
import sys
import json
from bs4 import BeautifulSoup
from test_odd_calendar_scraper import june,july,august,september,october,november,december, navigate_odd_calendar
from test_even_calendar_scraper import january,february,march,april,may , navigate_even_calendar
from test_timetable_scraper import navigate_to_timetable,scrape_table_data , get_batch_number
from test_unified_timetable import navigate_batch1,navigate_batch2,scrape_batch1_data,scrape_batch2_data
from datetime import date
from utils import get_current_date
from utils import process_calendar_data
import logging

logging.basicConfig(level=logging.DEBUG)


def format_date(day_number):
    current_year, current_month, _ = get_current_date()
    return f"{current_year}-{current_month}-{str(day_number).zfill(2)}"


def login_and_scrape(playwright: Playwright, email: str, password: str):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    try:
        print("trying to go to academia")
        page.goto("https://academia.srmist.edu.in/#CIRCULAR")
         
        iframe = page.frame(name="zohoiam")
    
        page.locator("iframe[name=\"zohoiam\"]").content_frame.get_by_placeholder("Email Address", exact=True).click()
        # iframe.get_by_label("Enter Email Address").wait_for(state="visible")

        iframe.get_by_placeholder("Email Address", exact=True).fill(email)
        iframe.get_by_role("button", name="Next").click()
        iframe.get_by_placeholder("Enter Password").wait_for(state="visible")
        iframe.get_by_placeholder("Enter Password").fill(password)
        iframe.get_by_role("button", name="Sign In").click()

        page.get_by_role("link", name="Academic Reports").wait_for(state="visible")
        page.get_by_role("link", name="Academic Reports").click()
        print("Clicked on 'Academic Reports'")
        navigate_even_calendar(page)

        weekly_data = process_calendar_data(page)

        page.get_by_role("link", name="Academic Reports").click()

        navigate_to_timetable(page)
        timetable_data = scrape_table_data(page)

        batch_number = get_batch_number(page)
        page.get_by_role("link", name="Academic Reports").click()

        if batch_number == 1:
            navigate_batch1(page)
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_selector("table[align='center']")
            batch_data = scrape_batch1_data(page)
        elif batch_number == 2: 
            navigate_batch2(page)
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_selector("table[align='center']")
            batch_data = scrape_batch2_data(page)
        else:
            batch_data = ["error in fetching batch data"]
        

        def map_weekly_schedule(timetable_data, batch_data, weekly_data):
            slot_to_details = {}

            for row in timetable_data[1:]:  
                slot_to_details[row[1]] = {"course": row[0], "room": row[2]}

            time_slots = batch_data[0][1:]  
            weekly_schedule = []

            for entry in weekly_data:
                if not isinstance(entry, list) or len(entry) != 3:
                    logging.error(f"Invalid entry in weekly_data: {entry}")
                    continue  

                day_number, day_name, day_order = entry  
                date = format_date(day_number)  

                print(f"Processing: {date}, {day_name}, Day Order: {day_order}")  

                if day_order == 0:  
                    weekly_schedule.append([date, day_name, []])  
                    continue

                if day_order + 2 >= len(batch_data):  
                    logging.error(f"Day order {day_order} out of bounds for batch_data")
                    weekly_schedule.append([date, day_name, []])
                    continue

                current_day_order_data = batch_data[day_order + 2] # 3rd row DO starts , current_day_order_data -> ["day 1","A","C"...]
                
                course_details = []

                for i in range(1, len(current_day_order_data)):
                    slot = current_day_order_data[i]
                    main_slot = slot.split('/')[0].strip()  

                    if main_slot not in slot_to_details:
                        continue

                    updated_time_slot = time_slots[i-1].replace('\t', '')

                    try:
                        start_time, end_time = map(str.strip, updated_time_slot.split('-'))
                        course_info = [
                            slot_to_details[main_slot]["course"],
                            start_time,
                            end_time,
                            slot_to_details[main_slot]["room"]
                        ]
                        course_details.append(course_info)
                    except ValueError as e:
                        logging.error(f"Time slot error: {updated_time_slot}, {e}")
                        continue

                weekly_schedule.append([date, day_name, course_details])

            return weekly_schedule


        weekly_schedule = (map_weekly_schedule(timetable_data,batch_data,weekly_data))


        span_selector = ".zc-header .navbar_user_name"
        page.locator(span_selector).click()
        page.locator("#portalLogout").click()


        print("SUCCESS") 
        print(json.dumps(weekly_schedule))  
        return True
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False
    finally:
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