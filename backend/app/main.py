from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import api_router
from app.db.session import create_database_tables


def create_app() -> FastAPI:
    application = FastAPI(title="Nautix API", version="0.1.0")

    # CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    application.include_router(api_router)

    @application.on_event("startup")
    def on_startup() -> None:
        # Create tables automatically in dev; replace with Alembic in production
        create_database_tables()

    return application


app = create_app()

