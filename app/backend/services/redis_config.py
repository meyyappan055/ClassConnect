from redis import Redis
from rq import Queue
from dotenv import load_dotenv
import os 

load_dotenv()

try : 
    REDIS_URL = os.getenv("REDIS_URL")
except Exception as e : 
    print(f"Error in redis importing URL from .env: {e}")

redis_conn = Redis.from_url(REDIS_URL)