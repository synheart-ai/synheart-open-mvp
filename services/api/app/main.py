from fastapi import FastAPI, HTTPException, Body
from .schemas import (
    SignalPoint, Inference, IngestionBatch, IngestionResponse,
    SignalStream, SignalPointV1
)
import json
from typing import List

app = FastAPI(
    title="Synheart API",
    description="Heart-driven intelligence API for biosignal ingestion and emotion inference",
    version="0.1.0"
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/infer", response_model=Inference)
def infer(window: list[SignalPoint]):
    """Legacy inference endpoint for backward compatibility"""
    hrs = [p.hr for p in window if p.hr is not None]
    if len(hrs) < 5:
        return Inference(state="Unknown", confidence=0.3)
    mean = sum(hrs) / len(hrs)
    var = sum((h - mean) ** 2 for h in hrs) / len(hrs)
    if var < 4:
        return Inference(state="Calm", confidence=0.7)
    if var < 16:
        return Inference(state="Focused", confidence=0.6)
    return Inference(state="Stressed", confidence=0.8)

@app.post("/ingest/batch", response_model=IngestionResponse)
def ingest_batch(batch: IngestionBatch):
    """Ingest biosignal data in batch format"""
    warnings = []
    total_points = 0
    
    # Validate and process each signal stream
    for signal in batch.signals:
        total_points += len(signal.points)
        
        # Validate heart rate range
        if signal.stream == "heart_rate":
            for point in signal.points:
                if isinstance(point.v, (int, float)) and (point.v < 30 or point.v > 220):
                    warnings.append(f"Heart rate {point.v} bpm outside normal range (30-220)")
        
        # Validate IBI range
        elif signal.stream == "ibi_ms":
            for point in signal.points:
                if isinstance(point.v, (int, float)) and (point.v < 300 or point.v > 3000):
                    warnings.append(f"IBI {point.v} ms outside normal range (300-3000)")
        
        # Validate HRV range
        elif signal.stream == "hrv_rmssd":
            for point in signal.points:
                if isinstance(point.v, (int, float)) and (point.v < 0 or point.v > 200):
                    warnings.append(f"HRV RMSSD {point.v} ms outside normal range (0-200)")
        
        # Validate accelerometer format
        elif signal.stream == "accelerometer":
            for point in signal.points:
                if isinstance(point.v, list) and len(point.v) != 3:
                    warnings.append(f"Accelerometer vector must have 3 components, got {len(point.v)}")
    
    return IngestionResponse(
        status="ok",
        session_id=batch.session.session_id,
        received_points=total_points,
        warnings=warnings
    )

@app.post("/ingest/jsonl", response_model=IngestionResponse)
def ingest_jsonl(data: str = Body(..., media_type="text/plain")):
    """Ingest biosignal data in JSONL format"""
    warnings = []
    total_points = 0
    session_id = None
    
    try:
        lines = data.strip().split('\n')
        for line_num, line in enumerate(lines, 1):
            if not line.strip():
                continue
            
            try:
                record = json.loads(line)
                total_points += 1
                
                if session_id is None:
                    session_id = record.get("session_id")
                
                # Basic validation
                if record.get("spec_version") != "0.1.0":
                    warnings.append(f"Line {line_num}: Invalid spec_version")
                
                if not record.get("subject_id", "").startswith("anon_"):
                    warnings.append(f"Line {line_num}: Subject ID must start with 'anon_'")
                
            except json.JSONDecodeError as e:
                warnings.append(f"Line {line_num}: Invalid JSON - {str(e)}")
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process JSONL: {str(e)}")
    
    if session_id is None:
        raise HTTPException(status_code=400, detail="No session_id found in JSONL data")
    
    return IngestionResponse(
        status="ok",
        session_id=session_id,
        received_points=total_points,
        warnings=warnings
    )

@app.get("/ingest/schema")
def get_schema():
    """Return JSON Schema for current ingestion format"""
    return {
        "spec_version": "0.1.0",
        "schema_url": "/schemas/ingest-batch.schema.json",
        "supported_streams": [
            "heart_rate", "ibi_ms", "hrv_rmssd", 
            "accelerometer", "resp_rate", "skin_temp_c"
        ],
        "validation_rules": {
            "heart_rate_range": "30-220 bpm",
            "ibi_range": "300-3000 ms",
            "hrv_rmssd_range": "0-200 ms",
            "subject_id_pattern": "anon_[a-zA-Z0-9]+",
            "accelerometer_format": "3-component vector [x, y, z]"
        }
    }
