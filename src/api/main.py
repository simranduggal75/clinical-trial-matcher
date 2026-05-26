from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from src.matching.search import TrialSearcher
from src.utils.logger import get_logger
from src.api.monitoring import router as monitoring_router, track_request, track_match_results, ACTIVE_REQUESTS
import time

logger = get_logger("api")

searcher = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global searcher
    logger.info("Loading TrialSearcher...")
    searcher = TrialSearcher()
    logger.info("TrialSearcher ready")
    yield
    searcher = None

app = FastAPI(
    title="Clinical Trial Matcher API",
    description="Match patient records to clinical trials using Bio_ClinicalBERT + FAISS",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(monitoring_router)

@app.middleware("http")
async def monitor_requests(request, call_next):
    ACTIVE_REQUESTS.inc()
    start = time.time()
    response = await call_next(request)
    latency = time.time() - start
    track_request(
        endpoint=request.url.path,
        method=request.method,
        status=response.status_code,
        latency=latency
    )
    ACTIVE_REQUESTS.dec()
    return response

class PatientInput(BaseModel):
    age:         int            = Field(..., ge=0, le=120)
    gender:      str            = Field(...)
    conditions:  List[str]      = Field(...)
    medications: Optional[List[str]] = []

class TrialResult(BaseModel):
    nct_id:      str
    title:       str
    conditions:  List[str]
    match_score: float
    min_age:     Optional[str]
    max_age:     Optional[str]
    sex:         Optional[str]

class MatchResponse(BaseModel):
    patient:       PatientInput
    total_matches: int
    trials:        List[TrialResult]

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model":  "Bio_ClinicalBERT",
        "index":  "FAISS",
        "trials": searcher.index.ntotal if searcher else 0
    }

@app.post("/match", response_model=MatchResponse)
def match_trials(patient: PatientInput, top_k: int = 10):
    if not searcher:
        raise HTTPException(status_code=503, detail="Search engine not ready")
    try:
        logger.info(f"Matching trials for age={patient.age} gender={patient.gender}")
        patient_dict = {
            "age":        patient.age,
            "gender":     patient.gender,
            "conditions": patient.conditions,
            "medications": patient.medications
        }
        results = searcher.search(patient_dict, top_k=top_k)
        trials = [
            TrialResult(
                nct_id=      r.get("nct_id", ""),
                title=       r.get("title", ""),
                conditions=  r.get("conditions", []),
                match_score= r.get("match_score", 0.0),
                min_age=     r.get("min_age", ""),
                max_age=     r.get("max_age", ""),
                sex=         r.get("sex", "ALL")
            )
            for r in results
        ]
        
        track_match_results([t.dict() for t in trials])
        
        return MatchResponse(
            patient=       patient,
            total_matches= len(trials),
            trials=        trials
        )
    except Exception as e:
        logger.error(f"Match error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Clinical Trial Matcher API", "docs": "/docs", "health": "/health"}