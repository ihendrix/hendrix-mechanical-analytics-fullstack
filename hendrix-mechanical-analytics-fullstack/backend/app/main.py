from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routes import analyses, uploads

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hendrix Mechanical Analytics API",
    description="FastAPI backend for full-stack mechanical-testing data analysis.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyses.router)
app.include_router(uploads.router)


@app.get("/")
def root():
    return {
        "name": "Hendrix Mechanical Analytics API",
        "status": "running",
        "docs": "/docs",
    }
