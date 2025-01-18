from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def navigate_to_timetable(page):
    """Navigate to the timetable page after login."""
    page.get_by_role("link", name="").click()
    page.get_by_role("link", name="My Time Table & Attendance").click()
    page.get_by_role("link", name="My Time Table 2024-").click()
    
    
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
        room_no = column_data[9]
        content = [subject_title, subject_slot, room_no]
        data.append(content)

    return data


def get_batch_number(page):
    page_html = page.content()
    soup = BeautifulSoup(page_html, "html.parser")
    table = soup.find("table", {"align": "left"})
    rows = table.find_all("tr")

    batch_data = []
    for row in rows:
        columns = row.find_all("td")
        column_data = [column.text.strip() for column in columns]
        col1 = column_data[1]
        batch_data.append(col1)
    
    batch_number  = int(batch_data[1])  
    
    return batch_number # -> 1 or 2
        