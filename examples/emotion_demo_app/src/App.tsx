import React, { useMemo } from "react";
import { SignalCard } from "./components/SignalCard";

export default function App() {
  const windowArr = useMemo(() => Array.from({ length: 30 }, (_, i) => ({ t: i, hr: 70 + (i % 3) })), []);
  const mean = windowArr.reduce((a, b) => a + (b.hr ?? 0), 0) / windowArr.length;
  const variance = windowArr.reduce((a, b) => a + Math.pow((b.hr ?? 0) - mean, 2), 0) / windowArr.length;
  const state = variance < 4 ? "Calm" : variance < 16 ? "Focused" : "Stressed";

  return (
    <div style={{ padding: 24, fontFamily: "system-ui" }}>
      <h1>Synheart Demo</h1>
      <p>Mock signal window visualized with naive state mapping.</p>
      <SignalCard title="Heart Rate" value={`${mean.toFixed(1)} bpm`} state={state} />
    </div>
  );
}
