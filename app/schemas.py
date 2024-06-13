from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, example="johndoe")
    password: str = Field(..., min_length=8, example="password123")
