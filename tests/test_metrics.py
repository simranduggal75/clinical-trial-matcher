from src.utils.metrics import (
    precision_at_k, recall_at_k,
    average_precision, mean_average_precision,
    reciprocal_rank, mean_reciprocal_rank,
    evaluate
)

RELEVANT  = ["NCT001", "NCT003", "NCT005"]
RETRIEVED = ["NCT001", "NCT002", "NCT003", "NCT004", "NCT005"]

def test_precision_at_k():
    assert round(precision_at_k(RELEVANT, RETRIEVED, k=3), 4) == round(2/3, 4)

def test_recall_at_k():
    assert recall_at_k(RELEVANT, RETRIEVED, k=5) == 1.0

def test_average_precision():
    ap = average_precision(RELEVANT, RETRIEVED)
    assert 0 < ap <= 1.0

def test_reciprocal_rank():
    rr = reciprocal_rank(RELEVANT, RETRIEVED)
    assert rr == 1.0

def test_mrr():
    mrr = mean_reciprocal_rank([RELEVANT], [RETRIEVED])
    assert mrr == 1.0

def test_map():
    map_score = mean_average_precision([RELEVANT], [RETRIEVED])
    assert 0 < map_score <= 1.0

def test_evaluate():
    results = evaluate([RELEVANT], [RETRIEVED], k=5)
    assert "MAP" in results
    assert "MRR" in results
    assert "Recall@5" in results
    assert "Precision@5" in results

if __name__ == "__main__":
    test_precision_at_k()
    test_recall_at_k()
    test_average_precision()
    test_reciprocal_rank()
    test_mrr()
    test_map()
    test_evaluate()
    print("All tests passed.")