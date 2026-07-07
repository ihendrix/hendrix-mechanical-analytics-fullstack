from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class AnalysisRun(Base):
    __tablename__ = "analysis_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String(255), index=True)
    sample: Mapped[str | None] = mapped_column(String(255), nullable=True)
    detected_strain_column: Mapped[str | None] = mapped_column(String(255), nullable=True)
    detected_stress_column: Mapped[str | None] = mapped_column(String(255), nullable=True)
    data_type: Mapped[str] = mapped_column(String(50), default="curve")
    status: Mapped[str] = mapped_column(String(100), default="Valid")

    maximum_load_n: Mapped[float | None] = mapped_column(Float, nullable=True)
    peak_stress_mpa: Mapped[float | None] = mapped_column(Float, nullable=True)
    strain_at_peak: Mapped[float | None] = mapped_column(Float, nullable=True)
    youngs_modulus_mpa: Mapped[float | None] = mapped_column(Float, nullable=True)
    modulus_r2: Mapped[float | None] = mapped_column(Float, nullable=True)
    area_under_curve: Mapped[float | None] = mapped_column(Float, nullable=True)
    rows: Mapped[int] = mapped_column(Integer, default=0)

    warnings: Mapped[list[str]] = mapped_column(JSON, default=list)
    clean_data: Mapped[list[dict]] = mapped_column(JSON, default=list)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
