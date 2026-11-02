from src.config import MonitoringConfig
from fastapi import Depends, FastAPI
from src.auth import verify_api_key
from src.models import Telemetry
from src.services.monitoring_service import MonitoringService
import asyncio

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

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


async def monitoring_loop():
    while True:
        await asyncio.sleep(MonitoringConfig.MONITOR_INTERVAL_SECONDS)
        monitor.autonomous_check()


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(monitoring_loop())
