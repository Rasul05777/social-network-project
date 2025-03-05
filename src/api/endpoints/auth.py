from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.dependencies import get_db
from src.auth.auth_service import authenticate_user
from src.service.user_service import create_user
from src.schemas.schemas_user import UserCreate
from datetime import timedelta
from src.core.utils import create_token


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/token")
async def login(from_data: OAuth2PasswordRequestForm=Depends(), db: AsyncSession=Depends(get_db)):
    user = await authenticate_user(db, from_data.username, from_data.password)
    access_token = create_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", summary="Регистрация нового пользователя")
async def register(user: UserCreate, db: AsyncSession=Depends(get_db)):
    return await create_user(db, user)