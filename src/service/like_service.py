from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from ..models.model import Comment, Post, Like

from ..schemas.schemas_like import LikeCreate, LikeResponse

from ..errors.model_error import AppExeption



async def add_like(db: AsyncSession, like: LikeCreate, user_id: int) -> LikeResponse:
    result = await db.execute(select(Post).where(Post.id == like.post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise AppExeption(status_code=404, detail="Post not found", error_code="POST_NOT_FOUND")
    
    result = await db.execute(select(Like).where(Like.user_id == user_id, Like.post_id == like.post_id))
    existing_like = result.scalar_one_or_none()
    if existing_like:
        raise AppExeption(status_code=400, detail="You already liked this post")

    like = Like(
        user_id=user_id,
        post_id=like.post_id
    )

    db.add(like)
    await db.commit()
    await db.refresh(like)
    
    return LikeResponse.model_validate(like)


async def remove_like(db: AsyncSession, post_id: int, user_id: int) -> None:
    result = await db.execute(select(Like).where(Like.user_id == user_id, Like.post_id == post_id))
    like = result.scalar_one_or_none()
    
    if not like:
        raise AppExeption(status_code=404, detail="Like not found", error_code="LIKE_NOT_FOUND")
    await db.delete(like)
    await db.commit()
    

async def get_post_likes_count(db: AsyncSession, post_id: int)  -> int:
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    
    if not post:
        raise AppExeption(status_code=404, detail="Post not found", error_code="POST_NOT_FOUND")
    query = await db.execute(select(Like).where(Like.post_id == post_id))
    return len(query.scalars().all())

