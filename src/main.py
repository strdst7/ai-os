import asyncio
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
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
