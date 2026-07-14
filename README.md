Hendrix Mechanical Analytics Full-Stack

Hendrix Mechanical Analytics Full-Stack is a cloud-based mechanical testing analysis platform for transforming raw stress–strain datasets into interactive visualizations, automated material-property calculations, quality-control review flags, and reproducible analysis records.

The platform is designed for engineering and research workflows where users need to analyze tensile-testing datasets, compare multiple samples, automatically clean experimental data, review material behavior, and preserve analysis history through a modern full-stack architecture.

Unlike the original Streamlit prototype, this application separates the frontend, backend, and database into a scalable web application that can be deployed entirely in the cloud.

Live Demo

Frontend

https://your-vercel-app.vercel.app

API Documentation

https://your-render-backend.onrender.com/docs

Citation

Hendrix, I. (2026). Hendrix Mechanical Analytics Full-Stack (Version 1.0.0) [Computer software].

Demo Data

Synthetic mechanical-testing datasets are included for testing.

Supported formats include:

CSV
TXT
DAT
TSV
XLS
XLSX
ZIP archives

The included datasets contain anonymized sample names and synthetic material behavior. They are provided solely for demonstration purposes and do not contain proprietary laboratory data.

What It Does

Hendrix Mechanical Analytics converts raw mechanical-testing exports into an interactive engineering analysis workflow.

Users can upload one or many tensile-testing datasets, automatically detect stress and strain columns, clean experimental curves, calculate material properties, visualize stress–strain behavior, review automated quality-control warnings, and store every analysis inside a PostgreSQL database for future comparison.

The platform also includes an automated research review layer that evaluates data quality, identifies questionable modulus calculations, detects noisy or incomplete curves, and flags datasets that require manual inspection.

Key Features
Data Upload
Upload CSV, TXT, DAT, TSV, XLS, XLSX, or ZIP datasets
Analyze single files or batch uploads
Automatically detect stress and strain columns
Expand ZIP archives into individual analyses
Preserve sample names throughout analysis
Data Cleaning

Automatically performs

Baseline offset correction
Negative stress clipping
Savitzky–Golay smoothing
Moving-average smoothing
Spike/outlier removal
Failure-point detection
Post-failure cropping

Cleaning operations are summarized for every uploaded sample.

Mechanical Analysis

Automatically calculates

Maximum Load
Peak Stress
Strain at Peak Stress
Young's Modulus
Modulus Fit (R²)
Area Under the Curve
Number of Data Points
Visualization

Display interactive Plotly dashboards showing

Stress–strain curves
Multiple sample overlays
Material-property summaries
Dataset statistics
Cleaning summaries
Quality-control status
Database

Every uploaded analysis is automatically stored in PostgreSQL.

Stored information includes

Filename
Sample name
Detected stress column
Detected strain column
Material metrics
Warnings
QA status
Cleaned dataset
Analysis timestamp

This creates a searchable and reproducible history of previous analyses.

Research Review Layer

The review layer is designed to make the platform more useful than a basic plotting dashboard.

It automatically

Detects poor modulus fits
Flags questionable Young's modulus calculations
Identifies noisy stress–strain curves
Detects excessive negative stress values
Detects abnormal failure behavior
Flags datasets requiring manual review
Separates review-worthy analyses from valid analyses
Produces cleaning summaries for every uploaded dataset

The review system is entirely metric-driven and does not rely on external AI services or API keys.

Analysis Metrics

Depending on the uploaded datasets, Hendrix Mechanical Analytics calculates

Maximum Load
Peak Stress
Strain at Peak
Young's Modulus
Modulus R²
Area Under Curve
Clean row count
Stress/strain column detection
Cleaning operations performed
QA review status

Metrics are calculated after automated preprocessing to reduce experimental artifacts and improve consistency across datasets.

Analysis Notes

Baseline stress offsets are automatically removed before analysis.

Negative stress values are clipped to zero.

Outlier spikes may be removed when enabled.

Savitzky–Golay smoothing and moving-average smoothing are optional.

Datasets with poor modulus fits or unusual behavior are labeled Needs Review rather than automatically rejected.

Automated review flags are intended to support engineering inspection and should not replace scientific judgment.

Full-Stack Architecture
React + TypeScript (Vite)
            │
            ▼
      FastAPI Backend
            │
            ▼
 SQLAlchemy + Python Analysis Engine
            │
            ▼
 PostgreSQL Database (Supabase)

Cloud Deployment

GitHub
Vercel
Render
Supabase PostgreSQL
Tech Stack
Frontend
React
TypeScript
Vite
Axios
Plotly.js
Backend
FastAPI
SQLAlchemy
Pandas
NumPy
SciPy
OpenPyXL
Database
PostgreSQL
Supabase
Cloud
GitHub
Vercel
Render
Run Locally

Clone the repository

git clone https://github.com/ihendrix/hendrix-mechanical-analytics-fullstack.git

cd hendrix-mechanical-analytics-fullstack
Backend
cd backend

python -m venv .venv

Windows

.venv\Scripts\activate

macOS/Linux

source .venv/bin/activate

Install dependencies

pip install -r requirements.txt

Run the API

uvicorn app.main:app --reload

Backend

http://localhost:8000

API Documentation

http://localhost:8000/docs
Frontend
cd frontend

npm install

npm run dev

Frontend

http://localhost:5173
Requirements
Backend
FastAPI
SQLAlchemy
Pandas
NumPy
SciPy
OpenPyXL
Uvicorn
Frontend
React
TypeScript
Vite
Axios
Plotly
Project Structure
hendrix-mechanical-analytics-fullstack
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── api.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── database.py
│   │   ├── models.py
│   │   └── main.py
│   └── requirements.txt
│
├── sample_data/
├── README.md
└── docker-compose.yml
Data Privacy

This repository does not include proprietary laboratory datasets or private research data.

Users upload datasets through the web interface during runtime.

Any included sample datasets are synthetic and anonymized.

Use Case

This platform was developed as a reusable engineering software application for mechanical-testing data analysis.

It supports tensile-testing workflows by automating stress–strain preprocessing, mechanical-property calculation, quality-control review, interactive visualization, cloud-based analysis storage, and reproducible engineering research.

Project Goal

The goal of Hendrix Mechanical Analytics Full-Stack is to move beyond desktop analysis software and spreadsheet-based workflows by providing a modern cloud-native platform for mechanical-testing analysis.

The project combines automated preprocessing, scientific computing, interactive visualization, database-backed analysis history, and scalable web deployment into a single reusable research application suitable for engineering laboratories, academic research, and materials science workflows.
