from fastapi import FastAPI
from api.v1.routes import login , generate_ical
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded


limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "https://classconnect-liart.vercel.app",
    "https://classconnect-meyyappans-projects.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset"]
)


app.include_router(login.router, prefix="/api")
app.include_router(generate_ical.router,prefix="/api")
