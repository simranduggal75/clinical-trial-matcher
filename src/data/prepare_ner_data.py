import json
import os
import glob
import random

IN_DIR = "data/processed"
OUT_DIR = "data/annotations"
os.makedirs(OUT_DIR, exist_ok=True)

def extract_ehr_snippets():
    with open(f"{IN_DIR}/patients_clean.json") as f:
        patients = json.load(f)

    snippets = []

    for p in patients:
        gender = p.get("gender", "unknown")
        dob = p.get("birth_date", "unknown")

        conditions = ", ".join(
            [c["display"] for c in p.get("conditions", []) if c.get("display")]
        )
        medications = ", ".join(
            [m["display"] for m in p.get("medications", []) if m.get("display")]
        )

        if not conditions:
            continue

        # Build a realistic EHR-style text snippet
        text = (
            f"Patient is a {gender}, born {dob}. "
            f"Diagnosed with: {conditions}. "
        )
        if medications:
            text += f"Current medications: {medications}."

        snippets.append({
            "id": p.get("id"),
            "text": text,
            "entities": []  # to be filled during annotation
        })

    # shuffle and take 500
    random.seed(42)
    random.shuffle(snippets)
    snippets = snippets[:500]

    out_path = f"{OUT_DIR}/ehr_snippets.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(snippets, f, indent=2)

    print(f"Saved {len(snippets)} EHR snippets to {out_path}")

if __name__ == "__main__":
    extract_ehr_snippets()