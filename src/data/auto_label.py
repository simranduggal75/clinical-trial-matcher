import json
import re
import os

IN_PATH  = "data/annotations/ehr_snippets.json"
OUT_PATH = "data/annotations/ehr_snippets_autolabeled.json"
os.makedirs("data/annotations", exist_ok=True)

CONDITION_KEYWORDS = [
    "diabetes", "hypertension", "cancer", "asthma", "stroke",
    "obesity", "depression", "anxiety", "arthritis", "alzheimer",
    "epilepsy", "anemia", "fibrosis", "leukemia", "pneumonia",
    "infection", "disorder", "disease", "syndrome", "failure",
    "tumor", "carcinoma", "dementia", "osteoporosis", "migraine",
    "psoriasis", "lupus", "copd", "parkinson", "schizophrenia"
]

DRUG_KEYWORDS = [
    "metformin", "insulin", "aspirin", "lisinopril", "atorvastatin",
    "amoxicillin", "ibuprofen", "warfarin", "omeprazole", "amlodipine",
    "metoprolol", "losartan", "gabapentin", "sertraline", "prednisone",
    "albuterol", "levothyroxine", "hydrochlorothiazide", "simvastatin"
]

PROCEDURE_KEYWORDS = [
    "surgery", "biopsy", "transplant", "dialysis", "chemotherapy",
    "radiation", "screening", "imaging", "mri", "ct scan",
    "blood test", "examination", "therapy", "treatment", "vaccination",
    "endoscopy", "colonoscopy", "mammography", "ultrasound"
]

DEMOGRAPHICS_KEYWORDS = [
    "male", "female", "years old", "year old", "born", "age"
]

LABEL_MAP = {
    "condition":   (CONDITION_KEYWORDS,  "CONDITION"),
    "drug":        (DRUG_KEYWORDS,       "DRUG"),
    "procedure":   (PROCEDURE_KEYWORDS,  "PROCEDURE"),
    "demographic": (DEMOGRAPHICS_KEYWORDS, "DEMOGRAPHICS"),
}

def find_entities(text: str) -> list:
    entities = []
    text_lower = text.lower()

    for _, (keywords, label) in LABEL_MAP.items():
        for kw in keywords:
            for match in re.finditer(re.escape(kw), text_lower):
                entities.append({
                    "text":  text[match.start():match.end()],
                    "label": label,
                    "start": match.start(),
                    "end":   match.end(),
                    "score": 1.0
                })

    # deduplicate by start position
    seen = set()
    unique = []
    for e in sorted(entities, key=lambda x: x["start"]):
        if e["start"] not in seen:
            seen.add(e["start"])
            unique.append(e)

    return unique

if __name__ == "__main__":
    with open(IN_PATH, encoding="utf-8") as f:
        snippets = json.load(f)

    print(f"Labeling {len(snippets)} snippets...")
    labeled = []

    for item in snippets:
        labeled.append({
            "id":       item["id"],
            "text":     item["text"],
            "entities": find_entities(item["text"])
        })

    total = sum(len(x["entities"]) for x in labeled)

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(labeled, f, indent=2)

    print(f"Done. {len(labeled)} snippets labeled")
    print(f"Total entities found: {total}")
    print(f"Avg entities per snippet: {round(total/len(labeled), 2)}")
    print(f"Sample: {labeled[0]['entities'][:3]}")