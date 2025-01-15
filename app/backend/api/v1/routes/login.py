from fastapi import APIRouter, HTTPException
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
        
        
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        
        if "SUCCESS" in result.stdout:
            try:
                
                output_lines = result.stdout.strip().split('\n')
                data_line = output_lines[output_lines.index("SUCCESS") + 1]
                june_data = json.loads(data_line)
                
                return {
                    "status": "success",
                    "message": "Login successful",
                    # fetched data
                    "data": june_data
                }
            except Exception as e:
                print(f"Data parsing error: {e}")
                raise HTTPException(status_code=500, detail="Failed to parse data")
        else:
            error_msg = result.stderr.strip() or result.stdout.strip() or "Login failed"
            raise HTTPException(status_code=401, detail=error_msg)
            
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))