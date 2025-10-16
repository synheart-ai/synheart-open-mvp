# Synheart Python SDK

A lightweight Python client for collecting or simulating biosignals and performing mock emotional inference.

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from synheart.client import SynheartClient, SignalPoint

# Create client
client = SynheartClient()

# Create sample heart rate data
window = [SignalPoint(t=i, hr=70 + (i % 3)) for i in range(30)]

# Perform inference
result = client.infer(window)
print(f"State: {result.state}, Confidence: {result.confidence}")
```

## API Reference

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

### SynheartClient
```python
client = SynheartClient()
result = client.infer(window: List[SignalPoint]) -> Inference
```

## Mock Inference Logic

The current implementation uses heart rate variance analysis:
- Low variance (<4) → "Calm" (70% confidence)
- Medium variance (<16) → "Focused" (60% confidence)  
- High variance (≥16) → "Stressed" (80% confidence)
- Insufficient data (<5 points) → "Unknown" (30% confidence)

This is for educational purposes only and should not be used for medical or clinical applications.
