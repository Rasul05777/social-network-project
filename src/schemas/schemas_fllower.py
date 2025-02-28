from pydantic import BaseModel

from datetime import datetime



class FllowerCreate(BaseModel):
    followed_id: int # ID Пользователя на которого подписываются    
    
    class Config:
        json_schema_extra = {
            "example": {
                "followed_id": 2
            }
        }
        

class FollowResponse(BaseModel):
    id: int
    follower_id: int  # Кто подписался
    followed_id: int  # На кого подписались
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "follower_id": 1,
                "followed_id": 2
            }
        }
        
