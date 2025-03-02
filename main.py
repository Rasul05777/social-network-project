from fastapi import FastAPI

from src.api.endpoints.users import router as router_user
from src.api.endpoints.posts import router as router_post
from src.api.endpoints.comments import router as router_comment
from src.api.endpoints.likes import router as router_like



from src.errors.model_error import AppExeption
from src.errors.error_handlers import error_handler




app = FastAPI()

app.add_exception_handler(AppExeption, error_handler())

app.include_router(router_user)
app.include_router(router_post)
app.include_router(router_comment)
app.include_router(router_like)

