import React from "react";

export function SignalCard({ title, value, state }: { title: string; value: string; state: string }) {
  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 12, padding: 16, maxWidth: 360 }}>
      <div style={{ fontSize: 12, opacity: 0.7 }}>{title}</div>
      <div style={{ fontSize: 28, fontWeight: 700 }}>{value}</div>
      <div style={{ marginTop: 8 }}>State: <strong>{state}</strong></div>
    </div>
  );
}
