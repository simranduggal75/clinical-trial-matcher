import json
from collections import Counter

def trial_stats(trials_path: str) -> dict:
    with open(trials_path, encoding="utf-8") as f:
        trials = json.load(f)

    conditions = []
    phases = []
    sex_counts = Counter()
    has_inclusion = 0
    has_exclusion = 0

    for t in trials:
        conditions.extend(t.get("conditions", []))
        phases.extend(t.get("phases", []))
        sex_counts[t.get("sex", "UNKNOWN")] += 1
        if t.get("inclusion"):
            has_inclusion += 1
        if t.get("exclusion"):
            has_exclusion += 1

    return {
        "total_trials":        len(trials),
        "top_conditions":      Counter(conditions).most_common(10),
        "top_phases":          Counter(phases).most_common(5),
        "sex_distribution":    dict(sex_counts),
        "has_inclusion":       has_inclusion,
        "has_exclusion":       has_exclusion,
    }

if __name__ == "__main__":
    stats = trial_stats("data/processed/trials_clean.json")
    print(f"Total trials: {stats['total_trials']}")
    print(f"\nTop conditions:")
    for cond, count in stats["top_conditions"]:
        print(f"  {cond}: {count}")
    print(f"\nSex distribution: {stats['sex_distribution']}")
    print(f"Trials with inclusion criteria: {stats['has_inclusion']}")
    print(f"Trials with exclusion criteria: {stats['has_exclusion']}") 
