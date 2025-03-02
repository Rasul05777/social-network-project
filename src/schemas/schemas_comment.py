from pydantic import BaseModel, Field

from datetime import datetime





class CommentCreate(BaseModel):
    text: str = Field(..., min_length=1)
    post_id: int 
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Great post!",
                "post_id": 1
            }
        }
        

class CommentResponse(BaseModel):
    id: int
    text: str
    created_at: datetime
    user_id: int
    post_id: int
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "text": "Great post!",
                "created_at": "2025-02-25T12:05:00Z",
                "user_id": 1,
                "post_id": 1
            }
        }
        
