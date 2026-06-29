# Edubirds

A lightweight FastAPI platform for delivering educational content to students in environments such as conflict zones where internet access is unreliable, restricted, or intermittently cut off.

> **Design principle:** First bytes matter more than pretty pixels. Optimized for 2G speeds, works offline where possible.

---

## Why This Exists

Standard edtech platforms assume stable high-speed broadband, CDNs, and modern browsers. That assumption breaks down in many regions affected by conflict.
This app strips away non-essential layers:
- **No JavaScript frameworks** (React, Vue, etc.) – only vanilla HTML/CSS/JS (~2KB total)
- **Text-first delivery** – Video is optional fallback only
- **Minimal dependencies** – Single Python process, one deployment command
- **Built-in admin UI** – Institutions can add courses without external tooling

---

## Key Features

| Feature | Benefit |
|---------|---------|
| Single-file inline UI | Loads instantly even on poor connections |
| Pydantic validation | Automatic input validation, clear error messages |
| Text-only fallback modes | Students can read materials even if video fails to load |
| Pagination support | Handles large course catalogs without bloating responses |
| CORS ready | Easy to integrate with other clients later |

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI + Uvicorn |
| Validation | Pydantic |
| Database | In-memory (switchable to SQLite) |
| Frontend | Vanilla HTML/CSS/JS (no build step) |
| Deployment | Docker-ready, single-process runtime |

---

## Quick Start

### Prerequisites

- Python 3.11+
- pip or poetry

### Installation

```bash
# Clone repository
git clone https://github.com/rastringer/edubirds.git
cd edubirds

# Install dependencies
pip install fastapi uvicorn pydantic-settings python-multipart

# Run development server
fastapi dev

# or
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
