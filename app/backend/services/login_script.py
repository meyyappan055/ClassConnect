from playwright.sync_api import Playwright, sync_playwright
import sys
import json
from bs4 import BeautifulSoup
from test_odd_calendar_scraper import june,july,august,september,october,november,december
from test_even_calendar_scraper import january,february,march,april,may


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
        
        # page.get_by_role("link", name="Academic Planner 2024 25 ODD").wait_for(state="visible")
        # page.get_by_role("link", name="Academic Planner 2024 25 ODD").click()
        # print("Clicked on 'Academic Planner 2024 25 ODD'")
        
        page.get_by_role("link", name="Academic Planner 2024-25-EVEN").wait_for(state="visible")
        page.get_by_role("link", name="Academic Planner 2024-25-EVEN").click()
        print("Clicked on 'Academic Planner 2024 25 EVEN'")

        page.get_by_role("link", name="Academic Reports").click()
        

        jan_data = january(page)
        
        print("SUCCESS") 
        print(json.dumps(jan_data))  
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