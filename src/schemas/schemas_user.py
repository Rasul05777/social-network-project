from pydantic import BaseModel, EmailStr



class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    followers_count: int | None
    following_count: int | None
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john.doe@example.com",
                "password": "securepassword123",
                "followers_count": 10,
                "following_count": 5
            }
        }
    
    
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: str
    followers_count: int | None
    following_count: int | None
    
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