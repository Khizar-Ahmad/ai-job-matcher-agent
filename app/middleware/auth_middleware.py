from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from app.core.logger import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next
    ):

        logger.info(
            f"{request.method} {request.url.path}"
        )

        response = await call_next(request)

        return response