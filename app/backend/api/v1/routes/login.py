from fastapi import Depends, APIRouter, HTTPException, Request, Response 
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
import subprocess
import os
import json
from slowapi import Limiter
from slowapi.util import get_remote_address


router = APIRouter()

def get_limiter(request: Request):
    return request.app.state.limiter

class LoginData(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
async def login(
    request: Request,
    login_data: LoginData,
    response: Response,
    limiter=Depends(get_limiter)  
):

    @limiter.limit("3/minute")
    async def limited_login():
        if not login_data.email.endswith("@srmist.edu.in"):
            raise HTTPException(status_code=401, detail="Invalid email domain. Use your SRM email.")

        script_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "services", "login_script.py")

        result = subprocess.run(
            ["python", script_path, login_data.email, login_data.password],
            capture_output=True,
            text=True
        )

        if "SUCCESS" in result.stdout:
            try:
                json_data = json.loads(result.stdout.strip().split('\n')[1])
                return JSONResponse(content={"status": "success", "message": "Login successful", "data": json_data})
            except Exception:
                raise HTTPException(status_code=500, detail="Failed to parse data")

        raise HTTPException(status_code=401, detail=result.stderr.strip() or result.stdout.strip() or "Login failed")

    return await limited_login()