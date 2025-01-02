from fastapi import FastAPI
from api.v1.routes import scraper
from api.v1.routes import login
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(scraper.router, prefix="/scraper", tags=["Scraper"])
app.include_router(login.router, prefix="/api")