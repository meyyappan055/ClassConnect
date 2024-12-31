from fastapi import APIRouter

router = APIRouter()


@router.get("/calendar")
def get_calendar():
    return {}

@router.get("/timetable")
def get_timetable():
    return {}

@router.get("/unified-timetable")
def get_unified_timetable():
    return {}


