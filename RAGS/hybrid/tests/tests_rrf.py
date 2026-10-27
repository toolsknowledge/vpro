from collections import defaultdict

def rrf_fuse(list_a, list_b, k=60):
    scores = defaultdict(float)
    for ranking in (list_a, list_b):
        for rank, item in enumerate(ranking, start=1):
            scores[item] += 1 / (k + rank)
    return sorted(scores.items(), key=lambda pair: pair[1], reverse=True)

def test_rrf_rewards_items_in_both_lists():
    ranked = rrf_fuse(["A", "B", "C"], ["C", "A", "D"])
    assert ranked[0][0] == "A"

def test_rrf_empty_lists():
    assert rrf_fuse([], []) == []
