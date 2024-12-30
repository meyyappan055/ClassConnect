from playwright.sync_api import Playwright, sync_playwright
import os
from dotenv import load_dotenv
import json

load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

COOKIES_FILE = "session_cookies.json"

def login(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://academia.srmist.edu.in/#CIRCULAR")
    page.wait_for_timeout(2000)

    try:
        iframe = page.frame(name="zohoiam")
        iframe.get_by_label("Enter Email Address").fill(USERNAME)
        iframe.get_by_role("button", name="Next").click()
        page.wait_for_timeout(1000)

        iframe.get_by_placeholder("Enter Password").fill(PASSWORD)
        iframe.get_by_role("button", name="Sign In").click()
        page.wait_for_timeout(5000)

        cookies = context.cookies() #using cookies as site is limiting login requests while testing
        with open(COOKIES_FILE, "w") as f:
            json.dump(cookies, f)
        print(f"Cookies saved to {COOKIES_FILE}")

    except Exception as e:
        print(f"Login error: {e}")
        browser.close()
        return None, None, None

    print("Login successful!")
    return page, context, browser

if __name__ == "__main__":
    with sync_playwright() as playwright:
        login(playwright)
