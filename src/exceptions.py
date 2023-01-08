import logging

from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


class BaseHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str) -> None:
        detail_message = detail or "Error"
        super().__init__(
            status_code=status_code,
            detail=detail_message,
        )
        logger.error(detail_message)


class BadRequestHTTPException(BaseHTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class InternalErrorHTTPException(BaseHTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)
