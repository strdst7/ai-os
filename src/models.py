from pydantic import BaseModel, Field


class Telemetry(BaseModel):
    kpi_error: float = Field(..., ge=0.0, le=1.0)
    embedding_shift: float = Field(..., ge=0.0, le=1.0)
    retrieval_score: float = Field(..., ge=0.0, le=1.0)
    latency_dev: float = Field(..., ge=0.0, le=1.0)
