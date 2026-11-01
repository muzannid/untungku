import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.database import Base, check_database_connection, engine
from .models import models  # noqa: F401  -- imported so SQLAlchemy registers the tables

logger = logging.getLogger("untungku")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create missing tables on startup. A database outage must not stop the API
    # from booting (the health endpoint will report the problem instead).
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified.")
    except Exception:
        logger.exception("Could not initialise the database schema.")

    yield

    engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "docs": "/docs",
    }


@app.get(f"{settings.API_V1_STR}/health")
def health_check():
    database_ok = check_database_connection()
    return {
        "status": "healthy" if database_ok else "degraded",
        "database": "connected" if database_ok else "disconnected",
        "environment": settings.ENVIRONMENT,
        "version": settings.VERSION,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
