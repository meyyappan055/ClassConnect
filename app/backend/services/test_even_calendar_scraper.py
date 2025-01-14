import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, project_root)


from app.backend.api.v1.routes import login


def january(page):
    january_data = []

    for i in range(1,31):
        date = page.locator(f"tr:nth-child({i+1}) > td").first
        day = page.locator(f"tr:nth-child({i+1}) > td:nth-child(2)").first
        day_order = page.locator(f"tr:nth-child({i+1}) > td:nth-child(4)").first


        if date and day and day_order:  
                data = {
                    "date": date.text_content().strip(),
                    "day": day.text_content().strip(),
                    "day_order": day_order.text_content().strip()
                }
                january_data.append(data)

    return january_data


def february(page):
    february_data = []

    for i in range(1,28):
        date = page.locator(f"tr:nth-child({i+1}) > td").first
        day = page.locator(f"tr:nth-child({i+1}) > td:nth-child(2)").first
        day_order = page.locator(f"tr:nth-child({i+1}) > td:nth-child(4)").first


        if date and day and day_order:  
                data = {
                    "date": date.text_content().strip(),
                    "day": day.text_content().strip(),
                    "day_order": day_order.text_content().strip()
                }
                february_data.append(data)

    return february_data


def march(page):
    march_data = []

    for i in range(1,31):
        date = page.locator(f"tr:nth-child({i+1}) > td").first
        day = page.locator(f"tr:nth-child({i+1}) > td:nth-child(2)").first
        day_order = page.locator(f"tr:nth-child({i+1}) > td:nth-child(4)").first
        
        if date and day and day_order:  
            data = {
                "date": date.text_content().strip(),
                "day": day.text_content().strip(),
                "day_order": day_order.text_content().strip()
            }
            march_data.append(data)

    return march_data


def april(page):
    april_data = []

    for i in range(1,30):
        date = page.locator(f"tr:nth-child({i+1}) > td").first
        day = page.locator(f"tr:nth-child({i+1}) > td:nth-child(2)").first
        day_order = page.locator(f"tr:nth-child({i+1}) > td:nth-child(4)").first
        
        if date and day and day_order:  
                data = {
                    "date": date.text_content().strip(),
                    "day": day.text_content().strip(),
                    "day_order": day_order.text_content().strip()
                }
                april_data.append(data)

    return april_data


def may(page):
    may_data = []

    for i in range(1,31):
        date = page.locator(f"tr:nth-child({i+1}) > td").first
        day = page.locator(f"tr:nth-child({i+1}) > td:nth-child(2)").first
        day_order = page.locator(f"tr:nth-child({i+1}) > td:nth-child(4)").first
        
        if date and day and day_order:  
            data = {
                "date": date.text_content().strip(),
                "day": day.text_content().strip(),
                "day_order": day_order.text_content().strip()
            }
            may_data.append(data)

    return may_data


def test_load_session(playwright):
    from app.backend.core.utils import process_calendar_data

    page , context, browser = login.login(playwright)

    if page is None or context is None or browser is None:
        print("Login failed...Please check your credentials and try again.")
        return

    page.goto("https://academia.srmist.edu.in/#WELCOME")
    print("Navigated to the Circular page after loading session.")
    

    try:
        page.get_by_role("link", name="Academic Reports").wait_for(state="visible")
        page.get_by_role("link", name="Academic Reports").click()
        print("Clicked on 'Academic Reports'")


        page.get_by_role("link", name="Academic Planner 2024 25 EVEN").wait_for(state="visible")
        page.get_by_role("link", name="Academic Planner 2024 25 EVEN").click()
        print("Clicked on 'Academic Planner 2024 25 EVEN'")
         
        day_name, day_order = process_calendar_data(page)
        print(f"Day name: {day_name}, Day order: {day_order}")

        print(january(page))

    except Exception as e:
        print(f"Error during interaction: {e}")
    
    browser.close()

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    with sync_playwright() as playwright:
        test_load_session(playwright)