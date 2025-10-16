# Overview

The Synheart Open MVP is a public, minimal stack to explore affective computing over biosignals. This repository provides the foundational framework for building emotion-aware applications with standardized, validated biosignal data ingestion.

## 🌍 Synheart Atlas

For comprehensive documentation, project updates, and research insights, visit the **Synheart Atlas** - our public knowledge base:

**🔗 [Synheart Atlas](https://atlas.synheart.ai)**

The Atlas contains:
- 🧩 **Product briefs** and MVP updates
- 🧠 **Research papers & experiments**  
- ⚙️ **Technical architecture & SDK docs**
- 💬 **Press, partnerships, and open data releases**

## 💓 What is Synheart?

Synheart infuses emotional awareness into artificial intelligence — merging human biosignals with neural networks to create **adaptive, heart-aware systems**. We build technology that senses how people actually feel and helps AI respond more humanly.

## 🎯 Open MVP Purpose

This repository provides the **"framework layer"** — the public foundation developers and researchers can build on:

### ✅ What's Open
- **SDKs (Python + JS)** — lightweight clients for biosignal collection and mock emotional inference
- **API Service (FastAPI)** — reference implementation for biosignal processing
- **Example UI (React + Vite)** — demo visualization of heart-driven intelligence
- **Schema & Documentation** — standardized definitions for signals, states, and feature mappings

### 🔒 What Stays Private
- Real biosignal datasets collected from wearables
- Fine-tuned models and internal inference engine
- Production infrastructure and pipelines
- Proprietary emotion-mapping algorithms

## 🧭 Philosophy

Synheart believes emotional intelligence in AI should be **transparent, ethical, and co-created**. By open-sourcing the foundational framework—but keeping sensitive data closed—we invite the world to help define the language between **the human heart and artificial intelligence**.

## 📊 Ingestion Schema v0.1.0

The MVP includes a **production-ready ingestion schema** that standardizes biosignal data collection:

- **Supported Signals**: heart_rate, ibi_ms, hrv_rmssd, accelerometer, resp_rate, skin_temp_c
- **Data Formats**: Batch JSON, JSONL, CSV with full validation
- **Privacy-First**: Anonymous subject IDs (`anon_xxx` pattern), consent tracking
- **Validation**: Range validation for physiological signals, format validation for vectors

## 🎨 Emotion Demo App

The React + Vite demo app demonstrates the "hello world" of heart-driven intelligence:

- **Heart Rate Visualization**: Generates 30 synthetic data points (70-72 bpm)
- **Emotional State Inference**: Uses variance-based classification (Calm/Focused/Stressed)
- **Clean UI**: Modern interface with SignalCard component
- **Performance**: 46.4 kB gzipped build size

## 🚀 Quick Start

```bash
# Python SDK
cd sdk/python && pip install -e . && python examples/quickstart.py

# JavaScript SDK  
cd sdk/js && npm install && npm run build && node examples/quickstart.mjs

# API Service
cd services/api && pip install -e . && uvicorn app.main:app --host 0.0.0.0 --port 8000

# Demo App
cd examples/emotion_demo_app && npm install && npm run dev
```

## 🤝 Who It's For

- **Researchers** exploring affective computing and human-AI interaction
- **Developers** building with the Synheart SDK
- **Educators** teaching biosignal processing and emotion-aware AI
- **Curious readers** who believe the next intelligence starts with the heart

## 🔐 Transparency & Values

We believe in **ethical AI**, **data privacy**, and **open collaboration**. Our models are designed to respect user consent, process signals privately, and advance the science of emotion-aware AI responsibly.

## 📫 Contact

Have a question or want to collaborate?

- ✉️ **hi@synheart.ai**
- 🌐 [synheart.ai](https://synheart.ai/)
- 📚 [Synheart Atlas](https://atlas.synheart.ai)

---

*This overview provides a high-level introduction. For detailed technical documentation, see the [API docs](api.md), [Schema docs](schema.md), and the comprehensive [Synheart Atlas](https://atlas.synheart.ai).*
