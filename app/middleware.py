import traceback

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.database import SessionLocal
from app.models import ErrorLog


class ErrorLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        try:
            response = await call_next(request)
            return response

        except Exception as e:

            # Get authenticated user ID if available
            user_id = getattr(
                request.state,
                "user_id",
                None
            )

            # Get complete stack trace
            stack_trace = traceback.format_exc()

            # Save error information to PostgreSQL
            db = SessionLocal()

            try:
                error_log = ErrorLog(
                    endpoint=str(request.url.path),
                    http_method=request.method,
                    error_message=str(e),
                    stack_trace=stack_trace,
                    user_id=user_id
                )

                db.add(error_log)
                db.commit()

            except Exception:
                # Avoid a database logging failure
                # from causing another unhandled exception
                db.rollback()

            finally:
                db.close()

            # Return a proper JSON error response
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": "Internal server error",
                    "detail": "An unexpected error occurred while processing the request."
                }
            )