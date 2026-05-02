import json
import os
import numpy as np
import faiss
from src.matching.embedder import ClinicalEmbedder
from src.utils.logger import get_logger

logger = get_logger("build_index")

TRIALS_PATH     = "data/processed/trials_clean.json"
EMBEDDINGS_PATH = "data/processed/trial_embeddings.npy"
INDEX_PATH      = "data/processed/faiss_index.bin"
METADATA_PATH   = "data/processed/trial_metadata.json"

def build_trial_texts(trials: list) -> list:
    """Convert trial dicts into searchable text strings."""
    texts = []
    for t in trials:
        conditions = ", ".join(t.get("conditions", []))
        inclusion  = " ".join(t.get("inclusion", [])[:5])  # first 5 criteria
        text = f"{t.get('title', '')}. Conditions: {conditions}. Eligibility: {inclusion}"
        texts.append(text)
    return texts

def build_index():
    # load trials
    with open(TRIALS_PATH, encoding="utf-8") as f:
        trials = json.load(f)
    logger.info(f"Loaded {len(trials)} trials")

    # build text representations
    texts = build_trial_texts(trials)

    # embed all trials
    embedder   = ClinicalEmbedder()
    embeddings = embedder.embed(texts, batch_size=16)
    logger.info(f"Embeddings shape: {embeddings.shape}")

    # save embeddings
    np.save(EMBEDDINGS_PATH, embeddings)
    logger.info(f"Saved embeddings to {EMBEDDINGS_PATH}")

    # build FAISS index
    dim   = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  # inner product = cosine sim on normalized vectors
    index.add(embeddings.astype(np.float32))
    faiss.write_index(index, INDEX_PATH)
    logger.info(f"FAISS index built with {index.ntotal} vectors, saved to {INDEX_PATH}")

    # save metadata for result lookup
    metadata = [
        {
            "nct_id":     t.get("nct_id"),
            "title":      t.get("title"),
            "conditions": t.get("conditions"),
            "min_age":    t.get("min_age"),
            "max_age":    t.get("max_age"),
            "sex":        t.get("sex"),
        }
        for t in trials
    ]
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    logger.info(f"Saved metadata to {METADATA_PATH}")

    print(f"\nDone. Index contains {index.ntotal} trials.")

if __name__ == "__main__":
    build_index()