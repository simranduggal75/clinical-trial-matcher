import numpy as np

def precision_at_k(relevant: list, retrieved: list, k: int) -> float:
    """Fraction of top-K retrieved that are relevant."""
    retrieved_k = retrieved[:k]
    hits = sum(1 for r in retrieved_k if r in relevant)
    return hits / k if k > 0 else 0.0

def recall_at_k(relevant: list, retrieved: list, k: int) -> float:
    """Fraction of relevant retrieved in top-K."""
    retrieved_k = retrieved[:k]
    hits = sum(1 for r in retrieved_k if r in relevant)
    return hits / len(relevant) if relevant else 0.0

def average_precision(relevant: list, retrieved: list) -> float:
    """Average precision for a single query."""
    if not relevant:
        return 0.0
    hits, score = 0, 0.0
    for i, r in enumerate(retrieved, 1):
        if r in relevant:
            hits += 1
            score += hits / i
    return score / len(relevant)

def mean_average_precision(relevant_list: list, retrieved_list: list) -> float:
    """MAP over multiple queries."""
    aps = [
        average_precision(rel, ret)
        for rel, ret in zip(relevant_list, retrieved_list)
    ]
    return float(np.mean(aps)) if aps else 0.0

def reciprocal_rank(relevant: list, retrieved: list) -> float:
    """Reciprocal rank for a single query."""
    for i, r in enumerate(retrieved, 1):
        if r in relevant:
            return 1.0 / i
    return 0.0

def mean_reciprocal_rank(relevant_list: list, retrieved_list: list) -> float:
    """MRR over multiple queries."""
    rrs = [
        reciprocal_rank(rel, ret)
        for rel, ret in zip(relevant_list, retrieved_list)
    ]
    return float(np.mean(rrs)) if rrs else 0.0

def evaluate(relevant_list: list, retrieved_list: list, k: int = 10) -> dict:
    """Run all metrics and return summary."""
    return {
        "MAP":           round(mean_average_precision(relevant_list, retrieved_list), 4),
        "MRR":           round(mean_reciprocal_rank(relevant_list, retrieved_list), 4),
        f"Recall@{k}":   round(float(np.mean([
            recall_at_k(rel, ret, k)
            for rel, ret in zip(relevant_list, retrieved_list)
        ])), 4),
        f"Precision@{k}": round(float(np.mean([
            precision_at_k(rel, ret, k)
            for rel, ret in zip(relevant_list, retrieved_list)
        ])), 4),
    }