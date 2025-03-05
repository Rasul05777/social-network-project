from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_service import get_current_user
from src.schemas.schemas_user import UserResponse
from src.schemas.schemas_post import PostCreate, PostResponse

from src.core.dependencies import get_db

from src.service.post_service import create_post, get_post_user_id, get_user_posts




router = APIRouter(
    prefix="/post",
    tags=["Posts"]
)


@router.post("/create", response_model=PostResponse, summary="Создание поста")
async def post_create(post_create: PostCreate, user_id: int, current: UserResponse=Depends(get_current_user), db: AsyncSession=Depends(get_db)):
    return await create_post(db, post_create, user_id)


@router.get("/{post_id}", response_model=PostResponse, summary="Нахождение поста по ID")
async def get_post_by_id(post_id: int, current: UserResponse=Depends(get_current_user), db: AsyncSession=Depends(get_db)):
    return await get_post_user_id(db, post_id)


@router.get("/{author_id}/posts", response_model=list[PostResponse], summary="Все посты пользователя")
async def get_all(author_id: int, current: UserResponse=Depends(get_current_user), db: AsyncSession=Depends(get_db)):
    return await get_user_posts(db, author_id)