from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_service import get_current_user
from src.schemas.schemas_user import UserResponse
from src.schemas.schemas_fllower import FllowerCreate, FollowResponse

from src.core.dependencies import get_db

from src.service.follow_service import get_followers, follow_user, unfollow_user





router = APIRouter(
    prefix="/follow",
    tags=["Follow"]
)


@router.post("/create", response_model=FollowResponse, summary="Создание подписки")
async def create_follow(follow: FllowerCreate, follower_id: int, current: UserResponse=Depends(get_current_user), db: AsyncSession=Depends(get_db)):
    return await follow_user(db, follow, follower_id)


@router.get("/{user_id}/followers", response_model=list[FollowResponse], summary="Получение всех подписок пользователя")
async def get_all_followers_by_id(user_id: int, current: UserResponse=Depends(get_current_user), db: AsyncSession=Depends(get_db)):
    return await get_followers(db, user_id)


@router.get("/remove/{followed_id}", summary="Удаление подписки")
async def remove_follow(follower_id: int, followed_id: int, current: UserResponse=Depends(get_current_user), db: AsyncSession=Depends(get_db)):
    return await unfollow_user(db, follower_id, followed_id)

