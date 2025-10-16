from pydantic import BaseModel, Field
from typing import Optional, List, Union, Dict, Any, Literal
from datetime import datetime

class SignalPoint(BaseModel):
    t: float
    hr: Optional[float] = None
    ibi: Optional[float] = None

class Inference(BaseModel):
    state: str
    confidence: float

# New ingestion schema models
class Device(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    firmware_version: Optional[str] = None

class Session(BaseModel):
    session_id: str
    subject_id: str = Field(pattern=r"^anon_[a-zA-Z0-9]+$")
    consent_id: Optional[str] = None
    timezone: Optional[str] = None
    device: Optional[Device] = None
    start_at: datetime
    end_at: datetime

class SignalPointV1(BaseModel):
    t: float = Field(ge=0)
    v: Union[float, List[float]]

class SignalStream(BaseModel):
    stream: str = Field(pattern=r"^(heart_rate|ibi_ms|hrv_rmssd|accelerometer|resp_rate|skin_temp_c)$")
    unit: str = Field(pattern=r"^(bpm|ms|m/s\^2|breaths/min|°C)$")
    sampling_hz: float = Field(ge=0)
    points: List[SignalPointV1]

class Event(BaseModel):
    label: str
    t: float = Field(ge=0)
    duration_s: Optional[float] = Field(ge=0, default=None)
    properties: Optional[Dict[str, Any]] = None

class IngestionBatch(BaseModel):
    spec_version: Literal["0.1.0"] = "0.1.0"
    session: Session
    signals: List[SignalStream]
    events: Optional[List[Event]] = None

class IngestionResponse(BaseModel):
    status: str
    session_id: str
    received_points: int
    warnings: List[str] = []
