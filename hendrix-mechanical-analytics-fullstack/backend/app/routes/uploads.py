from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/api/uploads", tags=["uploads"])


@router.get("/health")
def upload_health():
    return {"status": "upload service ready"}
