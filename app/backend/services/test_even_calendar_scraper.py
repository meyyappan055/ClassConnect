import sys
import os


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

