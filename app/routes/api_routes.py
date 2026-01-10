# app/routes/api_routes.py
from fastapi import APIRouter, Depends
from app.models.schemas import UserCreate, SummaryRequest
# Import the specific functions from the file
from app.controller.authcontroller import signup_user, login_user, handle_summarization
from app.utils.auth import get_current_user

router = APIRouter()

@router.post("/auth/signup")
async def signup(user: UserCreate):
    return await signup_user(user)

@router.post("/auth/login")
async def login(user: UserCreate):
    return await login_user(user)

@router.post("/api/summarize")
async def summarize(req: SummaryRequest, current_user: dict = Depends(get_current_user)):
    return await handle_summarization(url=req.url, user_id=str(current_user["_id"]))