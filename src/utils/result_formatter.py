from typing import List

def format_trial_result(trial: dict) -> dict:
    """Format a single trial result for clean output."""
    return {
        "nct_id":      trial.get("nct_id", "N/A"),
        "title":       trial.get("title", "N/A")[:100],
        "conditions":  ", ".join(trial.get("conditions", [])),
        "match_score": round(trial.get("match_score", 0.0), 4),
        "age_range":   f"{trial.get('min_age', 'N/A')} - {trial.get('max_age', 'N/A')}",
        "sex":         trial.get("sex", "ALL"),
        "url":         f"https://clinicaltrials.gov/study/{trial.get('nct_id', '')}"
    }

def format_results(trials: List[dict]) -> List[dict]:
    return [format_trial_result(t) for t in trials]

def results_to_text(trials: List[dict]) -> str:
    """Convert trial results to readable text summary."""
    if not trials:
        return "No matching trials found."

    lines = [f"Found {len(trials)} matching trials:\n"]
    for i, t in enumerate(trials, 1):
        formatted = format_trial_result(t)
        lines.append(
            f"{i}. {formatted['title']}\n"
            f"   NCT ID: {formatted['nct_id']}\n"
            f"   Score:  {formatted['match_score']}\n"
            f"   Age:    {formatted['age_range']}\n"
            f"   URL:    {formatted['url']}\n"
        )
    return "\n".join(lines)

if __name__ == "__main__":
    sample = [{
        "nct_id": "NCT001",
        "title": "Diabetes Study",
        "conditions": ["diabetes"],
        "match_score": 0.89,
        "min_age": "18 Years",
        "max_age": "75 Years",
        "sex": "ALL"
    }]
    print(results_to_text(sample))