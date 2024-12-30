import sys
import os

app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(app_dir)
print(sys.path)
from test_login import login

def june(page):
    june_data = []

    for i in range(1,31):
        date = page.locator(f"tr:nth-child({i+1}) > td").first
        day = page.locator(f"tr:nth-child({i+1}) > td:nth-child(2)").first
        day_order = page.locator(f"tr:nth-child({i+1}) > td:nth-child(4)").first

        data = (date.text_content(), day.text_content(), day_order.text_content())
        june_data.append(data)
    # print(june_data)
    # print(type(june_data))


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

        data = (date.text_content(), day.text_content(), day_order.text_content())
        july_data.append(data)

    # print(july_data)
    # print(type(july_data))


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

        data = (date.text_content(), day.text_content(), day_order.text_content())
        august_data.append(data)

    # print(august_data)
    # print(type(august_data))


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

        data = (date.text_content(), day.text_content(), day_order.text_content())
        september_data.append(data)

    # print(september_data)


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

        data = (date.text_content(), day.text_content(), day_order.text_content())
        october_data.append(data)

    # print(october_data)


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

        data = (date.text_content(), day.text_content(), day_order.text_content())
        november_data.append(data)

    # print(november_data)


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

        data = (date.text_content(), day.text_content(), day_order.text_content())
        december_data.append(data)

    print(december_data)
    print(type(december_data))


def test_load_session(playwright):

    page , context, browser = login(playwright)

    if page is None or context is None or browser is None:
        print("Login failed...Please check your credentials and try again.")
        return

    page.goto("https://academia.srmist.edu.in/#WELCOME")
    print("Navigated to the Circular page after loading session.")
    page.wait_for_timeout(3000)

    try:
        page.get_by_role("link", name=" Academic Reports").click()
        print("Clicked on 'Academic Reports'")

        page.get_by_role("link", name=" Academic Planner 2024 25 ODD").click()
        print("Clicked on 'Academic Planner 2024 25 ODD'")
        page.wait_for_timeout(3000)  
    

        # june(page)
        # july(page)
        # august(page)
        # september(page)
        # october(page)
        # november(page)
        december(page)
        
    except Exception as e:
        print(f"Error during interaction: {e}")
    
    browser.close()

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    with sync_playwright() as playwright:
        test_load_session(playwright)