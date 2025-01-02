from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import subprocess
import os

router = APIRouter()

class LoginData(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(login_data: LoginData):
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
            [
                "python", 
                script_path, 
                login_data.email, 
                login_data.password
            ],
            capture_output=True,
            text=True
        )

        if "SUCCESS" in result.stdout:
            return {
                "status": "success",
                "message": "Login successful",
                "user": {"email": login_data.email}
            }
        else:
            error_msg = result.stdout.strip() 
            raise HTTPException(
                status_code=401,
                detail=error_msg
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
