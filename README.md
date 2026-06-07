# 🏥 Clinical Trial Matcher

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-orange)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![MLflow](https://img.shields.io/badge/MLflow-Experiment%20Tracking-red)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-orange)

An AI system that automatically matches patient medical records to relevant clinical trials using Bio_ClinicalBERT embeddings and FAISS vector search.

## Problem

80% of clinical trials fail to meet enrollment timelines because matching patients to trials is done manually by doctors. This system automates that process.


## 🚀 Live Demo
🔗 [https://huggingface.co/spaces/simranduggal75/clinical-trial-matcher](https://huggingface.co/spaces/simranduggal75/clinical-trial-matcher)

> **Note:** Deployed on HuggingFace Spaces (free tier). Uses lightweight rule-based matching for the demo. Full Bio_ClinicalBERT + FAISS pipeline available locally — see Quick Start below.

## Architecture

```
Patient EHR Input
      ↓
Condition Normalizer + Patient Profile Builder
      ↓
Bio_ClinicalBERT Embedder (768-dim vectors)
      ↓
FAISS Vector Index (500+ trials)
      ↓
Rule-based Filter (age, sex, trial status)
      ↓
Trial Re-ranker (condition overlap + gender boost)
      ↓
Top-K Matched Trials
      ↓
FastAPI /match endpoint → Streamlit UI
```

## What's Built

| Phase | Status | Description |
|-------|--------|-------------|
| Data Collection | ✅ | 500+ trials from ClinicalTrials.gov, 100+ synthetic patients via Synthea |
| Preprocessing | ✅ | Structured trial eligibility, patient profiles |
| NER Pipeline | ✅ | Auto-labeled EHR snippets, HuggingFace token-classification format |
| FAISS Index | ✅ | Bio_ClinicalBERT embeddings, semantic search |
| Rule-based Filtering | ✅ | Age, sex, trial status filters |
| Re-ranking | ✅ | Condition overlap + gender boost scoring |
| FastAPI Service | ✅ | /match, /health, /metrics endpoints |
| Streamlit UI | ✅ | Interactive demo for clinicians |
| Docker | ✅ | Full stack containerization |
| MLflow | ✅ | Experiment tracking for NER training |
| Prometheus | ✅ | Request monitoring and match score tracking |
| Evaluation | ✅ | MAP, MRR, Recall@K, Precision@K |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| NLP Model | Bio_ClinicalBERT |
| Vector Search | FAISS |
| API | FastAPI + Pydantic |
| UI | Streamlit |
| Monitoring | Prometheus |
| Experiment Tracking | MLflow |
| Containerization | Docker + docker-compose |
| Data Generation | Synthea (synthetic EHR) |
| Data Source | ClinicalTrials.gov API |

## Quick Start

### Without Docker

```bash
# clone
git clone https://github.com/simranduggal75/clinical-trial-matcher.git
cd clinical-trial-matcher

# install
pip install -r requirements.txt

# fetch data
python src/data/download_trials.py
python src/data/generate_patients.py
python src/data/preprocess.py

# build FAISS index
python src/matching/build_index.py

# start API
uvicorn src.api.main:app --reload

# start UI (new terminal)
streamlit run src/api/streamlit_app.py
```

### With Docker

```bash
docker-compose up --build
```

API: http://localhost:8000
UI: http://localhost:8501
Docs: http://localhost:8000/docs
Metrics: http://localhost:8000/metrics
MLflow: http://localhost:5000 (run `mlflow ui`)

## API Usage

### Match Trials

```bash
curl -X POST "http://localhost:8000/match?top_k=5" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "gender": "female",
    "conditions": ["diabetes", "hypertension"],
    "medications": ["metformin"]
  }'
```

### Response

```json
{
  "total_matches": 5,
  "trials": [
    {
      "nct_id": "NCT02869477",
      "title": "...",
      "conditions": ["diabetes"],
      "match_score": 0.8929,
      "min_age": "18 Years",
      "max_age": "75 Years",
      "sex": "ALL"
    }
  ]
}
```

## Evaluation Results

| Metric | Score |
|--------|-------|
| MAP | logged via MLflow |
| MRR | logged via MLflow |
| Recall@10 | logged via MLflow |
| Precision@10 | logged via MLflow |

Run evaluation:
```bash
python src/matching/evaluate.py
mlflow ui  # view results at localhost:5000
```

## Project Structure

```
clinical-trial-matcher/
├── data/
│   ├── raw/              # Raw data (gitignored)
│   ├── processed/        # Trials, patients, FAISS index
│   └── annotations/      # NER labeled EHR snippets
├── src/
│   ├── data/             # Download, preprocess, NER pipeline
│   ├── models/           # Bio_ClinicalBERT NER training + MLflow
│   ├── matching/         # Embedder, FAISS index, search, evaluation
│   ├── api/              # FastAPI, Streamlit, Prometheus monitoring
│   └── utils/            # Logger, config, validators, metrics, filters
├── tests/                # 20+ unit and integration tests
├── configs/              # YAML configuration
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## License

MIT
