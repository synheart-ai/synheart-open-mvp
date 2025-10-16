export type SignalPoint = { t: number; hr?: number; ibi?: number };

export type Inference = {
  state: "Calm" | "Focused" | "Stressed" | "Unknown";
  confidence: number;
};

// New ingestion schema types
export type Device = {
  make?: string;
  model?: string;
  firmware_version?: string;
};

export type Session = {
  session_id: string;
  subject_id: string; // Must match pattern: anon_[a-zA-Z0-9]+
  consent_id?: string;
  timezone?: string;
  device?: Device;
  start_at: string; // ISO datetime
  end_at: string; // ISO datetime
};

export type SignalPointV1 = {
  t: number; // >= 0
  v: number | number[]; // scalar or vector (for accelerometer)
};

export type SignalStream = {
  stream: "heart_rate" | "ibi_ms" | "hrv_rmssd" | "accelerometer" | "resp_rate" | "skin_temp_c";
  unit: "bpm" | "ms" | "m/s^2" | "breaths/min" | "°C";
  sampling_hz: number; // >= 0
  points: SignalPointV1[];
};

export type Event = {
  label: string;
  t: number; // >= 0
  duration_s?: number; // >= 0
  properties?: Record<string, any>;
};

export type IngestionBatch = {
  spec_version: "0.1.0";
  session: Session;
  signals: SignalStream[];
  events?: Event[];
};

export function infer(window: SignalPoint[]): Inference {
  const hrs = window.map(p => p.hr).filter((v): v is number => typeof v === "number");
  if (hrs.length < 5) return { state: "Unknown", confidence: 0.3 };
  const mean = hrs.reduce((a, b) => a + b, 0) / hrs.length;
  const variance = hrs.reduce((a, b) => a + (b - mean) ** 2, 0) / hrs.length;
  if (variance < 4) return { state: "Calm", confidence: 0.7 };
  if (variance < 16) return { state: "Focused", confidence: 0.6 };
  return { state: "Stressed", confidence: 0.8 };
}

export function inferFromBatch(batch: IngestionBatch): Inference {
  // Extract heart rate data from batch
  const heartRateStream = batch.signals.find(s => s.stream === "heart_rate");
  
  if (!heartRateStream) {
    return { state: "Unknown", confidence: 0.3 };
  }
  
  // Convert to legacy format for inference
  const window: SignalPoint[] = [];
  for (const point of heartRateStream.points) {
    if (typeof point.v === "number") {
      window.push({ t: point.t, hr: point.v });
    }
  }
  
  return infer(window);
}

export function createSampleBatch(sessionId: string = "550e8400-e29b-41d4-a716-446655440000"): IngestionBatch {
  const now = new Date().toISOString();
  
  return {
    spec_version: "0.1.0",
    session: {
      session_id: sessionId,
      subject_id: "anon_1234",
      consent_id: "consent_v1",
      timezone: "America/Vancouver",
      device: {
        make: "Apple",
        model: "Watch Series 9",
        firmware_version: "10.1"
      },
      start_at: now,
      end_at: now
    },
    signals: [
      {
        stream: "heart_rate",
        unit: "bpm",
        sampling_hz: 1,
        points: Array.from({ length: 30 }, (_, i) => ({
          t: i,
          v: 70 + (i % 3)
        }))
      },
      {
        stream: "ibi_ms",
        unit: "ms",
        sampling_hz: 1,
        points: Array.from({ length: 30 }, (_, i) => ({
          t: i,
          v: 860 + (i % 5) * 10
        }))
      }
    ],
    events: [
      {
        label: "baseline",
        t: 0,
        duration_s: 30
      },
      {
        label: "cognitive_task",
        t: 30,
        duration_s: 60,
        properties: { task: "N-back", level: 2 }
      }
    ]
  };
}
