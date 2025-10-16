import { infer, inferFromBatch, createSampleBatch } from "../dist/index.js";

// Legacy example (backward compatibility)
console.log("=== Legacy Inference ===");
const windowArr = Array.from({ length: 30 }, (_, i) => ({ t: i, hr: 70 + (i % 3) }));
console.log("Signal window:", windowArr.slice(0, 5), "...");
const legacyResult = infer(windowArr);
console.log("Legacy result:", legacyResult);

// New ingestion schema example
console.log("\n=== New Ingestion Schema ===");
const batch = createSampleBatch();
console.log(`Created batch with ${batch.signals.length} signal streams`);
console.log(`Session ID: ${batch.session.session_id}`);
console.log(`Subject ID: ${batch.session.subject_id}`);

// Infer from batch
const batchResult = inferFromBatch(batch);
console.log("Batch inference:", batchResult);

// Show signal details
batch.signals.forEach(signal => {
  console.log(`  ${signal.stream}: ${signal.points.length} points at ${signal.sampling_hz} Hz`);
});

// Show events
if (batch.events) {
  console.log(`Events: ${batch.events.length}`);
  batch.events.forEach(event => {
    console.log(`  ${event.label} at t=${event.t}s (duration: ${event.duration_s}s)`);
  });
}
