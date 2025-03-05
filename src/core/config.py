from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    DB_URL: str 
    DB_URL_ALEMBIC: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    
    class Config:
        env_file=".env"
        

settings = Settings()





        
        