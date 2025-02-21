from fastapi import APIRouter, HTTPException , Request
from fastapi.responses import StreamingResponse
from io import BytesIO
from datetime import datetime
from typing import List

router = APIRouter()


def convert_to_utc(year, month, day, time):
    hours, minutes = map(int, time.split(":"))

    if hours < 8: 
        hours += 12

    total_minutes = (hours * 60 + minutes) - (5 * 60 + 30)

    if total_minutes < 0:
        total_minutes += 24 * 60
        day = str(int(day) - 1).zfill(2)

    utc_hours, utc_minutes = divmod(total_minutes, 60)
    return f"{year}{month}{day}T{str(utc_hours).zfill(2)}{str(utc_minutes).zfill(2)}00Z"


@router.post("/generate-ical")
async def generate_ical(request:Request):
    body = await request.json()
    # print("Received data:", body)
    print("received data")

    try:
        classes = body.get("data")  
    except Exception as e:
        raise HTTPException(status_code=422, detail="Invalid input format: " + str(e))


    def create_ics_file(schedule):
        ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Class Connect//NONSGML v1.0//EN\n"
        event_count = 0

        for each_data in schedule:
            event_date, day, events = each_data
            if not events:
                continue

            year, month, day = event_date.split("-")
            month, day = month.zfill(2), day.zfill(2)

            for i, (title, start_time, end_time, location) in enumerate(events):
                if not end_time:
                    if i + 1 < len(events) and events[i + 1][0] == title:
                        end_time = events[i + 1][1]  
                    else:
                        continue  

                formatted_start = convert_to_utc(year, month, day, start_time)
                formatted_end = convert_to_utc(year, month, day, end_time)
                dtstamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

                event_content = f"""BEGIN:VEVENT
UID:event{event_count}@classconnect.com
DTSTAMP:{dtstamp}
DTSTART:{formatted_start}
DTEND:{formatted_end}
SUMMARY:{title}
LOCATION:{location}
DESCRIPTION:Made with Class Connect :)
END:VEVENT
"""
                ics_content += event_content
                event_count += 1

        ics_content += "END:VCALENDAR"
        return ics_content
    

    try:
        ics_content = create_ics_file(classes)
        file_stream = BytesIO(ics_content.encode("utf-8"))
        print("Generated ics file")
        return StreamingResponse(
            file_stream,
            media_type="text/calendar",
            headers={"Content-Disposition": "attachment; filename=classes.ics"},
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
