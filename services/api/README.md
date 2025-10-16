# Synheart API Service

A FastAPI reference implementation demonstrating how apps can send biosignal data and receive emotion states.

## Installation

```bash
pip install -e .
```

## Running the Service

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

### POST /infer
Perform emotional inference on biosignal data.

**Request Body:**
```json
[
  {"t": 0, "hr": 70},
  {"t": 1, "hr": 71},
  {"t": 2, "hr": 72}
]
```

**Response:**
```json
{
  "state": "Calm",
  "confidence": 0.7
}
```

## Data Schemas

### SignalPoint
```python
class SignalPoint(BaseModel):
    t: float          # seconds since start
    hr: Optional[float] = None  # heart rate in bpm
    ibi: Optional[float] = None  # inter-beat interval in ms
```

### Inference
```python
class Inference(BaseModel):
    state: str        # "Calm", "Focused", "Stressed", or "Unknown"
    confidence: float  # 0.0 to 1.0
```

## Mock Inference Logic

The current implementation uses heart rate variance analysis:
- Low variance (<4) → "Calm" (70% confidence)
- Medium variance (<16) → "Focused" (60% confidence)  
- High variance (≥16) → "Stressed" (80% confidence)
- Insufficient data (<5 points) → "Unknown" (30% confidence)

This is for educational purposes only and should not be used for medical or clinical applications.
