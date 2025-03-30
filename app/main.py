from fastapi import FastAPI, Depends
from sqlalchemy import text
from app.database import get_db
from app.tasks import ping_task
import redis
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

@app.get("/healthcheck")
def healthcheck(db=Depends(get_db)) -> dict:
    status = {
        "postgres": False,
        "redis": False,
        "celery": False
    }

    # Check DB
    try:
        db.execute(text("SELECT 1"))
        status["postgres"] = True
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
