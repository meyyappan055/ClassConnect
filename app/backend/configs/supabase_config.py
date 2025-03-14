from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

def get_supabase_client():
    try :
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
    except Exception as e:
        print(f"Error in get_supabase_client: {str(e)}")
        
    return create_client(url, key)

supabase = get_supabase_client()