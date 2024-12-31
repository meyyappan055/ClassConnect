from fastapi import FastAPI
from api.v1.routes import scraper

app = FastAPI()

app.include_router(scraper.router, prefix="/scraper", tags=["Scraper"])
