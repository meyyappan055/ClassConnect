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



def login_and_scrape(playwright: Playwright, email: str, password: str):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    try:
        page.goto("https://academia.srmist.edu.in/#CIRCULAR")
        iframe = page.frame(name="zohoiam")
    
        iframe.get_by_label("Enter Email Address").wait_for(state="visible")
        iframe.get_by_label("Enter Email Address").fill(email)
        iframe.get_by_role("button", name="Next").click()
        iframe.get_by_placeholder("Enter Password").wait_for(state="visible")
        iframe.get_by_placeholder("Enter Password").fill(password)
        iframe.get_by_role("button", name="Sign In").click()

        page.get_by_role("link", name="Academic Reports").wait_for(state="visible")
        page.get_by_role("link", name="Academic Reports").click()
        print("Clicked on 'Academic Reports'")
        

        navigate_even_calendar(page)
        day_name, day_order = process_calendar_data(page)
 
        if day_order != "-":
            day_order = int(day_order) # 1 or 2..

        page.get_by_role("link", name="Academic Reports").click()

        navigate_to_timetable(page)
        timetable_data = scrape_table_data(page)

        batch_number = get_batch_number(page)
        if batch_number == 1:
            navigate_batch1(page)
            batch_data = scrape_batch1_data(page)
        elif batch_number == 2: 
            navigate_batch2(page)
            batch_data = scrape_batch2_data(page)
        else:
            batch_data = ["error in fetching batch data"]
        
        current_day_order_data = batch_data[day_order+2] # 3rd row DO starts , current_day_order_data -> ["day 1","A","C"...]

        for i in range(1,len(timetable_data)): # first row is heading
            slot_data = timetable_data[i]
            for j in range(len(current_day_order_data)):
                if slot_data[1] == current_day_order_data[j]:
                    current_day_order_data[j] = slot_data[1]

        
        scraped_data = [current_day_order_data] # -> ["day 1","Math","AI"...]
        
        print("SUCCESS") 
        print(json.dumps(scraped_data))  
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