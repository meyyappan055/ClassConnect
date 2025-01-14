import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, project_root)


from app.backend.api.v1.routes.login import login

def june(page):
    june_data = []
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
            june_data.append(data)

    return june_data

def july(page):
    july_data = []
    date_row1 = page.locator("td:nth-child(6)").first
    day_row1 = page.locator("td:nth-child(7)").first
    day_order_row1 = page.locator("td:nth-child(9)").first    
    july_data.append((date_row1.text_content(), day_row1.text_content(), day_order_row1.text_content()))
    for i in range(1,30):
        date = page.locator(f"tr:nth-child({i+2}) > td:nth-child(6)").first
        day = page.locator(f"tr:nth-child({i+2}) > td:nth-child(7)").first
        day_order = page.locator(f"tr:nth-child({i+2}) > td:nth-child(9)").first

        if (date and day and day_order) or (date_row1 and day_row1 and day_order_row1):  
                data = {
                    "date": date.text_content().strip(),
                    "day": day.text_content().strip(),
                    "day_order": day_order.text_content().strip()
                }
                july_data.append(data)

    return july_data


def august(page):
    august_data = []
    date_row1 = page.locator("td:nth-child(11)").first
    day_row1 = page.locator("td:nth-child(12)").first
    day_order_row1 = page.locator("td:nth-child(14)").first
    august_data.append((date_row1.text_content(), day_row1.text_content(), day_order_row1.text_content()))

    for i in range(1, 31):  
        date = page.locator(f"tr:nth-child({i+2}) > td:nth-child(11)").first
        day = page.locator(f"tr:nth-child({i+2}) > td:nth-child(12)").first
        day_order = page.locator(f"tr:nth-child({i+2}) > td:nth-child(14)").first

        if (date and day and day_order) or (date_row1 and day_row1 and day_order_row1): 
                data = {
                    "date": date.text_content().strip(),
                    "day": day.text_content().strip(),
                    "day_order": day_order.text_content().strip()
                }
                august_data.append(data)

    return august_data


def september(page):
    september_data = []
    date_row1 = page.locator("td:nth-child(16)").first
    day_row1 = page.locator("td:nth-child(17)").first
    day_order_row1 = page.locator("td:nth-child(19)").first
    september_data.append((date_row1.text_content(), day_row1.text_content(), day_order_row1.text_content()))

    for i in range(1, 30):  
        date = page.locator(f"tr:nth-child({i+2}) > td:nth-child(16)").first
        day = page.locator(f"tr:nth-child({i+2}) > td:nth-child(17)").first
        day_order = page.locator(f"tr:nth-child({i+2}) > td:nth-child(19)").first

        if (date and day and day_order) or (date_row1 and day_row1 and day_order_row1): 
                data = {
                    "date": date.text_content().strip(),
                    "day": day.text_content().strip(),
                    "day_order": day_order.text_content().strip()
                }
                september_data.append(data)

    return september_data


def october(page):
    october_data = []
    date_row1 = page.locator("td:nth-child(21)").first
    day_row1 = page.locator("td:nth-child(22)").first
    day_order_row1 = page.locator("td:nth-child(24)").first
    october_data.append((date_row1.text_content(), day_row1.text_content(), day_order_row1.text_content()))

    for i in range(1, 31):  
        date = page.locator(f"tr:nth-child({i+2}) > td:nth-child(21)").first
        day = page.locator(f"tr:nth-child({i+2}) > td:nth-child(22)").first
        day_order = page.locator(f"tr:nth-child({i+2}) > td:nth-child(24)").first

        if (date and day and day_order) or (date_row1 and day_row1 and day_order_row1):  
                data = {
                    "date": date.text_content().strip(),
                    "day": day.text_content().strip(),
                    "day_order": day_order.text_content().strip()
                }
                october_data.append(data)

    return october_data


def november(page):
    november_data = []
    date_row1 = page.locator("td:nth-child(26)").first
    day_row1 = page.locator("td:nth-child(27)").first
    day_order_row1 = page.locator("td:nth-child(29)").first
    november_data.append((date_row1.text_content(), day_row1.text_content(), day_order_row1.text_content()))

    for i in range(1, 30):  
        date = page.locator(f"tr:nth-child({i+2}) > td:nth-child(26)").first
        day = page.locator(f"tr:nth-child({i+2}) > td:nth-child(27)").first
        day_order = page.locator(f"tr:nth-child({i+2}) > td:nth-child(29)").first

        if (date and day and day_order) or (date_row1 and day_row1 and day_order_row1): 
                data = {
                    "date": date.text_content().strip(),
                    "day": day.text_content().strip(),
                    "day_order": day_order.text_content().strip()
                }
                november_data.append(data)

    return november_data


def december(page):
    december_data = []
    date_row1 = page.locator("td:nth-child(31)").first
    day_row1 = page.locator("td:nth-child(32)").first
    day_order_row1 = page.locator("td:nth-child(34)").first
    december_data.append((date_row1.text_content(), day_row1.text_content(), day_order_row1.text_content()))

    for i in range(1, 31):  
        date = page.locator(f"tr:nth-child({i+2}) > td:nth-child(31)").first
        day = page.locator(f"tr:nth-child({i+2}) > td:nth-child(32)").first
        day_order = page.locator(f"tr:nth-child({i+2}) > td:nth-child(34)").first

        if (date and day and day_order) or (date_row1 and day_row1 and day_order_row1):  
                data = {
                    "date": date.text_content().strip(),
                    "day": day.text_content().strip(),
                    "day_order": day_order.text_content().strip()
                }
                december_data.append(data)

    return december_data


def test_load_session(playwright):
    from app.backend.core.utils import process_calendar_data

    page , context, browser = login(playwright)

    if page is None or context is None or browser is None:
        print("Login failed...Please check your credentials and try again.")
        return

    page.goto("https://academia.srmist.edu.in/#WELCOME")
    print("Navigated to the Circular page after loading session.")
    

    try:
        page.get_by_role("link", name="Academic Reports").wait_for(state="visible")
        page.get_by_role("link", name="Academic Reports").click()
        print("Clicked on 'Academic Reports'")


        page.get_by_role("link", name="Academic Planner 2024 25 ODD").wait_for(state="visible")
        page.get_by_role("link", name="Academic Planner 2024 25 ODD").click()
        print("Clicked on 'Academic Planner 2024 25 ODD'")
         
        day_name, day_order = process_calendar_data(page)
        print(f"Day name: {day_name}, Day order: {day_order}")

    except Exception as e:
        print(f"Error during interaction: {e}")
    
    browser.close()

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    with sync_playwright() as playwright:
        test_load_session(playwright)