import json
import re
import os
import glob

RAW_TRIALS = "data/raw/trials/trials_raw.json"
RAW_PATIENTS_DIR = "data/raw/patients"
OUT_TRIALS = "data/processed/trials_clean.json"
OUT_PATIENTS = "data/processed/patients_clean.json"

os.makedirs("data/processed", exist_ok=True)

# ── Trial Preprocessing 

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_criteria(text):
    inclusion, exclusion = [], []
    if not text:
        return inclusion, exclusion

    text = text.replace("\r\n", "\n").replace("\r", "\n")

    inc = re.search(r"inclusion criteria[:\s]*(.*?)(?=exclusion criteria|$)", text, re.I | re.S)
    exc = re.search(r"exclusion criteria[:\s]*(.*?)$", text, re.I | re.S)

    def parse_bullets(block):
        lines = block.strip().split("\n")
        return [l.strip("•-* \t") for l in lines if len(l.strip()) > 10]

    if inc:
        inclusion = parse_bullets(inc.group(1))
    if exc:
        exclusion = parse_bullets(exc.group(1))

    return inclusion, exclusion

def preprocess_trials():
    with open(RAW_TRIALS) as f:
        trials = json.load(f)

    cleaned, skipped = [], 0

    for t in trials:
        proto = t.get("protocolSection", {})
        ident = proto.get("identificationModule", {})
        elig  = proto.get("eligibilityModule", {})
        cond  = proto.get("conditionsModule", {})
        design = proto.get("designModule", {})

        raw_elig = elig.get("eligibilityCriteria", "")
        if not raw_elig:
            skipped += 1
            continue

        inclusion, exclusion = extract_criteria(raw_elig)

        cleaned.append({
            "nct_id":          ident.get("nctId"),
            "title":           clean_text(ident.get("briefTitle", "")),
            "conditions":      cond.get("conditions", []),
            "phases":          design.get("phases", []),
            "min_age":         elig.get("minimumAge", ""),
            "max_age":         elig.get("maximumAge", ""),
            "sex":             elig.get("sex", "ALL"),
            "inclusion":       inclusion,
            "exclusion":       exclusion,
            "raw_eligibility": clean_text(raw_elig)
        })

    with open(OUT_TRIALS, "w") as f:
        json.dump(cleaned, f, indent=2)

    print(f"Trials  — processed: {len(cleaned)}, skipped: {skipped}")

# ── Patient Preprocessing 

def extract_patient_info(fhir_bundle):
    """Extract basic fields from a Synthea FHIR bundle."""
    patient_info = {
        "id": None, "gender": None, "birth_date": None,
        "conditions": [], "medications": []
    }

    for entry in fhir_bundle.get("entry", []):
        resource = entry.get("resource", {})
        rtype = resource.get("resourceType")

        if rtype == "Patient":
            patient_info["id"] = resource.get("id")
            patient_info["gender"] = resource.get("gender")
            patient_info["birth_date"] = resource.get("birthDate")

        elif rtype == "Condition":
            code = resource.get("code", {})
            codings = code.get("coding", [])
            if codings:
                patient_info["conditions"].append({
                    "code": codings[0].get("code"),
                    "display": codings[0].get("display")
                })

        elif rtype == "MedicationRequest":
            med = resource.get("medicationCodeableConcept", {})
            codings = med.get("coding", [])
            if codings:
                patient_info["medications"].append({
                    "code": codings[0].get("code"),
                    "display": codings[0].get("display")
                })

    return patient_info

def preprocess_patients():
    files = glob.glob(os.path.join(RAW_PATIENTS_DIR, "*.json"))
    # skip hospitalInformation and practitionerInformation files
    files = [f for f in files if not any(x in f for x in ["hospitalInformation", "practitionerInformation"])]

    patients = []
    for fpath in files:
        with open(fpath, encoding="utf-8") as f:
            try:
                bundle = json.load(f)
                info = extract_patient_info(bundle)
                if info["id"]:
                    patients.append(info)
            except Exception as e:
                print(f"Skipped {fpath}: {e}")

    with open(OUT_PATIENTS, "w") as f:
        json.dump(patients, f, indent=2)

    print(f"Patients — processed: {len(patients)}")

# ── Main 

if __name__ == "__main__":
    preprocess_trials()
    preprocess_patients()
    print("Done. Files saved to data/processed/")