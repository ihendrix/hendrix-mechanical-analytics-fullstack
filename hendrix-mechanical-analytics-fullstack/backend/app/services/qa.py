from __future__ import annotations


def result_needs_review(result: dict) -> bool:
    metrics = result.get("metrics", {})
    fit = metrics.get("modulus_fit")
    warnings = result.get("warnings", [])

    if result.get("status") != "Valid":
        return True
    if fit and fit != "Valid":
        return True
    if metrics.get("youngs_modulus_mpa") is None:
        return True
    if metrics.get("peak_stress_mpa") is None:
        return True
    if warnings:
        return True

    return False
