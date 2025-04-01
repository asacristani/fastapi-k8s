import os
from contextlib import asynccontextmanager

import redis
from fastapi import FastAPI

from app.database import init_db, mongo_client
from app.tasks import ping_task


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


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
