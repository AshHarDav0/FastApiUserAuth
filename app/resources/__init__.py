from fastapi import APIRouter
from app.resources import auth

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
