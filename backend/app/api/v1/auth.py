from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import os
from datetime import timedelta

from app.core.security import create_access_token

router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCredentials(BaseModel):
    username: str
    password: str


@router.post('/login', response_model=Token)
async def login(creds: UserCredentials):
    demo_user = os.getenv('DEMO_USER', 'admin')
    demo_pass = os.getenv('DEMO_PASS', 'password')
    if creds.username == demo_user and creds.password == demo_pass:
        token = create_access_token({'sub': creds.username}, expires_delta=timedelta(minutes=60))
        return Token(access_token=token, token_type='bearer')
    raise HTTPException(status_code=401, detail='invalid credentials')
