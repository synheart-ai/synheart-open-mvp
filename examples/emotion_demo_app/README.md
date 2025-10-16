# Synheart Emotion Demo App

A React + Vite visualization that turns heart rate data into color-coded emotional feedback.

## Installation

```bash
npm install
```

## Development

```bash
npm run dev
```

## Build

```bash
npm run build
```

## Preview

```bash
npm run preview
```

## Features

- **Real-time Visualization**: Displays synthetic heart rate data
- **Emotional State Mapping**: Shows inferred emotional states (Calm, Focused, Stressed)
- **Interactive UI**: Clean, modern interface built with React
- **Educational Purpose**: Demonstrates the "hello world" of heart-driven intelligence

## Components

### App.tsx
Main application component that generates sample data and performs inference.

### SignalCard.tsx
Reusable component for displaying signal information with emotional state.

## Mock Data

The app generates synthetic heart rate data:
```javascript
const windowArr = Array.from({ length: 30 }, (_, i) => ({ 
  t: i, 
  hr: 70 + (i % 3) 
}));
```

## Emotional State Logic

Based on heart rate variance:
- Low variance (<4) → "Calm"
- Medium variance (<16) → "Focused"  
- High variance (≥16) → "Stressed"

This is for educational purposes only and should not be used for medical or clinical applications.
