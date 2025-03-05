from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_service import get_current_user
from src.models.model import User

from src.schemas.schemas_user import UserResponse
from src.schemas.schemas_comment import CommentCreate, CommentResponse

from src.core.dependencies import get_db

from src.service.comment_service import create_comment, get_comments



router = APIRouter(
    prefix="/comment",
    tags=["Comments"]
)


@router.post("/create", response_model=CommentResponse, summary="Добавление комментария")
async def comment_create(comment: CommentCreate, user_id: int, current: UserResponse=Depends(get_current_user), db: AsyncSession=Depends(get_db), current_user: User = Depends(get_current_user)):
    return await create_comment(db, user_id, comment)


@router.get("/list/{user_id}", response_model=list[CommentResponse], summary="Все комментарии")
async def get_user_comments(post_id: int, current: UserResponse=Depends(get_current_user), db: AsyncSession=Depends(get_db),  current_user: User = Depends(get_current_user)):
    return await get_comments(db, post_id)