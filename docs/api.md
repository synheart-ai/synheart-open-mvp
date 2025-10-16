# API

## Legacy Endpoints

`POST /infer` -> `Inference`

`GET /health` -> `{ status: "ok" }`

## Ingestion Endpoints (v0.1.0)

`POST /ingest/batch` -> `IngestionResponse`
- Accepts batch JSON format with session and signal data
- Validates data ranges and formats
- Returns status, session_id, received_points, and warnings

`POST /ingest/jsonl` -> `IngestionResponse`
- Accepts NDJSON stream format
- One record per line with session metadata
- Validates each line independently

`GET /ingest/schema` -> Schema Information
- Returns supported streams, validation rules, and schema URL
- Provides current spec version and format requirements

## Response Format

```json
{
  "status": "ok",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "received_points": 1720,
  "warnings": []
}
```
