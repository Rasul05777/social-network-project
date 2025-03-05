from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_service import get_current_user
from src.schemas.schemas_user import UserResponse
from src.schemas.schemas_like import LikeCreate, LikeResponse

from src.core.dependencies import get_db

from src.service.like_service import add_like, get_post_likes_count, remove_like





router = APIRouter(
    prefix="/like",
    tags=["Likes"]
)


@router.post("/create", response_model=LikeResponse, summary="Поставить лайк")
async def create_like(like: LikeCreate, user_id: int, current: UserResponse=Depends(get_current_user), db: AsyncSession=Depends(get_db)):
    return await add_like(db, like, user_id)


@router.get("/remove/{post_id}", summary="Удаление лайка")
async def delete_like( post_id:int, user_id: int, current: UserResponse=Depends(get_current_user), db: AsyncSession=Depends(get_db)):
    return await remove_like(db, post_id, user_id)


@router.get("/{post_id}/list/", response_model=int, summary="Все лайки на посте")
async def all_likes_post(post_id: int,current: UserResponse=Depends(get_current_user),  db: AsyncSession=Depends(get_db)):
    return await get_post_likes_count(db, post_id)

