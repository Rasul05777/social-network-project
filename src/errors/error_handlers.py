from fastapi import Request
from fastapi.responses import JSONResponse

from .model_error import AppExeption



def error_handler():
    async def handler_app_excteption(request: Request, exc: AppExeption):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "message": exc.detail,
                "code": exc.error_code,
                "path": request.url.path
            }
        )
        
    return handler_app_excteption