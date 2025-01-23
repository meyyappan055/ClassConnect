from fastapi import APIRouter, HTTPException , Request
from fastapi.responses import StreamingResponse
from io import BytesIO
from datetime import date
from typing import List

router = APIRouter()

def get_current_date():
    current_date = str(date.today())  # "2025-01-21"
    current_year = current_date[0:4]
    current_month = current_date[5:7]
    current_day = current_date[8:10]
    return current_year, current_month, current_day


@router.post("/generate-ical")
async def generate_ical(request:Request):
    body = await request.json()
    print("Received data:", body)

    try:
        classes = body.get("data")  
    except Exception as e:
        raise HTTPException(status_code=422, detail="Invalid input format: " + str(e))

    year, month, day = get_current_date()
    
    def create_ics_file(events):
        ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Class Connect//NONSGML v1.0//EN\n"
        
        for i, event in enumerate(events):
            title, start_time, end_time, location = event
            
            start_hour, start_mins = start_time.split(":")
            end_hour, end_mins = end_time.split(":")
            
            start_hour_utc = int(start_hour) - 5
            start_mins_utc = int(start_mins) - 30
            end_hour_utc = int(end_hour) - 5
            end_mins_utc = int(end_mins) - 30

            if start_mins_utc < 0:
                start_hour_utc -= 1
                start_mins_utc += 60
                
            if end_mins_utc < 0:
                end_hour_utc -= 1
                end_mins_utc += 60

            if start_hour_utc < 0:
                start_hour_utc += 24 
            if end_hour_utc < 0:
                end_hour_utc += 24 
    
            formatted_start = f"{year}{month}{day}T{str(start_hour_utc).zfill(2)}{str(start_mins_utc).zfill(2)}00Z"
            formatted_end = f"{year}{month}{day}T{str(end_hour_utc).zfill(2)}{str(end_mins_utc).zfill(2)}00Z"

            event_content = f"""BEGIN:VEVENT
UID:event{i}@example.com
DTSTAMP:{year}{month}{day}T000000Z
DTSTART:{formatted_start}
DTEND:{formatted_end}
SUMMARY:{title}
LOCATION:{location}
DESCRIPTION:Made with Class Connect :)
END:VEVENT
"""
            ics_content += event_content
        
        ics_content += "END:VCALENDAR"
        return ics_content
    

    try:
        ics_content = create_ics_file(classes)
        file_stream = BytesIO(ics_content.encode("utf-8"))
        return StreamingResponse(
            file_stream,
            media_type="text/calendar",
            headers={"Content-Disposition": "attachment; filename=classes.ics"},
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
