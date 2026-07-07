from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import AnalysisRun
from ..schemas import AnalysisRunRead
from ..services.analysis_engine import analyze_dataframe
from ..services.parser import iter_uploaded_payloads, read_file_bytes, safe_name
from ..services.qa import result_needs_review

router = APIRouter(prefix="/api/analyses", tags=["analyses"])


@router.get("/", response_model=list[AnalysisRunRead])
def list_analyses(db: Session = Depends(get_db)):
    return db.query(AnalysisRun).order_by(AnalysisRun.created_at.desc()).limit(50).all()


@router.post("/upload")
async def upload_and_analyze(
    files: list[UploadFile] = File(...),
    smoothing: str = Form("Savitzky-Golay"),
    smooth_window: int = Form(17),
    remove_outliers: bool = Form(True),
    crop_failure: bool = Form(True),
    modulus_min: float = Form(0.005),
    modulus_max: float = Form(0.080),
    db: Session = Depends(get_db),
):
    payloads = [(file.filename or "uploaded_file", await file.read()) for file in files]
    expanded_payloads = list(iter_uploaded_payloads(payloads))

    results = []

    for filename, data in expanded_payloads:
        display_name = safe_name(filename)
        raw = read_file_bytes(filename, data)

        result = analyze_dataframe(
            name=display_name,
            df=raw,
            smoothing=smoothing,
            smooth_window=smooth_window,
            remove_outliers=remove_outliers,
            crop_failure=crop_failure,
            modulus_min=modulus_min,
            modulus_max=modulus_max,
        )

        if result_needs_review(result) and result["status"] == "Valid":
            result["status"] = "Needs Review"

        metrics = result["metrics"]

        record = AnalysisRun(
            filename=result["filename"],
            sample=result["sample"],
            detected_strain_column=result["detected_strain_column"],
            detected_stress_column=result["detected_stress_column"],
            data_type=result["data_type"],
            status=result["status"],
            maximum_load_n=metrics["maximum_load_n"],
            peak_stress_mpa=metrics["peak_stress_mpa"],
            strain_at_peak=metrics["strain_at_peak"],
            youngs_modulus_mpa=metrics["youngs_modulus_mpa"],
            modulus_r2=metrics["modulus_r2"],
            area_under_curve=metrics["area_under_curve"],
            rows=metrics["rows"],
            warnings=result["warnings"],
            clean_data=result["clean_data"],
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        result["id"] = record.id
        results.append(result)

    return {"count": len(results), "results": results}
