from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict, Any, Literal
from datetime import datetime
import numpy as np

class SignalPoint(BaseModel):
    t: float  # seconds since start
    hr: Optional[float] = None  # bpm
    ibi: Optional[float] = None  # inter-beat interval ms

class Inference(BaseModel):
    state: str
    confidence: float = Field(ge=0.0, le=1.0)

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

class SynheartClient:
    """Minimal client with mock inference and ingestion support."""

    def infer(self, window: List[SignalPoint]) -> Inference:
        """Legacy inference method for backward compatibility"""
        hrs = np.array([p.hr for p in window if p.hr is not None])
        if len(hrs) < 5:
            return Inference(state="Unknown", confidence=0.3)
        var = np.var(hrs)
        if var < 4:
            return Inference(state="Calm", confidence=0.7)
        if var < 16:
            return Inference(state="Focused", confidence=0.6)
        return Inference(state="Stressed", confidence=0.8)

    def infer_from_batch(self, batch: IngestionBatch) -> Inference:
        """Infer emotional state from ingestion batch data"""
        # Extract heart rate data from batch
        heart_rate_stream = None
        for signal in batch.signals:
            if signal.stream == "heart_rate":
                heart_rate_stream = signal
                break
        
        if not heart_rate_stream:
            return Inference(state="Unknown", confidence=0.3)
        
        # Convert to legacy format for inference
        window = []
        for point in heart_rate_stream.points:
            if isinstance(point.v, (int, float)):
                window.append(SignalPoint(t=point.t, hr=point.v))
        
        return self.infer(window)

    def create_sample_batch(self, session_id: str = "550e8400-e29b-41d4-a716-446655440000") -> IngestionBatch:
        """Create a sample ingestion batch for testing"""
        from datetime import datetime, timezone
        
        return IngestionBatch(
            spec_version="0.1.0",
            session=Session(
                session_id=session_id,
                subject_id="anon_1234",
                consent_id="consent_v1",
                timezone="America/Vancouver",
                device=Device(
                    make="Apple",
                    model="Watch Series 9",
                    firmware_version="10.1"
                ),
                start_at=datetime.now(timezone.utc),
                end_at=datetime.now(timezone.utc)
            ),
            signals=[
                SignalStream(
                    stream="heart_rate",
                    unit="bpm",
                    sampling_hz=1,
                    points=[
                        SignalPointV1(t=i, v=70 + (i % 3))
                        for i in range(30)
                    ]
                ),
                SignalStream(
                    stream="ibi_ms",
                    unit="ms",
                    sampling_hz=1,
                    points=[
                        SignalPointV1(t=i, v=860 + (i % 5) * 10)
                        for i in range(30)
                    ]
                )
            ],
            events=[
                Event(
                    label="baseline",
                    t=0,
                    duration_s=30
                ),
                Event(
                    label="cognitive_task",
                    t=30,
                    duration_s=60,
                    properties={"task": "N-back", "level": 2}
                )
            ]
        )
