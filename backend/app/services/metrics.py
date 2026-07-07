from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

from .cleaning import convert_to_mpa, guess_column, unit_from_column_or_row


def parse_sample_repetition(name: str):
    base = Path(str(name)).stem.strip()
    base = re.sub(r"\s*\(\d+\)$", "", base)
    base = re.sub(r"\s+", " ", base)

    match = re.match(r"^(.*?)[_\s-]+(-?\d+)$", base)
    if match:
        sample = match.group(1).strip(" _-") or base
        return sample, int(match.group(2))

    return base, None


def detect_failure(clean):
    if clean.empty or len(clean) < 12:
        return None, "Insufficient fit region", ["Too few rows for detection."]

    stress = clean["Stress_MPa"].to_numpy()
    strain = clean["Strain"].to_numpy()

    peak_idx = int(np.nanargmax(stress))
    peak_stress = stress[peak_idx]
    peak_strain = strain[peak_idx]
    final_stress = stress[-1]
    max_strain = strain[-1]

    flags = []
    status = "Valid"
    failure_idx = None

    if peak_idx < len(stress) - 3 and peak_stress > 0:
        post = stress[peak_idx:]
        below = np.where(post <= 0.80 * peak_stress)[0]

        if len(below):
            candidate = peak_idx + int(below[0])
            if candidate > peak_idx:
                failure_idx = candidate

    early_end = max(8, int(len(stress) * 0.25))
    early = stress[:early_end]
    early_peak = float(np.max(early)) if len(early) else 0
    early_drops = np.diff(early)

    if early_peak > 0 and np.any(early_drops < -0.20 * early_peak):
        status = "Noisy curve"
        flags.append("Large early stress drop detected.")

    if max_strain > 0 and peak_strain < 0.35 * max_strain and peak_stress > 0:
        status = "Noisy curve" if status == "Valid" else status
        flags.append("Peak stress occurred unusually early in the strain range.")

    if failure_idx is not None:
        flags.append("Confirmed post-peak stress drop detected and cropped if enabled.")
    elif peak_stress > 0 and final_stress < 0.70 * peak_stress:
        flags.append("Post-peak decrease detected, but no stable crop point was found.")

    return failure_idx, status, flags


def validate_modulus(window):
    if len(window) < 5 or window["Strain"].nunique() < 2:
        return np.nan, np.nan, "Insufficient fit region"

    x = window["Strain"].to_numpy()
    y = window["Stress_MPa"].to_numpy()

    slope, intercept = np.polyfit(x, y, 1)
    pred = slope * x + intercept

    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan

    residual_noise = np.std(y - pred) / max(np.mean(y), 1e-9)

    if slope <= 0:
        status = "Negative modulus"
    elif np.isnan(r2) or r2 < 0.75:
        status = "Low R²"
    elif residual_noise > 0.35:
        status = "Noisy curve"
    else:
        status = "Valid"

    return float(slope), float(r2), status


def calculate_metrics(clean, modulus_min, modulus_max, data_kind="curve"):
    if clean.empty:
        return {
            "Maximum Load (N)": None,
            "Peak Stress (MPa)": None,
            "Strain at Peak": None,
            "Young's Modulus (MPa)": None,
            "Modulus R²": None,
            "Modulus Fit": "Insufficient fit region",
            "Area Under Curve": None,
            "Rows": 0,
        }

    if data_kind == "summary":
        modulus = pd.to_numeric(clean.get("Youngs_Modulus_MPa", pd.Series(dtype=float)), errors="coerce")
        auc = pd.to_numeric(clean.get("Area_Under_Curve", pd.Series(dtype=float)), errors="coerce")
        load = pd.to_numeric(clean.get("Maximum_Load_N", pd.Series(dtype=float)), errors="coerce")

        return {
            "Maximum Load (N)": float(load.mean()) if load.notna().any() else None,
            "Peak Stress (MPa)": float(clean["Stress_MPa"].mean()),
            "Strain at Peak": float(clean["Strain"].mean()),
            "Young's Modulus (MPa)": float(modulus.mean()) if modulus.notna().any() else None,
            "Modulus R²": None,
            "Modulus Fit": "Automatic results-table values",
            "Area Under Curve": float(auc.mean()) if auc.notna().any() else None,
            "Rows": int(len(clean)),
        }

    peak_idx = int(clean["Stress_MPa"].idxmax())
    window = clean[(clean["Strain"] >= modulus_min) & (clean["Strain"] <= modulus_max)].copy()

    modulus, r2, fit_status = validate_modulus(window)
    auc = float(np.trapezoid(clean["Stress_MPa"], clean["Strain"])) if len(clean) >= 2 else None

    return {
        "Maximum Load (N)": None,
        "Peak Stress (MPa)": float(clean.loc[peak_idx, "Stress_MPa"]),
        "Strain at Peak": float(clean.loc[peak_idx, "Strain"]),
        "Young's Modulus (MPa)": None if np.isnan(modulus) else modulus,
        "Modulus R²": None if np.isnan(r2) else r2,
        "Modulus Fit": fit_status,
        "Area Under Curve": auc,
        "Rows": int(len(clean)),
    }


def is_peak_summary(strain_col, stress_col):
    combined = f"{strain_col} {stress_col}".lower()
    return "maximum load" in combined or "at maximum" in combined


def prepare_peak_summary(name, df, strain_col, stress_col, units):
    unit = unit_from_column_or_row(stress_col, units)

    strain = pd.to_numeric(df[strain_col], errors="coerce")
    stress = convert_to_mpa(df[stress_col], unit)

    modulus_col = guess_column(df.columns, ["automatic young", "young", "modulus"], ["strain", "stress"])
    auc_col = guess_column(df.columns, ["area under curve", "area", "energy"], ["strain", "stress"])
    load_col = guess_column(df.columns, ["maximum load", "max load", "load"], ["strain", "stress"])

    excluded_columns = {strain_col, stress_col}
    excluded_columns.update(col for col in [modulus_col, auc_col, load_col] if col is not None)
    label_col = next((col for col in df.columns if col not in excluded_columns), None)

    if label_col is not None:
        labels = df[label_col].astype(str).str.strip()
    else:
        labels = pd.Series([str(i + 1) for i in range(len(df))], index=df.index)

    excluded = labels.str.contains(
        r"mean|standard deviation|std\.?|results table",
        case=False,
        regex=True,
        na=False,
    )

    modulus = (
        convert_to_mpa(df[modulus_col], unit_from_column_or_row(modulus_col, units))
        if modulus_col is not None
        else pd.Series(np.nan, index=df.index)
    )
    auc = pd.to_numeric(df[auc_col], errors="coerce") if auc_col is not None else pd.Series(np.nan, index=df.index)
    load = pd.to_numeric(df[load_col], errors="coerce") if load_col is not None else pd.Series(np.nan, index=df.index)

    clean = pd.DataFrame(
        {
            "Strain": strain,
            "Stress_Raw_MPa": stress,
            "Point_Label": labels,
            "Maximum_Load_N": load,
            "Youngs_Modulus_MPa": modulus,
            "Area_Under_Curve": auc,
        }
    )

    clean = clean[~excluded].replace([np.inf, -np.inf], np.nan).dropna(subset=["Strain", "Stress_Raw_MPa"])
    clean = clean[clean["Strain"] >= 0].reset_index(drop=True)

    clean["Stress_Corrected_MPa"] = clean["Stress_Raw_MPa"]
    clean["Stress_MPa"] = clean["Stress_Raw_MPa"]
    clean["Specimen"] = name
    clean["Data_Type"] = "summary"

    notes = [
        "Parsed as an Instron results table with one repetition per row.",
        "Existing mean and standard-deviation rows were excluded and recalculated from repetition rows.",
    ]

    if modulus_col is not None:
        notes.append(f"Imported automatic Young's modulus from `{modulus_col}`.")
    if auc_col is not None:
        notes.append(f"Imported area-under-curve values from `{auc_col}`.")
    if load_col is not None:
        notes.append(f"Imported maximum-load values from `{load_col}`.")

    return clean, unit, notes
