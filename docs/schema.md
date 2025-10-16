# Schema

## Legacy Schema (v0.0)

**SignalPoint**: `{ t: number, hr?: number, ibi?: number }`

**Inference**: `{ state: Calm|Focused|Stressed|Unknown, confidence: 0..1 }`

## Ingestion Schema (v0.1.0)

### Batch Format
```json
{
  "spec_version": "0.1.0",
  "session": {
    "session_id": "uuid",
    "subject_id": "anon_1234",
    "consent_id": "consent_v1",
    "timezone": "America/Vancouver",
    "device": { "make": "Apple", "model": "Watch Series 9" },
    "start_at": "2025-10-15T19:00:00Z",
    "end_at": "2025-10-15T19:05:00Z"
  },
  "signals": [
    {
      "stream": "heart_rate",
      "unit": "bpm",
      "sampling_hz": 1,
      "points": [{ "t": 0, "v": 72 }]
    }
  ],
  "events": [
    { "label": "baseline", "t": 0, "duration_s": 30 }
  ]
}
```

### Supported Streams
- `heart_rate` (bpm)
- `ibi_ms` (inter-beat interval, ms)
- `hrv_rmssd` (ms)
- `accelerometer` (m/s², 3-component vector)
- `resp_rate` (breaths/min)
- `skin_temp_c` (°C)

### Validation Rules
- Heart rate: 30-220 bpm
- IBI: 300-3000 ms
- HRV RMSSD: 0-200 ms
- Subject ID: `anon_[a-zA-Z0-9]+`
- Accelerometer: 3-component vector `[x, y, z]`

Mappings in MVP are heuristic/educational only.
