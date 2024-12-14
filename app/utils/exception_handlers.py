from fastapi import Request
from fastapi.responses import JSONResponse
from .exceptions import CustomException

async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "statusCode": exc.status_code,
            "message": exc.message,
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "statusCode": 500,
            "message": f"Internal server error - {exc}",
        }
    )