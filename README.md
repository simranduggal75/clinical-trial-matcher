# Clinical Trial Matching System

An AI system that automatically matches patient medical records to relevant clinical trials using advanced NLP techniques.

## Overview

This project aims to build a production-ready system for matching de-identified patient records (EHR snippets) to clinical trials from ClinicalTrials.gov. The system uses:

- Fine-tuned ClinicalBERT models for medical named entity recognition (NER) and trial eligibility embedding.
- A vector store (FAISS) for efficient similarity search.
- A hybrid matching approach: rule-based filtering followed by neural re-ranking.
- A FastAPI service for deployment, with monitoring and evaluation components.

## Directory Structure

```
clinical-trial-matcher/
├── data/
│   ├── raw/              # Raw data downloaded from sources
│   └── processed/        # Cleaned and processed data
├── src/
│   ├── data/             # Data loading and preprocessing scripts
│   ├── models/           # Model training and fine-tuning scripts
│   ├── matching/         # Matching engine logic
│   ├── api/              # FastAPI application
│   └── utils/            # Utility functions
├── tests/                # Unit and integration tests
└── README.md
```

## Getting Started

1. Clone the repository.
2. Install dependencies (see `requirements.txt` or `environment.yml`).
3. Download the data (see `src/data/download.py`).
4. Preprocess the data (see `src/data/preprocess.py`).
5. Train/fine-tune models (see `src/models/`).
6. Build the matching engine (see `src/matching/`).
7. Run the API service (see `src/api/`).
8. Evaluate the system (see `tests/`).

## License

MIT