from fastapi import HTTPException
from typing import Optional, Any

class CustomException(HTTPException):
    def __init__(
        self,
        status_code: int,
        message: str,
        error: Optional[Any] = None
    ) -> None:
        self.status_code = status_code
        self.message = message
        self.error = error
        super().__init__(status_code=status_code, detail=message)