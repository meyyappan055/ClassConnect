import sys
import os
import json
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(app_dir)

from test_login import COOKIES_FILE, login


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


def load_cookies(context):
    if os.path.exists(COOKIES_FILE):
        with open(COOKIES_FILE, "r") as f:
            cookies = json.load(f)
        context.add_cookies(cookies)
        print(f"Cookies loaded from {COOKIES_FILE}")
    else:
        print("error in loading cookies")


def navigate_batch1(page):
    page.get_by_role("link", name=" Unified Time Table").click()
    page.get_by_role("link", name=" Unified Time Table 2024-Batch").click()
    # time.sleep(3)


def navigate_batch2(page):
    page.get_by_role("link", name=" Unified Time Table", exact=True).click()
    page.get_by_role("link", name=" Unified Time Table-2024-Batch").click()
    time.sleep(3)


def scrape_batch1_data(page):
    page.reload()
    page.wait_for_load_state('domcontentloaded')
    page.wait_for_selector("table", timeout=4000)
    page_html = page.content()
    soup = BeautifulSoup(page_html, "html.parser")
    table = soup.find("table", {"align": "center"})
    rows = table.find_all("tr")
    
    batch1_data = []
    for row in rows:
        columns = row.find_all("td")
        column_data = [column.text.strip() for column in columns]
        batch1_data.append(column_data)

    return batch1_data


def scrape_batch2_data(page):
    # page.reload()
    # page.wait_for_load_state('domcontentloaded')
    # page.wait_for_selector("table", timeout=4000)
    page_html = page.content()
    soup = BeautifulSoup(page_html, "html.parser")
    table = soup.find("table", {"align": "center"})
    rows = table.find_all("tr")
    
    batch2_data = []
    for row in rows:
        columns = row.find_all("td")
        column_data = [column.text.strip() for column in columns]
        batch2_data.append(column_data)

    return batch2_data


def test_unified_timetable(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    load_cookies(context)

    page = context.new_page()
    page.goto("https://academia.srmist.edu.in/#WELCOME")
    page.wait_for_timeout(2000)

    page, context, browser = check_login(page, playwright)

    navigate_batch1(page)
    batch1_timetable_data = scrape_batch1_data(page)
    print(batch1_timetable_data)

    navigate_batch2(page)
    batch2_timetable_data = scrape_batch2_data(page)
    print(batch2_timetable_data)


    browser.close()



if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_unified_timetable(playwright)