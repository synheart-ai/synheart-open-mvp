# Synheart JavaScript SDK

A lightweight JavaScript/TypeScript client for collecting or simulating biosignals and performing mock emotional inference.

## Installation

```bash
npm install
npm run build
```

## Quick Start

```javascript
import { infer } from './dist/index.js';

// Create sample heart rate data
const window = Array.from({ length: 30 }, (_, i) => ({ 
  t: i, 
  hr: 70 + (i % 3) 
}));

// Perform inference
const result = infer(window);
console.log(`State: ${result.state}, Confidence: ${result.confidence}`);
```

## TypeScript Types

```typescript
type SignalPoint = { 
  t: number; 
  hr?: number; 
  ibi?: number; 
};

type Inference = {
  state: "Calm" | "Focused" | "Stressed" | "Unknown";
  confidence: number;
};
```

## API Reference

### infer(window: SignalPoint[]): Inference

Performs mock emotional inference on a window of biosignal data.

**Parameters:**
- `window`: Array of SignalPoint objects containing time and heart rate data

**Returns:**
- `Inference` object with state and confidence

## Mock Inference Logic

The current implementation uses heart rate variance analysis:
- Low variance (<4) → "Calm" (70% confidence)
- Medium variance (<16) → "Focused" (60% confidence)  
- High variance (≥16) → "Stressed" (80% confidence)
- Insufficient data (<5 points) → "Unknown" (30% confidence)

This is for educational purposes only and should not be used for medical or clinical applications.
