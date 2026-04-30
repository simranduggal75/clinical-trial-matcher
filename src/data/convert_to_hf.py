import json
import os
from transformers import AutoTokenizer

IN_PATH  = "data/annotations/ehr_snippets_autolabeled.json"
OUT_DIR  = "data/processed/ner_dataset"
os.makedirs(OUT_DIR, exist_ok=True)

MODEL_NAME = "emilyalsentzer/Bio_ClinicalBERT"
tokenizer  = AutoTokenizer.from_pretrained(MODEL_NAME)

LABELS = [
    "O",
    "B-CONDITION", "I-CONDITION",
    "B-DRUG",      "I-DRUG",
    "B-PROCEDURE", "I-PROCEDURE",
    "B-DEMOGRAPHICS", "I-DEMOGRAPHICS"
]
LABEL2ID = {l: i for i, l in enumerate(LABELS)}

def char_spans_to_bio(text, entities, tokens, offsets):
    labels = ["O"] * len(tokens)

    for ent in entities:
        s, e, label = ent["start"], ent["end"], ent["label"]
        first = True
        for i, (tok_s, tok_e) in enumerate(offsets):
            if tok_s is None or tok_e is None:
                continue
            if tok_s >= s and tok_e <= e:
                if first:
                    labels[i] = f"B-{label}"
                    first = False
                else:
                    labels[i] = f"I-{label}"

    return labels

def convert(snippets):
    dataset = []
    skipped = 0

    for item in snippets:
        try:
            encoding = tokenizer(
                item["text"],
                return_offsets_mapping=True,
                truncation=True,
                max_length=256
            )

            tokens    = encoding.tokens()
            offsets   = encoding["offset_mapping"]
            labels    = char_spans_to_bio(item["text"], item["entities"], tokens, offsets)
            label_ids = [LABEL2ID.get(l, 0) for l in labels]

            dataset.append({
                "id":        item["id"],
                "tokens":    tokens,
                "labels":    labels,
                "label_ids": label_ids
            })

        except Exception as ex:
            print(f"Skipped {item['id']}: {ex}")
            skipped += 1

    return dataset, skipped

if __name__ == "__main__":
    with open(IN_PATH, encoding="utf-8") as f:
        snippets = json.load(f)

    print(f"Converting {len(snippets)} snippets...")
    dataset, skipped = convert(snippets)

    # 80/20 train/val split
    split = int(len(dataset) * 0.8)
    train = dataset[:split]
    val   = dataset[split:]

    with open(f"{OUT_DIR}/train.json", "w") as f:
        json.dump(train, f, indent=2)
    with open(f"{OUT_DIR}/val.json", "w") as f:
        json.dump(val, f, indent=2)

    print(f"Train: {len(train)}, Val: {len(val)}, Skipped: {skipped}")
    print(f"Sample tokens: {dataset[0]['tokens'][:10]}")
    print(f"Sample labels: {dataset[0]['labels'][:10]}")
    print(f"Saved to {OUT_DIR}")