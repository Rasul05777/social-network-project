from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.core.config import settings 


async_engine = create_async_engine(url=settings.DB_URL, echo=True)

async_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


