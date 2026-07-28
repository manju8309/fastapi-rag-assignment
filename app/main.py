from fastapi import FastAPI

from app.database import engine, Base
from app import models

from app.routes.auth_routes import router as auth_router
from app.routes.document_routes import router as document_router
from app.routes.chat_routes import router as chat_router

from app.middleware import ErrorLoggingMiddleware


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.add_middleware(ErrorLoggingMiddleware)


app.include_router(auth_router)
app.include_router(document_router)
app.include_router(chat_router)


@app.get("/")
def home():
    return {
        "message": "FastAPI RAG Assignment API is running"
    }