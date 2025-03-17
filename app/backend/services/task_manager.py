import multiprocessing
import time
from datetime import datetime , timedelta
from playwright.sync_api import sync_playwright
from configs.supabase_config import supabase
import ssl
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from fastapi import HTTPException
from threading import Semaphore

max_workers = 3


task_queue = []
process_pool = []


thread_pool = ThreadPoolExecutor(max_workers=10)
task_lock = Lock()
max_workers = 5

browser_semaphore = Semaphore(5)  
task_lock = Lock()
thread_pool = ThreadPoolExecutor(max_workers=10)

def process_task(email, password, task_id):
    try:
        if not browser_semaphore.acquire(timeout=30):
            raise Exception("Browser resource timeout - too many concurrent sessions")

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--disable-gpu",
                        "--disable-dev-shm-usage",
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--ignore-certificate-errors",
                        "--ignore-ssl-errors",
                        "--disable-web-security"
                    ]
                )
                context = browser.new_context(
                    bypass_csp=True,
                    ignore_https_errors=True
                )
                
                try:
                    from services.login_script import login_and_scrape
                    
                    supabase.table('tasks').update({
                        'status': 'processing',
                        'started_at': datetime.now().isoformat()
                    }).eq('task_id', task_id).execute()
                    
                    schedule_data = login_and_scrape(p, email, password)
                    print(f"Scraped data for task {task_id}:", schedule_data)
                    
                    if schedule_data:
                        supabase.table('tasks').update({
                            'status': 'completed',
                            'result': schedule_data,
                            'completed_at': datetime.now().isoformat()
                        }).eq('task_id', task_id).execute()
                    else:
                        raise Exception("No data received from scraping")
                        
                except Exception as e:
                    print(f"Task failed: {str(e)}")
                    supabase.table('tasks').update({
                        'status': 'failed',
                        'error': str(e),
                        'completed_at': datetime.now().isoformat()
                    }).eq('task_id', task_id).execute()
                finally:
                    context.close()
                    browser.close()
        finally:
            browser_semaphore.release()
            
    except Exception as e:
        print(f"Error in process_task: {e}")
        supabase.table('tasks').update({
            'status': 'failed',
            'error': str(e),
            'completed_at': datetime.now().isoformat()
        }).eq('task_id', task_id).execute()

def add_task(email: str, password: str) -> str:
    task_id = f"{email}_{int(time.time())}"
    
    try:
        with task_lock:
            # retry
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = supabase.table('tasks')\
                        .select('task_id')\
                        .eq('email', email)\
                        .in_('status', ['pending', 'processing'])\
                        .execute()
                    
                    if response.data:
                        return response.data[0]['task_id']
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    time.sleep(1)
            task_queue.append((email, password, task_id))
            
            supabase.table('tasks').insert({
                'task_id': task_id,
                'email': email,
                'status': 'pending',
                'created_at': datetime.now().isoformat()
            }).execute()

        cleanup_processes()
        process_queued_tasks()
        
        return task_id
    except Exception as e:
        print(f"Error adding task: {e}")
        raise HTTPException(status_code=500, detail="Failed to create task")

def process_queued_tasks():
    while len(process_pool) < max_workers and task_queue:
        email, password, task_id = task_queue.pop(0)
        process = multiprocessing.Process(
            target=process_task,
            args=(email, password, task_id)
        )
        process.start()
        process_pool.append(process)


def cleanup_processes():
    global process_pool
    process_pool = [p for p in process_pool if p.is_alive()]


def get_task_status(task_id: str) -> dict:
    response = supabase.table('tasks')\
        .select('*')\
        .eq('task_id', task_id)\
        .execute()
    
    if response.data:
        task = response.data[0]
        status = task['status']
        result = task.get('result')
        error = task.get('error')

        if status == 'completed' and result:
            print(f"Returning completed task data for {task_id}")
            print("Result data:", result)
            
            supabase.table('tasks').update({
                'data_retrieved': True
            }).eq('task_id', task_id).execute()

            return {
                'status': status,
                'result': result,
                'error': None
            }

        return {
            'status': status,
            'result': None,
            'error': error
        }
    return {'status': 'not_found'}