# Hendrix Mechanical Analytics Full-Stack

Hendrix Mechanical Analytics Full-Stack is a web-based mechanical testing analysis platform for processing stress–strain datasets through an interactive React frontend, FastAPI backend, and PostgreSQL database.

The platform allows researchers to upload mechanical-testing data, automatically clean stress–strain curves, calculate material properties, visualize results, and store analysis runs for reproducible review.

---

## Live Demo

**Application**

https://your-vercel-app.vercel.app

**API Documentation**

https://your-render-backend.onrender.com/docs

---

## Citation

Hendrix, I. (2026). *Hendrix Mechanical Analytics Full-Stack* (Version 1.0.0) [Computer software].

---

## Demo Data

Sample mechanical-testing datasets are included for demonstration purposes.

Supported formats:

- CSV
- TXT
- DAT
- TSV
- XLS
- XLSX
- ZIP

The included datasets are synthetic and do not contain proprietary research data.

---

## What It Does

Hendrix Mechanical Analytics provides an end-to-end workflow for mechanical-testing data analysis.

Users can upload one or more datasets, automatically detect stress and strain columns, clean experimental curves, calculate material properties, visualize stress–strain behavior, and review automated quality-control results through a web interface.

Each analysis is stored in a PostgreSQL database for reproducibility and future comparison.

---

## Key Features

### Data Processing

- Upload individual files or batch datasets
- Automatic stress/strain column detection
- Support for ZIP archives
- Batch analysis

### Data Cleaning

- Baseline offset correction
- Negative stress clipping
- Savitzky–Golay smoothing
- Moving-average smoothing
- Spike/outlier removal
- Failure-point detection
- Post-failure cropping

### Material Property Analysis

Automatically calculates:

- Maximum Load
- Peak Stress
- Strain at Peak
- Young's Modulus
- Modulus Fit (R²)
- Area Under the Curve

### Visualization

- Interactive Plotly stress–strain curves
- Multi-sample comparison
- Material-property summary tables
- Cleaning notes
- Analysis status flags

### Analysis Review

Automatically identifies datasets that may require inspection by evaluating data quality, modulus fit, and preprocessing results.

---

## Tech Stack

**Frontend**

- React
- TypeScript
- Vite
- Plotly.js

**Backend**

- FastAPI
- SQLAlchemy
- Pandas
- NumPy
- SciPy

**Database**

- PostgreSQL (Supabase)

**Deployment**

- Vercel
- Render
- GitHub

---

## Run Locally

Clone the repository

```bash
git clone https://github.com/ihendrix/hendrix-mechanical-analytics-fullstack.git
cd hendrix-mechanical-analytics-fullstack
```

Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Project Structure

```text
hendrix-mechanical-analytics-fullstack/
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── main.py
├── sample_data/
└── README.md
```

---

## Data Privacy

This repository does not include proprietary laboratory datasets or private research data. Users upload datasets locally through the web interface during runtime.

---

## Project Goal

The goal of Hendrix Mechanical Analytics Full-Stack is to provide a reusable, cloud-based platform for mechanical-testing data analysis that combines scientific computing, interactive visualization, and reproducible data management in a modern full-stack application.
