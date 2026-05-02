# Clinical Trial Matching System

An AI system that automatically matches patient medical records to relevant clinical trials using Bio_ClinicalBERT and FAISS vector search.

## Overview

This project builds a production-ready system for matching de-identified patient EHR records to clinical trials from ClinicalTrials.gov using:

- **Bio_ClinicalBERT** for medical named entity recognition (NER) and semantic embeddings
- **FAISS** vector index for fast similarity search over 500+ trials
- **Rule-based filtering** for age, sex, and trial status pre-filtering
- **FastAPI** service for deployment (in progress)
- **Synthea** for synthetic EHR patient data generation

## What's Built So Far

| Phase | Status | Description |
|-------|--------|-------------|
| Data Collection | ✅ Done | 500+ trials from ClinicalTrials.gov, 100+ synthetic patients via Synthea |
| Preprocessing | ✅ Done | Structured trial eligibility, patient profiles |
| NER Pipeline | ✅ Done | Auto-labeled EHR snippets, HuggingFace token-classification format |
| FAISS Index | ✅ Done | Bio_ClinicalBERT embeddings, semantic search returning top-K trials |
| FastAPI Service | 🔄 In Progress | |
| Streamlit Demo | 🔄 In Progress | |
| Docker Deployment | 🔄 In Progress | |

## Directory Structure

```
clinical-trial-matcher/
├── data/
│   ├── raw/              # Raw downloaded data (gitignored)
│   ├── processed/        # Cleaned trials, patient profiles, FAISS index
│   └── annotations/      # NER labeled EHR snippets
├── src/
│   ├── data/             # Download, preprocess, NER pipeline scripts
│   ├── models/           # Bio_ClinicalBERT NER training
│   ├── matching/         # Embedder, FAISS index builder, search
│   ├── api/              # FastAPI application (in progress)
│   └── utils/            # Logger, config, text cleaner, age parser, filters
├── tests/                # Unit and integration tests
├── notebooks/            # Exploratory analysis
└── configs/              # YAML configuration
```

## Quick Start

```bash
git clone https://github.com/simranduggal75/clinical-trial-matcher.git
cd clinical-trial-matcher
pip install -r requirements.txt

# Fetch trials
python src/data/download_trials.py

# Generate synthetic patients
python src/data/generate_patients.py

# Preprocess
python src/data/preprocess.py

# Build FAISS index
python src/matching/build_index.py

# Search
python src/matching/search.py
```

## Tech Stack

`Python` `HuggingFace Transformers` `Bio_ClinicalBERT` `FAISS` `FastAPI` `Synthea` `scikit-learn` `PyTorch`

## License

MIT
