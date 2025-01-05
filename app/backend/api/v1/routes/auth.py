from fastapi import APIRouter, HTTPException , Request
from pydantic import BaseModel
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
    authorize_params=None,
    access_token_url="https://oauth2.googleapis.com/token",
    refresh_token_url=None,
    client_kwargs={
        'scope': 'openid email profile https://www.googleapis.com/auth/calendar'
    }
)


@router.get("/login")
async def login(request:Request):
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/callback")
async def callback(request:Request):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    return {"user": user, "access_token": token.get("access_token")} 