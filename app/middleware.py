import traceback

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.database import SessionLocal
from app.models import ErrorLog


class ErrorLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        try:
            response = await call_next(request)
            return response

        except Exception as e:

            db = SessionLocal()

            try:
                error_log = ErrorLog(
                    endpoint=str(request.url.path),
                    http_method=request.method,
                    error_message=str(e),
                    stack_trace=traceback.format_exc()
                )

                db.add(error_log)
                db.commit()

            finally:
                db.close()

            raise e