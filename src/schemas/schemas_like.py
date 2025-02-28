from pydantic import BaseModel

from datetime import datetime



class LikeCreate(BaseModel):
    post_id: int # ID Поста который лайкают
    
    class Config:
        json_schema_extra = {
            "example": {
                "post_id": 1
            }
        }
        

class LikeResponse(BaseModel):
    id: int
    user_id: int
    post_id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "post_id": 1
            }
        }