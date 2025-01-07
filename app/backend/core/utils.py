from datetime import date
from app.backend.services.test_odd_calendar_scraper import june,july,august,september,october,november,december
from app.backend.services.test_even_calendar_scraper import january,february,march,april,may

def get_current_date():
    current_date = str(date.today()) # 2025-01-01
    current_year = current_date[0:4]
    current_month = current_date[5:7]
    current_day = current_date[8:10]

    # To eliminate 0s at beginning
    if(current_day[0]==0): 
        current_day = current_day[1]
    if(current_month[0]==0):
        current_month = current_month[1]

    return int(current_year),int(current_month),int(current_day)


def process_calendar_data(page):
        year,month,day = get_current_date()

        if month ==1:
            month_data = january(page)
        
        if month == 2:
            month_data = february(page)
        
        if month == 3:
            month_data = march(page)
        
        if month == 4:
            month_data = april(page)
        
        if month == 5:
            month_data = may(page)
        
        if month == 6:
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
        else:
            print(f"No data for the current month: {month}")
            return

        # print(f"Data for month {month}: {month_data}")

        calendar_data = month_data[day-1] # ('1', 'Sun', ' - ')
        day_name = calendar_data[1] 
        day_order = calendar_data[2]

        return day_name,day_order