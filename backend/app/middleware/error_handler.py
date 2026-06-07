from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from slowapi.errors import RateLimitExceeded
from app.config.logger import logger

class AppException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code

def setup_exception_handlers(app: FastAPI):
    
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.warning("AppException raised", message=exc.message, status_code=exc.status_code, path=request.url.path)
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "error": {"message": exc.message, "code": exc.status_code}}
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.warning("HTTPException raised", detail=exc.detail, status_code=exc.status_code, path=request.url.path)
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "error": {"message": str(exc.detail), "code": exc.status_code}}
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning("Validation error", errors=exc.errors(), path=request.url.path)
        return JSONResponse(
            status_code=422,
            content={
                "success": False, 
                "error": {
                    "message": "Data validation failed", 
                    "code": 422, 
                    "details": exc.errors()
                }
            }
        )

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        logger.warning("Rate limit exceeded", path=request.url.path)
        return JSONResponse(
            status_code=429,
            content={"success": False, "error": {"message": "Rate limit exceeded. Please try again later.", "code": 429}}
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.error("Unhandled exception", exc_info=exc, path=request.url.path)
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": {"message": "Internal server error", "code": 500}}
        )
