from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status":    "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version":   "1.0.0",
        "model":     "Bio_ClinicalBERT",
        "index":     "FAISS"
    }

@router.get("/ready")
def readiness_check():
    return {"status": "ready"}