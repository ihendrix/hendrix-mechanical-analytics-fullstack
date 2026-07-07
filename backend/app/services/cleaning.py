from __future__ import annotations

import re

import numpy as np
import pandas as pd

try:
    from scipy.signal import savgol_filter
except Exception:
    savgol_filter = None


def extract_unit_row(df: pd.DataFrame):
    if df.empty:
        return df, {}

    first = df.iloc[0].astype(str).str.strip()
    numeric_ratio = pd.to_numeric(df.iloc[0], errors="coerce").notna().mean()

    has_units = first.str.contains(
        r"\(|\)|mpa|kpa|pa|mm/mm|%|n$",
        case=False,
        regex=True,
    ).mean() > 0.35

    if has_units and numeric_ratio < 0.45:
        units = {str(col): str(first.iloc[i]).strip("() ") for i, col in enumerate(df.columns)}
        return df.iloc[1:].reset_index(drop=True), units

    return df, {}


def guess_column(columns, include_terms, exclude_terms=None):
    exclude_terms = exclude_terms or []
    best = None
    best_score = -999

    for col in columns:
        low = str(col).lower()
        score = sum(term in low for term in include_terms) * 4
        score -= sum(term in low for term in exclude_terms) * 5

        if score > best_score:
            best = col
            best_score = score

    return best if best_score > 0 else None


def unit_from_column_or_row(col, units):
    text = f"{col} {units.get(col, '')}".lower()

    if "kpa" in text:
        return "kPa"
    if "mpa" in text:
        return "MPa"
    if re.search(r"\bpa\b", text):
        return "Pa"

    return "MPa"


def convert_to_mpa(series, source_unit):
    y = pd.to_numeric(series, errors="coerce")

    if source_unit == "kPa":
        return y / 1000.0
    if source_unit == "Pa":
        return y / 1_000_000.0

    return y


def smooth_series(values, method, window):
    y = values.astype(float).copy()
    window = max(3, int(window))

    if window % 2 == 0:
        window += 1

    if method == "None" or len(y) < 5:
        return y

    if method == "Moving average":
        return y.rolling(window=window, center=True, min_periods=1).mean()

    if method == "Savitzky-Golay" and savgol_filter is not None and len(y) >= window:
        return pd.Series(
            savgol_filter(y.to_numpy(), window_length=window, polyorder=2),
            index=y.index,
        )

    return y.rolling(window=window, center=True, min_periods=1).mean()


def clean_curve(df, strain_col, stress_col, units, smoothing, smooth_window, remove_outliers):
    unit = unit_from_column_or_row(stress_col, units)

    strain = pd.to_numeric(df[strain_col], errors="coerce")
    stress = convert_to_mpa(df[stress_col], unit)

    clean = (
        pd.DataFrame({"Strain": strain, "Stress_Raw_MPa": stress})
        .replace([np.inf, -np.inf], np.nan)
        .dropna()
    )

    clean = clean.sort_values("Strain").drop_duplicates("Strain").reset_index(drop=True)
    clean = clean[clean["Strain"] >= 0].copy()

    notes = []

    if clean.empty:
        return clean, unit, ["No numeric stress/strain rows detected."]

    n_base = max(5, int(len(clean) * 0.03))
    baseline = float(clean["Stress_Raw_MPa"].iloc[:n_base].median())

    clean["Stress_Corrected_MPa"] = clean["Stress_Raw_MPa"] - baseline
    notes.append(f"Baseline offset removed: {baseline:.5g} MPa")

    neg_count = int((clean["Stress_Corrected_MPa"] < 0).sum())
    clean["Stress_Corrected_MPa"] = clean["Stress_Corrected_MPa"].clip(lower=0)

    if neg_count:
        notes.append(f"Clipped {neg_count} negative stress points to zero.")

    if remove_outliers and len(clean) >= 15:
        median = clean["Stress_Corrected_MPa"].rolling(11, center=True, min_periods=1).median()
        resid = (clean["Stress_Corrected_MPa"] - median).abs()
        mad = float(np.nanmedian(np.abs(resid - np.nanmedian(resid))))
        threshold = max(0.03, 8 * mad)

        mask = resid <= threshold
        removed = int((~mask).sum())

        clean = clean[mask].reset_index(drop=True)

        if removed:
            notes.append(f"Removed {removed} spike/outlier points.")

    clean["Stress_MPa"] = smooth_series(
        clean["Stress_Corrected_MPa"],
        smoothing,
        smooth_window,
    ).clip(lower=0)

    if smoothing != "None":
        notes.append(f"Applied {smoothing.lower()} smoothing.")

    return clean, unit, notes
