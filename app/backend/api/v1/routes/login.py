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

    if not login_data.email.endswith("@srmist.edu.in"):
        raise HTTPException(status_code=401, detail="Invalid email domain. Use your SRM email.")

    task_id = add_task(login_data.email, login_data.password)
    
    return JSONResponse(content={
        "status": "success", 
        "message": "Login request received", 
        "task_id": task_id
    })

    # script_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "services", "login_script.py")

    # result = subprocess.run(
    #     ["python", script_path, login_data.email, login_data.password],
    #     capture_output=True,
    #     text=True
    # )
    
    # print("STDOUT:", result.stdout)
    # print("STDERR:", result.stderr)
    
    # if "SUCCESS" in result.stdout:
    #     try:
    #         output_lines = result.stdout.strip().split('\n')
    #         success_index = -1
            
    #         for i, line in enumerate(output_lines):
    #             if line.strip() == "SUCCESS":
    #                 success_index = i
    #                 break
            
    #         if success_index >= 0 and success_index + 1 < len(output_lines):
    #             json_data = json.loads(output_lines[success_index + 1])
    #             return JSONResponse(content={"status": "success", "message": "Login successful", "data": json_data})
    #         else:
    #             raise HTTPException(status_code=500, detail="Missing data after SUCCESS marker")
    #     except json.JSONDecodeError as e:
    #         raise HTTPException(status_code=500, detail=f"JSON parsing error: {str(e)}")
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=f"Failed to parse data: {str(e)}")

    # raise HTTPException(status_code=401, detail=result.stderr.strip() or result.stdout.strip() or "Login failed")


@router.get("/status/{task_id}")
async def get_status(task_id: str, response: Response, limiter: Limiter = Depends(get_limiter)):
    result = get_task_status(task_id)

    if result['status'] == 'not_found':
        raise HTTPException(status_code=404, detail="Task not found")
    return JSONResponse(content=result)

