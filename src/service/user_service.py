from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from ..models.model import User

from ..schemas.schemas_user import UserCreate, UserResponse

from ..core.utils import get_password_hash, create_token

from ..errors.model_error import AppExeption




async def create_user(db: AsyncSession, user_create: UserCreate) -> dict:
    existing_user = await db.execute(select(User).where((User.email==user_create.email)|(User.username==user_create.username)))
    result = existing_user.scalar()
    if result:
        if result.email == user_create.email:
            raise AppExeption(status_code=400, detail="Email already registred", error_code="DUPLICATE_EMALE")
        if result.username == user_create.username:
            raise AppExeption(status_code=400, detail="Username already registred", error_code="DUPLICATE_USERNAME")
    
    hashed_password = get_password_hash(user_create.password)
    
    user = User(
        username=user_create.username, 
        email=user_create.email,
        password=hashed_password
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    access_token = create_token(
        data={"sub": str(user.id)}
    )
    
    return { 
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user),
    }
async def get_user_by_id(db: AsyncSession, user_id: int) -> UserResponse:
    result = await db.execute(
        select(User)
        .options(selectinload(User.followers), selectinload(User.following))
        .filter(User.id==user_id)
    )
    
    user = result.scalar_one_or_none()

    if not user:
        raise AppExeption(
            status_code=404,
            detail="User not found",
            error_code="USER_NOT_FOUND"
        )
            
    followers_count = len(user.followers) if user.followers else 0
    following_count = len(user.following) if user.following else 0
    
    response = UserResponse.model_validate(user)
    response.followers_count = followers_count
    response.following_count = following_count
    return response   

 
async def get_user_by_name(db: AsyncSession, user_name: str) -> UserResponse:
    result = await db.execute(
        select(User)
        .options(selectinload(User.followers), selectinload(User.following))
        .filter(User.username==user_name)
    )
                                                
    user = result.scalar_one_or_none()

    if not user:
        raise AppExeption(
            status_code=404,
            detail="User not found",
            error_code="USER_NOT_FOUND"
        )
            
    followers_count = len(user.followers) if user.followers else 0
    following_count = len(user.following) if user.following else 0
    
    response = UserResponse.model_validate(user)
    response.followers_count = followers_count
    response.following_count = following_count
    return response