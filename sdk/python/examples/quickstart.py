from synheart.client import SynheartClient, SignalPoint, IngestionBatch

# Create client
client = SynheartClient()

# Legacy example (backward compatibility)
print("=== Legacy Inference ===")
window = [SignalPoint(t=i, hr=70 + (i % 3)) for i in range(30)]
result = client.infer(window)
print(f"Legacy result: {result.state} (confidence: {result.confidence})")

# New ingestion schema example
print("\n=== New Ingestion Schema ===")
batch = client.create_sample_batch()
print(f"Created batch with {len(batch.signals)} signal streams")
print(f"Session ID: {batch.session.session_id}")
print(f"Subject ID: {batch.session.subject_id}")

# Infer from batch
batch_result = client.infer_from_batch(batch)
print(f"Batch inference: {batch_result.state} (confidence: {batch_result.confidence})")

# Show signal details
for signal in batch.signals:
    print(f"  {signal.stream}: {len(signal.points)} points at {signal.sampling_hz} Hz")

# Show events
if batch.events:
    print(f"Events: {len(batch.events)}")
    for event in batch.events:
        print(f"  {event.label} at t={event.t}s (duration: {event.duration_s}s)")
