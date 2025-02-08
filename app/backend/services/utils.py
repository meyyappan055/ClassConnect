from datetime import date
from test_odd_calendar_scraper import june,july,august,september,october,november,december
from test_even_calendar_scraper import january,february,march,april,may

def get_current_date():
    current_date = str(date.today()) # 2025-01-01
    current_year = current_date[0:4]
    current_month = current_date[5:7]
    current_day = current_date[8:10]

    # To eliminate 0s at beginning
    if current_day.startswith("0"):
        current_day = current_day[1]
    if current_month.startswith("0"):
        current_month = current_month[1]

    return int(current_year),int(current_month),int(current_day)


def process_calendar_data(page):
    year, month, day = get_current_date()
    # print(f"Year: {year}, Month: {month}, Day: {day}")
    
    # For testing purposes
    month = 2
    
    month_data = None
    if month == 1:
        month_data = january(page)
    elif month == 2:
        month_data = february(page)
    elif month == 3:
        month_data = march(page)
    elif month == 4:
        month_data = april(page)
    elif month == 5:
        month_data = may(page)
    elif month == 6:
        month_data = june(page)
    elif month == 7:
        month_data = july(page)
    elif month == 8:
        month_data = august(page)
    elif month == 9:
        month_data = september(page)
    elif month == 10:
        month_data = october(page)
    elif month == 11:
        month_data = november(page)
    elif month == 12:
        month_data = december(page)

    if not month_data:
        print(f"No data for the current month: {month}")
        return [None, None]

    if day - 1 >= len(month_data):
        print(f"Day {day} is out of range for month {month}")
        return [None, None]


    weekly_schedule = []

    calendar_data = [ month_data[day - 1], month_data[day],month_data[day+1],month_data[day+2],month_data[day+3],month_data[day+4],month_data[day+5]]

    for i in calendar_data:
        date = i["date"]
        day_name = i["day"]
        day_order = i["day_order"]

        if day_order == "-":
            day_order = 0
        elif day_order != "-":
            day_order = int(day_order)

        weekly_schedule.append([date,day_name,day_order])
        
    #sample return data => [['2025-2-07','Fri', 5], ['2025-2-08','Sat', 0], ['2025-2-09','Sun', 0], ['2025-2-10','Mon', 1], ['2025-2-11','Tue', 0], ['2025-2-12','Wed', 2], ['2025-2-13','Thu', 3]]
    return weekly_schedule
