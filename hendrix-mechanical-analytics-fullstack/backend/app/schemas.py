from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class AnalysisSettings(BaseModel):
    smoothing: str = "Savitzky-Golay"
    smooth_window: int = 17
    remove_outliers: bool = True
    crop_failure: bool = True
    modulus_min: float = 0.005
    modulus_max: float = 0.080


class MetricSummary(BaseModel):
    maximum_load_n: float | None = None
    peak_stress_mpa: float | None = None
    strain_at_peak: float | None = None
    youngs_modulus_mpa: float | None = None
    modulus_r2: float | None = None
    modulus_fit: str | None = None
    area_under_curve: float | None = None
    rows: int = 0


class AnalysisResult(BaseModel):
    id: int | None = None
    filename: str
    sample: str | None = None
    detected_strain_column: str | None = None
    detected_stress_column: str | None = None
    data_type: str
    status: str
    warnings: list[str]
    metrics: MetricSummary
    clean_data: list[dict]


class AnalysisRunRead(BaseModel):
    id: int
    filename: str
    sample: str | None = None
    detected_strain_column: str | None = None
    detected_stress_column: str | None = None
    data_type: str
    status: str
    peak_stress_mpa: float | None = None
    youngs_modulus_mpa: float | None = None
    modulus_r2: float | None = None
    rows: int
    created_at: datetime

    class Config:
        from_attributes = True
