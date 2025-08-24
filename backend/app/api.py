# Standard library imports
from contextlib import asynccontextmanager

# Third-party imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

# Local imports
from app.core import db
from app.core.config import Settings, get_settings
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.events import router as events_router
from app.routers.sessions import router as sessions_router
from app.routers.speakers import router as speakers_router
from app.routers.registrations import router as registrations_router


def configure_middleware(app: FastAPI, settings: Settings) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS if settings.ENV != "dev" else ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(GZipMiddleware)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield


def configure_routers(app: FastAPI, settings: Settings) -> None:
    prefix = settings.API_V1_PREFIX

    app.include_router(auth_router, prefix=prefix)
    app.include_router(users_router, prefix=prefix)
    app.include_router(events_router, prefix=prefix)
    app.include_router(sessions_router, prefix=prefix)
    app.include_router(speakers_router, prefix=prefix)
    app.include_router(registrations_router, prefix=prefix)


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="Events API",
        description="API for my events",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.DOCS_ENABLED else None,
        redoc_url="/redoc" if settings.DOCS_ENABLED else None,
        openapi_url="/openapi.json" if settings.DOCS_ENABLED else None,
    )

    configure_middleware(app, settings=settings)
    configure_routers(app, settings=settings)

    return app
