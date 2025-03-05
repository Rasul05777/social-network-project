from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from ..models.model import Follow, User

from ..schemas.schemas_fllower import FollowResponse, FllowerCreate

from ..errors.model_error import AppExeption





async def follow_user(db: AsyncSession, follow: FllowerCreate, follower_id: int) -> FollowResponse:
    if follower_id == follow.followed_id:
        raise AppExeption(status_code=400, detail="Cannot follow yourself", error_code="FOLLOW_YOURSELF")
    
    followed = await db.execute(select(User).where(User.id == follow.followed_id))
    result = followed.scalar_one_or_none()
    if not result:
        raise AppExeption(status_code=404, detail="User not found", error_code="USER_NOT_FOUND")
    
    existing_follow = await db.execute(select(Follow).where(Follow.follower_id==follower_id))
    result = existing_follow.scalar_one_or_none()
    if result:
        raise AppExeption(status_code=400, detail="Already following this user", error_code="ALREADY_FOLLOWING")
    
    db_follow = Follow(follower_id=follower_id, followed_id=follow.followed_id)
    
    db.add(db_follow)
    await db.commit()
    await db.refresh(db_follow)
    
    return FollowResponse.model_validate(db_follow)


async def unfollow_user(db: AsyncSession, follower_id:int, followed_id: int) -> dict:
    result = await db.execute(select(Follow).where(Follow.followed_id==followed_id, Follow.follower_id==follower_id))
    follow = result.scalar_one_or_none()
    if not follow:
        raise AppExeption(status_code=404, detail="Follow not found", error_code="FOLLOW_NOT_FOUND")
    
    await db.delete(follow)
    await db.commit()
    return {"status": "success", "message": "Successfully unfollowed user"}
    
    
async def get_followers(db: AsyncSession, user_id: int) -> list[FollowResponse]:
    result = await db.execute(select(Follow).where(Follow.followed_id==user_id))
    followers = result.scalars().all()
    return [FollowResponse.model_validate(follow) for follow in followers]