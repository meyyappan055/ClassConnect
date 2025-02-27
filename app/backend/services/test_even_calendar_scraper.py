import sys
import os


def navigate_even_calendar(page):
    page.get_by_role("link", name="Academic Planner 2024-25-EVEN").wait_for(state="visible")
    page.get_by_role("link", name="Academic Planner 2024-25-EVEN").click()
    # print("Clicked on 'Academic Planner 2024 25 EVEN'")


def january(page):
    january_data = []

    # Handling dates 1 to 28
    for i in range(1, 29):
        date = page.locator(f"tr:nth-child({i+1}) > td").first
        day = page.locator(f"tr:nth-child({i+1}) > td:nth-child(2)").first
        day_order = page.locator(f"tr:nth-child({i+1}) > td:nth-child(4)").first

        if date and day and day_order:
            try:
                data = {
                    "date": date.text_content().strip(),
                    "day": day.text_content().strip(),
                    "day_order": day_order.text_content().strip()
                }
                january_data.append(data)
            except Exception as e:
                print(f"Error processing January row {i+1}: {str(e)}")

    # Handling dates 29, 30, 31 separately
    for row_index in range(30, 33):
        date = page.get_by_role("cell", name=f"{row_index-1}").first
        day = page.locator(f"tr:nth-child({row_index}) > td:nth-child(2)").first
        day_order = page.locator(f"tr:nth-child({row_index}) > td:nth-child(4)").first

        if date and day and day_order:
            try : 
                data = {
                    "date": date.text_content().strip(),
                    "day": day.text_content().strip(),
                    "day_order": day_order.text_content().strip()
                }
                january_data.append(data)
            except Exception as e:
                print(f"Error processing January row {row_index}: {str(e)}")

    return january_data


def february(page):
    february_data = []

    try:
        date_row_1 = page.locator("td:nth-child(6)").first
        day_row_1 = page.locator("td:nth-child(7)").first
        day_order_row_1 = page.locator("td:nth-child(9)").first

        if not date_row_1 or not day_row_1 or not day_order_row_1:
            raise ValueError("One or more elements in the first row were not found")

        data = {
            "date": date_row_1.text_content().strip(),
            "day": day_row_1.text_content().strip(),
            "day_order": day_order_row_1.text_content().strip()
        }
        february_data.append(data)

    except Exception as e:
        print(f"[ERROR] February first row: {str(e)}")

    for i in range(1, 28):
        try:
            row_index = i + 2  

            date = page.locator(f"tr:nth-child({row_index}) > td:nth-child(6)").first
            day = page.locator(f"tr:nth-child({row_index}) > td:nth-child(7)").first
            day_order = page.locator(f"tr:nth-child({row_index}) > td:nth-child(9)").first

            if not date or not day or not day_order:
                raise ValueError(f"Row {row_index}: One or more elements not found")

            data = {
                "date": date.text_content().strip(),
                "day": day.text_content().strip(),
                "day_order": day_order.text_content().strip()
            }
            february_data.append(data)

        except Exception as e:
            print(f"[ERROR] Row {row_index}: {str(e)}")

    return february_data


def march(page):
    march_data = []

    date_row_1 = page.locator("td:nth-child(11)").first
    day_row_1 = page.locator("td:nth-child(12)").first
    day_order_row_1 = page.locator("td:nth-child(14)").first
    
    if date_row_1 and day_row_1 and day_order_row_1:
        try:
            data = {
                "date": date_row_1.text_content().strip(),
                "day": day_row_1.text_content().strip(),
                "day_order": day_order_row_1.text_content().strip()
            }
            march_data.append(data)
        except Exception as e:
            print(f"Error processing March first row: {str(e)}")

    for i in range(1, 31):  
        date = page.locator(f"tr:nth-child({i+2}) > td:nth-child(11)").first
        day = page.locator(f"tr:nth-child({i+2}) > td:nth-child(12)").first
        day_order = page.locator(f"tr:nth-child({i+2}) > td:nth-child(14)").first

        if date and day and day_order:
            try:
                data = {
                    "date": date.text_content().strip(),
                    "day": day.text_content().strip(),
                    "day_order": day_order.text_content().strip()
                }
                march_data.append(data)
            except Exception as e:
                print(f"Error processing March row {i+2}: {str(e)}")

    return march_data


def april(page):
    april_data = []

    date_row_1 = page.locator("td:nth-child(16)").first
    day_row_1 = page.locator("td:nth-child(17)").first
    day_order_row_1 = page.locator("td:nth-child(19)").first
    
    if date_row_1 and day_row_1 and day_order_row_1:
        try:
            data = {
                "date": date_row_1.text_content().strip(),
                "day": day_row_1.text_content().strip(),
                "day_order": day_order_row_1.text_content().strip()
            }
            april_data.append(data)
        except Exception as e:
            print(f"Error processing April first row: {str(e)}")

    for i in range(1, 30):  
        date = page.locator(f"tr:nth-child({i+2}) > td:nth-child(16)").first
        day = page.locator(f"tr:nth-child({i+2}) > td:nth-child(17)").first
        day_order = page.locator(f"tr:nth-child({i+2}) > td:nth-child(19)").first

        if date and day and day_order:
            try:
                data = {
                    "date": date.text_content().strip(),
                    "day": day.text_content().strip(),
                    "day_order": day_order.text_content().strip()
                }
                april_data.append(data)
            except Exception as e:
                print(f"Error processing April row {i+2}: {str(e)}")

    return april_data


def may(page):
    may_data = []

    date_row_1 = page.locator("td:nth-child(21)").first
    day_row_1 = page.locator("td:nth-child(22)").first
    day_order_row_1 = page.locator("td:nth-child(24)").first
    
    if date_row_1 and day_row_1 and day_order_row_1:
        try:
            data = {
                "date": date_row_1.text_content().strip(),
                "day": day_row_1.text_content().strip(),
                "day_order": day_order_row_1.text_content().strip()
            }
            may_data.append(data)
        except Exception as e:
            print(f"Error processing May first row: {str(e)}")

    for i in range(1, 31):  
        date = page.locator(f"tr:nth-child({i+2}) > td:nth-child(21)").first
        day = page.locator(f"tr:nth-child({i+2}) > td:nth-child(22)").first
        day_order = page.locator(f"tr:nth-child({i+2}) > td:nth-child(24)").first

        if date and day and day_order:
            try:
                data = {
                    "date": date.text_content().strip(),
                    "day": day.text_content().strip(),
                    "day_order": day_order.text_content().strip()
                }
                may_data.append(data)
            except Exception as e:
                print(f"Error processing May row {i+2}: {str(e)}")

    return may_data