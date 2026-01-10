from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr

class SummaryRequest(BaseModel):
    url: str

class SummaryResponse(BaseModel):
    url: str
    summary: str