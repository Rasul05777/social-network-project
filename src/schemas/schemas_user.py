from pydantic import BaseModel, EmailStr

from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john.doe@example.com",
                "password": "securepassword123",
            }
        }
    
    
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    followers_count: int | None=None
    following_count: int | None=None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "john_doe",
                "email": "john.doe@example.com",
                "created_at": "2025-02-25T12:00:00Z",
                "followers_count": 10,
                "following_count": 5
            }
        }
    