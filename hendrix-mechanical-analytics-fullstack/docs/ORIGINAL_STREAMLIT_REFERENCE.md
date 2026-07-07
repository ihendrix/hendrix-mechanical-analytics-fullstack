# Original Streamlit reference

The full-stack version in this repository is adapted from the original Hendrix Mechanical Analytics Streamlit prototype.

The original prototype included:

- Multi-file upload and ZIP expansion
- Instron/Bluehill-style header detection
- Stress and strain column detection
- Unit handling for MPa, kPa, and Pa
- Baseline correction
- Optional spike/outlier removal
- Savitzky-Golay and moving-average smoothing
- Post-peak failure detection
- Young's modulus fitting
- Peak stress and strain metrics
- Area-under-curve calculation
- Repetition-level and sample-level summaries
- Plotly visualization
- CSV and HTML exports

This full-stack version moves the analysis logic into a FastAPI backend and uses a React dashboard for the user interface.
