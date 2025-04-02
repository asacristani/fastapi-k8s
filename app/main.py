import os
from contextlib import asynccontextmanager

import redis
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.database import init_db, mongo_client
from app.tasks import ping_task
from app.claims.routes import router as claims_router
from app.auth.routes import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(claims_router)
app.include_router(auth_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Insurance API",
        version="1.0.0",
        description="API with HTTP Bearer Auth",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
def read_root():
    return {"message": "Hello, world!"}


@app.get("/healthcheck")
async def healthcheck() -> dict:
    status = {"mongo": False, "redis": False, "celery": False}

    # Check MongoDB
    try:
        await mongo_client.admin.command("ping")
        status["mongo"] = True
    except Exception:
        pass

    # Check Redis
    try:
        r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379)
        r.ping()
        status["redis"] = True
    except Exception:
        pass

    # Check Celery
    try:
        res = ping_task.delay()
        status["celery"] = res is not None
    except Exception:
        pass

    status["status"] = "ok" if all(status.values()) else "error"
    return status
