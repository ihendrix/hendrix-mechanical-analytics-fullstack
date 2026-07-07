# Hendrix Mechanical Analytics Full-Stack

Hendrix Mechanical Analytics Full-Stack is a research software platform for mechanical-testing data analysis. The system uses a React frontend, FastAPI backend, PostgreSQL database, and Python analysis engine to upload stress-strain datasets, clean experimental data, calculate mechanical metrics, visualize results, and store analysis runs for reproducible review.

This repository expands the original Streamlit prototype into a deployable full-stack web application.

## What the application does

- Upload CSV, TXT, DAT, TSV, XLSX, XLS, or ZIP files containing mechanical-testing data.
- Detect likely stress and strain columns from experimental exports.
- Clean stress-strain curves by removing baseline offsets, clipping negative stress, optionally smoothing data, and detecting noisy regions.
- Calculate peak stress, strain at peak, Young's modulus, modulus fit quality, and area under the curve.
- Return analysis results through a FastAPI backend.
- Display stress-strain curves, metrics, warnings, and summary tables in a React dashboard.
- Store analysis runs in PostgreSQL for review and reproducibility.

## Architecture

```text
React + TypeScript frontend
        ↓
FastAPI backend API
        ↓
Python mechanical-analysis engine
        ↓
PostgreSQL database
```

## Repository structure

```text
hendrix-mechanical-analytics-fullstack/
  backend/
    app/
      main.py
      database.py
      models.py
      schemas.py
      routes/
      services/
  frontend/
    src/
      pages/
      components/
  sample_data/
  docker-compose.yml
  README.md
```

## Local setup

### 1. Start the backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at:

```text
http://localhost:8000
```

API docs:

```text
http://localhost:8000/docs
```

### 2. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

### 3. Optional: run PostgreSQL with Docker

```bash
docker compose up -d db
```

Then copy `.env.example` to `.env` and update values if needed.

## Main API endpoint

```text
POST /api/analyses/upload
```

Upload one or more files. The backend returns cleaned curve data, extracted metrics, warnings, detected columns, and saved analysis IDs.

## Positioning

This project is designed as a public-safe demonstration of full-stack research software for experimental data analysis. It shows how mechanical-testing workflows can be converted into reusable software systems that support data cleaning, automated metric extraction, visualization, QA review, and reproducible exports.

## Notes

This platform is intended for research workflow demonstration and portfolio review. It is not a substitute for final material validation, instrument calibration, or laboratory quality-control procedures.
