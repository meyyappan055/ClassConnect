import sys
import os
import json
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(app_dir)

from test_login import COOKIES_FILE, login


def load_cookies(context):
    if os.path.exists(COOKIES_FILE):
        with open(COOKIES_FILE, "r") as f:
            cookies = json.load(f)
        context.add_cookies(cookies)
        print(f"Cookies loaded from {COOKIES_FILE}")


def check_login(page, playwright):
 
    if page.url != "https://academia.srmist.edu.in/#WELCOME":
        print("Session expired or cookies invalid. Logging in again...")
        page, context, browser = login(playwright)  
        return page, context, browser
    else:
        print("Logged in using session cookies.")
        context = page.context  
        browser = context.browser  
        return page, context, browser  


def navigate_to_timetable(page):
    """Navigate to the timetable page after login."""
    page.get_by_role("link", name="").click()
    page.get_by_role("link", name=" My Time Table & Attendance").click()
    page.get_by_role("link", name=" My Time Table 2024-").click()


def scrape_table_data(page):
    """Scrape the timetable table data."""
    page.wait_for_selector("table.course_tbl", timeout=2000)
    page_html = page.content()
    soup = BeautifulSoup(page_html, "html.parser")
    table = soup.find("table", class_="course_tbl")
    rows = table.find_all("tr")
    
    data = []
    for row in rows:
        columns = row.find_all("td")
        column_data = [column.text.strip() for column in columns]
        subject_title = column_data[2]
        subject_slot = column_data[8]
        room_no = column_data[10]
        content = [subject_title, subject_slot, room_no]
        data.append(content)

    return data


def test_timetable_scraper(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    load_cookies(context)
    
    page = context.new_page()
    page.goto("https://academia.srmist.edu.in/#WELCOME")
    page.wait_for_timeout(2000)

    page, context, browser = check_login(page, playwright)

    navigate_to_timetable(page)
    user_timetable_data = scrape_table_data(page)
    print(user_timetable_data)

    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_timetable_scraper(playwright)
