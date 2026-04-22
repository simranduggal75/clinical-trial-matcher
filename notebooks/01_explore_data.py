
import json
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Load Trials ---
with open("data/raw/trials/trials_raw.json") as f:
    trials = json.load(f)

print(f"Total trials loaded: {len(trials)}")

# Extract key fields
records = []
for t in trials:
    proto = t.get("protocolSection", {})
    ident = proto.get("identificationModule", {})
    elig = proto.get("eligibilityModule", {})
    cond = proto.get("conditionsModule", {})

    records.append({
        "nct_id": ident.get("nctId"),
        "title": ident.get("briefTitle"),
        "conditions": ", ".join(cond.get("conditions", [])),
        "eligibility": elig.get("eligibilityCriteria", ""),
    })

df = pd.DataFrame(records)
print(df.head())
print(f"\nNull eligibility rows: {df['eligibility'].isna().sum()}")

# --- Eligibility text length distribution ---
df["elig_length"] = df["eligibility"].str.len()
df["elig_length"].hist(bins=30)
plt.title("Eligibility Criteria Text Length Distribution")
plt.xlabel("Character count")
plt.ylabel("Number of trials")
plt.tight_layout()
plt.savefig("notebooks/elig_length_dist.png")
print("Plot saved.")

# --- Condition frequency ---
all_conditions = []
for c in df["conditions"]:
    all_conditions.extend([x.strip() for x in c.split(",")])

cond_series = pd.Series(all_conditions)
print("\nTop 10 conditions:")
print(cond_series.value_counts().head(10))

# Save processed summary
df.to_csv("data/processed/trials_summary.csv", index=False)
print("\nSummary saved to data/processed/trials_summary.csv") 
