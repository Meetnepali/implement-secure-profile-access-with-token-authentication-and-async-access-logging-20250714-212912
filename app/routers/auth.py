from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt

# NOTE: In production, load from env or secure config
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

MOCK_USER = {
    "username": "alice",
    "password": "password123",
    "full_name": "Alice Doe",
    "email": "alice@example.com"
}

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class ErrorResponse(BaseModel):
    detail: str

@router.post("/login", response_model=TokenResponse, responses={
    401: {"model": ErrorResponse}
})
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if (
        form_data.username != MOCK_USER["username"] \
        or form_data.password != MOCK_USER["password"]
    ):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    to_encode = {
        "sub": MOCK_USER["username"],
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return TokenResponse(access_token=token, token_type="bearer")
