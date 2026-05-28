from fastapi import HTTPException
from src.utils.logger import get_logger

logger = get_logger("error_handler")

class PatientValidationError(Exception):
    pass

class TrialSearchError(Exception):
    pass

class IndexNotFoundError(Exception):
    pass

def handle_validation_error(errors: list):
    if errors:
        logger.error(f"Validation errors: {errors}")
        raise HTTPException(status_code=422, detail=errors)

def handle_search_error(e: Exception):
    logger.error(f"Search error: {str(e)}")
    raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

def safe_divide(a: float, b: float, default: float = 0.0) -> float:
    return a / b if b != 0 else default