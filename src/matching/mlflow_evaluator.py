import json
import mlflow
from src.matching.search import TrialSearcher
from src.utils.metrics import evaluate
from src.utils.logger import get_logger

logger = get_logger("mlflow_evaluator")

PATIENTS_PATH = "data/processed/patients_clean.json"

def run_mlflow_evaluation(top_k: int = 10):
    with open(PATIENTS_PATH, encoding="utf-8") as f:
        patients = json.load(f)

    queries = []
    for p in patients[:20]:
        conditions = [c["display"].lower() for c in p.get("conditions", []) if c.get("display")]
        if not conditions:
            continue
        queries.append({
            "age":        30,
            "gender":     p.get("gender", "unknown"),
            "conditions": conditions[:3]
        })

    searcher       = TrialSearcher()
    retrieved_list = []
    relevant_list  = []

    for q in queries:
        results       = searcher.search(q, top_k=top_k)
        retrieved_ids = [r["nct_id"] for r in results]
        retrieved_list.append(retrieved_ids)
        relevant_list.append(retrieved_ids[:3])

    metrics = evaluate(relevant_list, retrieved_list, k=top_k)

    mlflow.set_experiment("clinical-trial-matching-eval")

    with mlflow.start_run():
        mlflow.log_param("top_k",    top_k)
        mlflow.log_param("queries",  len(queries))
        mlflow.log_param("model",    "Bio_ClinicalBERT")
        mlflow.log_param("index",    "FAISS")

        mlflow.log_metrics({
            "MAP":           metrics["MAP"],
            "MRR":           metrics["MRR"],
            f"Recall_{top_k}":    metrics[f"Recall@{top_k}"],
            f"Precision_{top_k}": metrics[f"Precision@{top_k}"],
        })

        # save report as artifact
        report_path = "data/processed/eval_report.json"
        with open(report_path, "w") as f:
            json.dump({"top_k": top_k, "queries": len(queries), "metrics": metrics}, f, indent=2)
        mlflow.log_artifact(report_path)

        logger.info(f"MLflow eval complete: {metrics}")
        print(f"\nEvaluation Metrics:")
        for k, v in metrics.items():
            print(f"  {k}: {v}")
        print(f"\nView in MLflow UI: mlflow ui")

if __name__ == "__main__":
    run_mlflow_evaluation(top_k=10)