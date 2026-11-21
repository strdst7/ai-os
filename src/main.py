import asyncio
import sqlite3
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from src.auth import verify_api_key
from src.config import MonitoringConfig
from src.models import Telemetry
from src.services.monitoring_service import MonitoringService


async def monitoring_loop():
    while True:
        await asyncio.sleep(MonitoringConfig.MONITOR_INTERVAL_SECONDS)
        monitor.autonomous_check()


@asynccontextmanager
async def lifespan(app):
    task = asyncio.create_task(monitoring_loop())
    try:
        yield
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan)


@app.exception_handler(sqlite3.OperationalError)
def storage_error_handler(request: Request, exc: sqlite3.OperationalError):
    """Map storage failures to a structured, retryable response.

    A full disk or locked database is a transient capacity problem, not a bug
    in the request. Return 503 so operators and clients can distinguish it from
    an unexpected 500, and keep the SQLite message out of the response body.
    """
    message = str(exc)
    if "database or disk is full" in message:
        detail = "storage_full: the observation store has no free space"
    elif "database is locked" in message:
        detail = "storage_busy: the observation store is locked, retry shortly"
    elif "readonly" in message or "unable to open" in message:
        detail = "storage_unavailable: the observation store cannot be written"
    else:
        detail = "storage_error: the observation store failed, retry shortly"
    return JSONResponse(
        status_code=503,
        content={"detail": detail, "retryable": True},
        headers={"Retry-After": "5"},
    )


monitor = MonitoringService()


@app.get("/health")
def health():
    return {"status": "AI-OS running"}


@app.post("/agent/evaluate", dependencies=[Depends(verify_api_key)])
def agent_evaluate(metrics: Telemetry):
    return monitor.evaluate(metrics.model_dump(mode="json"))


@app.get("/observability", dependencies=[Depends(verify_api_key)])
def observability():
    return monitor.get_observability()
