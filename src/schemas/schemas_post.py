from pydantic import BaseModel, Field

from datetime import datetime

from src.schemas.schemas_user import UserResponse



class PostCreate(BaseModel):
    tittle: str | None
    context: str = Field(..., min_length=1)
    
    class Config:
            json_schema_extra = {
                "example": {
                    "tittle": "My First Post",
                    "context": "This is the content of my post."
                }
            }        
            
    
class PostResponse(BaseModel):
    id: int
    tittle: str | None
    context: str
    created_at: datetime
    author_id: int 
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "tittle": "My First Post",
                "context": "This is the content of my post.",
                "created_at": "2025-02-25T12:00:00Z",
            }
        }
        
