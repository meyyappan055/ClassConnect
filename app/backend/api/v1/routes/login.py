from fastapi import APIRouter, HTTPException , Response
from pydantic import BaseModel
import subprocess
import os
import json

router = APIRouter()

class LoginData(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(login_data: LoginData):
    try:
        if not login_data.email.endswith("@srmist.edu.in"):
            raise HTTPException(
                status_code=401, 
                detail="Invalid email domain. Please use your SRM email."
            )
            
        script_path = os.path.join(
            os.path.dirname(__file__), 
            "..", "..", "..",
            "services",
            "login_script.py"
        )
        
        result = subprocess.run(
            ["python", script_path, login_data.email, login_data.password],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            try:
                json_data = json.loads(result.stdout) 
                return json_data
            except json.JSONDecodeError:
                raise HTTPException(status_code=500, detail="Failed to parse JSON response")

        error_msg = result.stderr.strip() or "Login failed"
        raise HTTPException(status_code=401, detail=error_msg)

    except Exception as e:
        print("An error occurred:", str(e))
        raise HTTPException(status_code=500, detail=str(e))