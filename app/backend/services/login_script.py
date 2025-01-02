from playwright.sync_api import Playwright, sync_playwright
import sys
import json

COOKIES_FILE = "session_cookies.json"

def login(playwright: Playwright, email: str, password: str):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://academia.srmist.edu.in/#CIRCULAR")

    try:
        iframe = page.frame(name="zohoiam")
        iframe.get_by_label("Enter Email Address").wait_for(state="visible",timeout=5000)
        iframe.get_by_label("Enter Email Address").fill(email)
        iframe.get_by_role("button", name="Next").click()
        
        iframe.get_by_placeholder("Enter Password").wait_for(state="visible")
        iframe.get_by_placeholder("Enter Password").fill(password)
        iframe.get_by_role("button", name="Sign In").click()
        
        cookies = context.cookies()
        with open(COOKIES_FILE, "w") as f:
            json.dump(cookies, f)
        print(f"Cookies saved to {COOKIES_FILE}")
        return True

    except Exception as e:
        print(f"Login error: {e}")
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
        success = login(playwright, email, password)
        if success:
            print("SUCCESS")
            sys.exit(0)
        else:
            print("ERROR: Login failed")
            sys.exit(1)

if __name__ == "__main__":
    main() 