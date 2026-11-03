from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StrictFloat


class Telemetry(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    observation_id: UUID | None = None
    kpi_error: StrictFloat = Field(..., ge=0.0, le=1.0)
    embedding_shift: StrictFloat = Field(..., ge=0.0, le=1.0)
    retrieval_score: StrictFloat = Field(..., ge=0.0, le=1.0)
    latency_dev: StrictFloat = Field(..., ge=0.0, le=1.0)
