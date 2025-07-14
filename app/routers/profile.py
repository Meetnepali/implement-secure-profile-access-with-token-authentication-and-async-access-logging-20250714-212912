from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from typing import Dict, List
from datetime import datetime
import jwt

# Constants must match those in auth.py
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

MOCK_USER = {
    "username": "alice",
    "password": "password123",
    "full_name": "Alice Doe",
    "email": "alice@example.com"
}

MENU_ACCESS_LOG: List[Dict] = []  # type: ignore

class ProfileResponse(BaseModel):
    username: str
    full_name: str
    email: EmailStr

class ErrorResponse(BaseModel):
    detail: str

async def log_profile_access(username: str, req: Request):
    log_entry = {
        "username": username,
        "accessed_at": datetime.utcnow().isoformat() + "Z",
        "client_host": req.client.host if req.client else None
    }
    MENU_ACCESS_LOG.append(log_entry)


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username != MOCK_USER["username"]:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

@router.get("/profile", response_model=ProfileResponse, responses={
    401: {"model": ErrorResponse},
    403: {"model": ErrorResponse}
})
async def get_profile(
    background_tasks: BackgroundTasks,
    request: Request,
    username: str = Depends(verify_token),
):
    profile = {
        k: MOCK_USER[k] for k in ("username","full_name","email")
    }
    background_tasks.add_task(log_profile_access, username, request)
    return profile
