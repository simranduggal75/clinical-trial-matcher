import requests
import json
import os
import time

SAVE_DIR = "data/raw/trials"
os.makedirs(SAVE_DIR, exist_ok=True)

BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

def fetch_trials():
    all_trials = []
    next_token = None
    page = 1

    while len(all_trials) < 500:
        params = {
            "format": "json",
            "pageSize": 100,
            "query.cond": "cancer",
            "filter.overallStatus": "RECRUITING",
        }

        if next_token:
            params["pageToken"] = next_token

        response = requests.get(BASE_URL, params=params, timeout=30)
        print(f"Status code: {response.status_code}")

        if response.status_code != 200:
            print(f"Error: {response.text[:300]}")
            break

        data = response.json()
        studies = data.get("studies", [])
        print(f"Page {page} — fetched {len(studies)} — total: {len(all_trials) + len(studies)}")

        if not studies:
            break

        all_trials.extend(studies)
        next_token = data.get("nextPageToken")
        if not next_token:
            break

        page += 1
        time.sleep(0.5)

    return all_trials

def save_trials(trials):
    path = os.path.join(SAVE_DIR, "trials_raw.json")
    with open(path, "w") as f:
        json.dump(trials, f, indent=2)
    print(f"Saved {len(trials)} trials to {path}")

if __name__ == "__main__":
    trials = fetch_trials()
    save_trials(trials)