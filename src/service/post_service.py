from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from ..models.model import Post

from ..schemas.schemas_post import PostCreate, PostResponse

from ..errors.model_error import AppExeption




async def create_post(db: AsyncSession, post_create: PostCreate, user_id: int)-> PostResponse:
    post = Post(
        tittle=post_create.tittle,
        context=post_create.context,
        author_id=user_id
    )
    
    db.add(post)
    await db.commit()
    await db.refresh(post)
    
    return PostResponse.model_validate(post)


async def get_post_user_id(db: AsyncSession, post_id: int) -> PostResponse:
    query = await db.execute(select(Post).where(Post.id==post_id))
    post = query.scalar_one_or_none()
    if not post:
        raise AppExeption(status_code=404, detail="Post not found", error_code="POST_NOT_FOUND")
    
    return PostResponse.model_validate(post)


async def get_user_posts(db: AsyncSession, user_id) -> list[PostResponse]:
    query = await db.execute(select(Post).where(Post.author_id==user_id))
    posts = query.scalars().all()
    return [PostResponse.model_validate(post) for post in posts]
    
    