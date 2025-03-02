from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.schemas_user import UserResponse, UserCreate

from src.core.dependencies import get_db

from src.service.user_service import create_user, get_user_by_id, get_user_by_name



router = APIRouter(
    prefix="/user",
    tags=["Users"]
)


@router.post("/create", response_model=UserResponse, summary="Добавление пользователя")
async def create_new_user(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user_create)


@router.get("/id/{user_id}", response_model=UserResponse, summary="Нахождение пользователя по ID")
async def get_user_id(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_user_by_id(db, user_id)


@router.get("/name/{user_name}", response_model=UserResponse, summary="Нахождение пользователя по имени")
async def get_user_name(user_name: str, db: AsyncSession = Depends(get_db)):
    return await get_user_by_name(db, user_name)

