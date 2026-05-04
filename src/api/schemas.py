from pydantic import BaseModel, Field
from typing import List, Optional

class PatientInput(BaseModel):
    age:         int            = Field(..., ge=0, le=120)
    gender:      str            = Field(..., description="male or female")
    conditions:  List[str]      = Field(..., min_items=1)
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
    total_matches: int
    trials:        List[TrialResult]