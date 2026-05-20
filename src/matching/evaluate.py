import json
from src.matching.search import TrialSearcher
from src.utils.metrics import evaluate
from src.utils.logger import get_logger

logger = get_logger("evaluate")

PATIENTS_PATH = "data/processed/patients_clean.json"

def build_test_queries(patients: list, n: int = 20) -> list:
    """Build test queries from patient profiles."""
    queries = []
    for p in patients[:n]:
        conditions = [c["display"].lower() for c in p.get("conditions", []) if c.get("display")]
        if not conditions:
            continue
        queries.append({
            "id":         p.get("id"),
            "age":        30,
            "gender":     p.get("gender", "unknown"),
            "conditions": conditions[:3]
        })
    return queries

def run_evaluation(top_k: int = 10):
    with open(PATIENTS_PATH, encoding="utf-8") as f:
        patients = json.load(f)

    queries = build_test_queries(patients, n=20)
    logger.info(f"Running evaluation on {len(queries)} queries")

    searcher = TrialSearcher()

    retrieved_list = []
    relevant_list  = []

    for q in queries:
        results = searcher.search(q, top_k=top_k)
        retrieved_ids = [r["nct_id"] for r in results]
        retrieved_list.append(retrieved_ids)

        # use top-3 as pseudo-relevant (no ground truth labels)
        relevant_list.append(retrieved_ids[:3])

    metrics = evaluate(relevant_list, retrieved_list, k=top_k)

    print("\n=== Evaluation Results ===")
    for metric, value in metrics.items():
        print(f"{metric}: {value}")

    # save report
    with open("data/processed/eval_report.json", "w") as f:
        json.dump({
            "queries":  len(queries),
            "top_k":    top_k,
            "metrics":  metrics
        }, f, indent=2)

    logger.info("Evaluation complete. Report saved.")
    return metrics

if __name__ == "__main__":
    run_evaluation(top_k=10)