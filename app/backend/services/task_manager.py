import multiprocessing
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
from configs.supabase_config import supabase

max_workers = 3
process_pool = []

def process_task(email, password, task_id):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            try:
                from services.login_script import login_and_scrape
                
                supabase.table('tasks').update({
                    'status': 'processing',
                    'started_at': datetime.now().isoformat()
                }).eq('task_id', task_id).execute()
                
                result = login_and_scrape(p, email, password)
                
                supabase.table('tasks').update({
                    'status': 'completed',
                    'result': result,
                    'completed_at': datetime.now().isoformat()
                }).eq('task_id', task_id).execute()
                    
            except Exception as e:
                supabase.table('tasks').update({
                    'status': 'failed',
                    'error': str(e),
                    'completed_at': datetime.now().isoformat()
                }).eq('task_id', task_id).execute()
            finally:
                context.close()
                browser.close()
    except Exception as e:
        print(f"Error in process_task: {e}")


def cleanup_processes():
    global process_pool
    process_pool = [p for p in process_pool if p.is_alive()]


def add_task(email: str, password: str) -> str:
    task_id = f"{email}_{int(time.time())}"
    
    supabase.table('tasks').insert({
        'task_id': task_id,
        'email': email,
        'status': 'pending',
        'created_at': datetime.now().isoformat()
    }).execute()

    cleanup_processes()
    
    if len(process_pool) < max_workers:
        process = multiprocessing.Process(
            target=process_task,
            args=(email, password, task_id)
        )
        process.start()
        process_pool.append(process)

    return task_id


def get_task_status(task_id: str) -> dict:
    response = supabase.table('tasks')\
        .select('*')\
        .eq('task_id', task_id)\
        .execute()
    
    if response.data:
        return {
            'status': response.data[0]['status'],
            'result': response.data[0].get('result'),
            'error': response.data[0].get('error')
        }
    return {'status': 'not_found'}