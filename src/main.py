from src.config import MonitoringConfig
from fastapi import FastAPI
from src.models import Telemetry
from src.services.monitoring_service import MonitoringService
import asyncio

app = FastAPI()

monitor = MonitoringService()


@app.get("/health")
def health():
    return {"status": "AI-OS running"}


@app.post("/agent/evaluate")
def agent_evaluate(metrics: Telemetry):
    return monitor.evaluate(metrics.dict())


@app.get("/observability")
def observability():
    return monitor.get_observability()


async def monitoring_loop():
    while True:
        await asyncio.sleep(MonitoringConfig.MONITOR_INTERVAL_SECONDS)
        monitor.autonomous_check()


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(monitoring_loop())
