from redis_config import redis_conn
from rq import Queue

RESULT_TTL = 86400


def store_result(task_id, result):
    result_key = f"result:{task_id}"
    redis_conn.set(result_key, result)
    redis_conn.expire(result_key, RESULT_TTL)


def get_result(task_id):
    result_key = f"result:{task_id}"
    
    return redis_conn.get(result_key)


def store_task_status(task_id, status, message=None):
    status_key = f"status:{task_id}"
    data = {
        "status": status,
        "message": message or ""
    }

    redis_conn.hset(status_key, mapping=data)
    redis_conn.expire(status_key, RESULT_TTL)


def get_task_status(task_id):
    status_key = f"status:{task_id}"
    status_data = redis_conn.hgetall(status_key)
    if not status_data:
        return {"status": "not_found", "message": "Task not found"}
    
    return status_data 


default_queue = Queue('default', connection=redis_conn)
high_queue = Queue('high', connection=redis_conn)