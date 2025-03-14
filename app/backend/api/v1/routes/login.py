from fastapi import Depends, APIRouter, HTTPException, Request, Response 
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
import subprocess
import os
import json
from slowapi import Limiter
from slowapi.util import get_remote_address
from services.task_manager import add_task, get_task_status

router = APIRouter()

def get_limiter(request: Request):
    return request.app.state.limiter

class LoginData(BaseModel):
    email: EmailStr
    password: str

limiter = Limiter(key_func=get_remote_address)


@router.post("/login")
@limiter.limit("3/minute") 
async def login(
    request: Request,
    login_data: LoginData,
    response: Response
):
    print("Login request received for:", login_data.email) 

    if not login_data.email.endswith("@srmist.edu.in"):
        raise HTTPException(status_code=401, detail="Invalid email domain. Use your SRM email.")

    task_id = add_task(login_data.email, login_data.password)
    print(f"Task ID generated: {task_id}") 
    
    return JSONResponse(content={
        "status": "success", 
        "message": "Login request received", 
        "task_id": task_id
    })

@router.get("/status/{task_id}")
async def get_status(task_id: str, response: Response, limiter: Limiter = Depends(get_limiter)):
    print(f"Checking status for task: {task_id}")  # Debug log
    result = get_task_status(task_id)
    print(f"Status result: {result}")  # Debug log

    if result['status'] == 'not_found':
        raise HTTPException(status_code=404, detail="Task not found")
    return JSONResponse(content=result)

