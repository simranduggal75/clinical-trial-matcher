from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import APIRouter, Response
import time

router = APIRouter()

# metrics
REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total API requests",
    ["endpoint", "method", "status"]
)

REQUEST_LATENCY = Histogram(
    "api_request_latency_seconds",
    "API request latency",
    ["endpoint"],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

MATCH_SCORE = Histogram(
    "trial_match_score",
    "Distribution of trial match scores",
    buckets=[0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
)

TRIALS_RETURNED = Histogram(
    "trials_returned_per_request",
    "Number of trials returned per match request",
    buckets=[1, 2, 3, 5, 10, 20]
)

ACTIVE_REQUESTS = Gauge(
    "api_active_requests",
    "Number of active requests"
)

def track_request(endpoint: str, method: str, status: int, latency: float):
    REQUEST_COUNT.labels(endpoint=endpoint, method=method, status=str(status)).inc()
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)

def track_match_results(trials: list):
    TRIALS_RETURNED.observe(len(trials))
    for trial in trials:
        score = trial.get("match_score", 0)
        MATCH_SCORE.observe(score)

@router.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )