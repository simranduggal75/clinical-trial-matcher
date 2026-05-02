import json
import numpy as np
import faiss
from src.matching.embedder import ClinicalEmbedder
from src.utils.trial_filter import apply_basic_filters
from src.utils.logger import get_logger

logger = get_logger("search")

INDEX_PATH    = "data/processed/faiss_index.bin"
METADATA_PATH = "data/processed/trial_metadata.json"

class TrialSearcher:
    def __init__(self):
        logger.info("Loading FAISS index and metadata...")
        self.index    = faiss.read_index(INDEX_PATH)
        self.embedder = ClinicalEmbedder()

        with open(METADATA_PATH, encoding="utf-8") as f:
            self.metadata = json.load(f)

        logger.info(f"Index loaded with {self.index.ntotal} trials")

    def search(self, patient: dict, top_k: int = 10) -> list:
        """
        Search for top-K matching trials for a patient.
        patient dict expects: age, gender, conditions (list of strings)
        """
        # build query text from patient profile
        conditions = ", ".join(patient.get("conditions", []))
        query_text = f"Patient conditions: {conditions}."

        # embed query
        query_vec = self.embedder.embed_single(query_text).astype(np.float32)
        query_vec = query_vec.reshape(1, -1)

        # search FAISS
        scores, indices = self.index.search(query_vec, top_k * 2)  # fetch extra for filtering

        # build results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            trial = self.metadata[idx].copy()
            trial["match_score"] = round(float(score), 4)
            results.append(trial)

        # apply basic filters (age, sex)
        results = apply_basic_filters(results, patient)

        return results[:top_k]


if __name__ == "__main__":
    searcher = TrialSearcher()

    test_patient = {
        "age":        45,
        "gender":     "female",
        "conditions": ["diabetes", "hypertension"]
    }

    print(f"\nSearching trials for: {test_patient}")
    matches = searcher.search(test_patient, top_k=5)

    print(f"\nTop {len(matches)} matches:")
    for i, m in enumerate(matches, 1):
        print(f"\n{i}. {m['nct_id']} — {m['title']}")
        print(f"   Score: {m['match_score']}")
        print(f"   Conditions: {m['conditions']}")
        print(f"   Age: {m['min_age']} - {m['max_age']}, Sex: {m['sex']}")