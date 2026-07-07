from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .cleaning import clean_curve, extract_unit_row, guess_column
from .metrics import (
    calculate_metrics,
    detect_failure,
    is_peak_summary,
    parse_sample_repetition,
    prepare_peak_summary,
)


@dataclass
class TestData:
    name: str
    raw: pd.DataFrame
    clean: pd.DataFrame
    strain_col: str | None
    stress_col: str | None
    stress_unit: str
    warnings: list[str]
    status: str
    data_kind: str


def prepare_test(
    name: str,
    df: pd.DataFrame,
    smoothing: str = "Savitzky-Golay",
    smooth_window: int = 17,
    remove_outliers: bool = True,
    crop_failure: bool = True,
) -> TestData:
    df, units = extract_unit_row(df)

    df = df.dropna(axis=1, how="all").copy()
    df.columns = [str(c).strip() for c in df.columns]

    columns = list(df.columns)

    strain_col = guess_column(
        columns,
        ["composite strain", "tensile strain", "strain", "mm/mm"],
        ["stress"],
    )

    stress_col = guess_column(
        columns,
        ["tensile stress", "stress", "mpa", "kpa"],
        ["strain"],
    )

    numeric_cols = [c for c in columns if pd.to_numeric(df[c], errors="coerce").notna().sum() >= 3]

    if strain_col is None and numeric_cols:
        strain_col = numeric_cols[0]

    if stress_col is None:
        stress_col = next((c for c in numeric_cols if c != strain_col), None)

    warnings = []
    unit = "MPa"
    clean = pd.DataFrame()
    status = "Insufficient fit region"
    data_kind = "curve"

    if strain_col and stress_col:
        if is_peak_summary(strain_col, stress_col):
            clean, unit, warnings = prepare_peak_summary(name, df, strain_col, stress_col, units)
            status = "Summary points"
            data_kind = "summary"
        else:
            clean, unit, warnings = clean_curve(
                df,
                strain_col,
                stress_col,
                units,
                smoothing,
                smooth_window,
                remove_outliers,
            )

            failure_idx, status, failure_notes = detect_failure(clean)
            warnings.extend(failure_notes)

            if crop_failure and failure_idx is not None and failure_idx > 5:
                clean = clean.iloc[: failure_idx + 1].copy()
                warnings.append("Curve cropped at confirmed failure point.")

            clean["Specimen"] = name
            clean["Point_Label"] = ""
            clean["Data_Type"] = "curve"
    else:
        warnings.append("Could not detect strain and stress columns.")

    return TestData(
        name=name,
        raw=df,
        clean=clean,
        strain_col=strain_col,
        stress_col=stress_col,
        stress_unit=unit,
        warnings=warnings,
        status=status,
        data_kind=data_kind,
    )


def _json_safe(value):
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    return value


def analyze_dataframe(
    name: str,
    df: pd.DataFrame,
    smoothing: str,
    smooth_window: int,
    remove_outliers: bool,
    crop_failure: bool,
    modulus_min: float,
    modulus_max: float,
) -> dict:
    test = prepare_test(
        name=name,
        df=df,
        smoothing=smoothing,
        smooth_window=smooth_window,
        remove_outliers=remove_outliers,
        crop_failure=crop_failure,
    )

    metrics = calculate_metrics(test.clean, modulus_min, modulus_max, test.data_kind)
    sample, _repetition = parse_sample_repetition(test.name)

    clean = test.clean.copy()
    clean = clean.replace([np.inf, -np.inf], np.nan)
    clean_data = [
        {key: _json_safe(value) for key, value in row.items()}
        for row in clean.to_dict(orient="records")
    ]

    return {
        "filename": test.name,
        "sample": sample,
        "detected_strain_column": test.strain_col,
        "detected_stress_column": test.stress_col,
        "data_type": test.data_kind,
        "status": test.status,
        "warnings": test.warnings,
        "metrics": {
            "maximum_load_n": _json_safe(metrics.get("Maximum Load (N)")),
            "peak_stress_mpa": _json_safe(metrics.get("Peak Stress (MPa)")),
            "strain_at_peak": _json_safe(metrics.get("Strain at Peak")),
            "youngs_modulus_mpa": _json_safe(metrics.get("Young's Modulus (MPa)")),
            "modulus_r2": _json_safe(metrics.get("Modulus R²")),
            "modulus_fit": _json_safe(metrics.get("Modulus Fit")),
            "area_under_curve": _json_safe(metrics.get("Area Under Curve")),
            "rows": int(metrics.get("Rows") or 0),
        },
        "clean_data": clean_data,
    }
