from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from ..models.model import Comment, Post

from ..schemas.schemas_comment import CommentCreate, CommentResponse

from ..errors.model_error import AppExeption


async def create_comment(db: AsyncSession, user_id: int, comment: CommentCreate) -> CommentResponse:
    result = await db.execute(select(Post).where(Post.id==comment.post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise AppExeption(status_code=404, detail="Post not found", error_code="POST_NOT_FOUND")
    
    comment = Comment(
        text=comment.text, post_id=comment.post_id, user_id=user_id
    )
    
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    
    return CommentResponse.model_validate(comment)


async def get_comments(db: AsyncSession, post_id: int) -> list[CommentResponse]:
    result = await db.execute(select(Post).where(Post.id==post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise AppExeption(status_code=404, detail="Post not found")
    
    query = await db.execute(select(Comment).where(Comment.id==post_id))
    comments = query.scalars().all()
    return [CommentResponse.model_validate(comment) for comment in comments]
    