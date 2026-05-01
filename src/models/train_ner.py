import json
import os
import numpy as np
import torch
from torch.utils.data import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    TrainingArguments,
    Trainer,
    DataCollatorForTokenClassification
)
from seqeval.metrics import f1_score, precision_score, recall_score, classification_report

TRAIN_PATH = "data/processed/ner_dataset/train.json"
VAL_PATH   = "data/processed/ner_dataset/val.json"
MODEL_NAME = "emilyalsentzer/Bio_ClinicalBERT"
OUT_DIR    = "src/models/ner_model"

LABELS = [
    "O",
    "B-CONDITION", "I-CONDITION",
    "B-DRUG",      "I-DRUG",
    "B-PROCEDURE", "I-PROCEDURE",
    "B-DEMOGRAPHICS", "I-DEMOGRAPHICS"
]
LABEL2ID = {l: i for i, l in enumerate(LABELS)}
ID2LABEL = {i: l for l, i in LABEL2ID.items()}

class NERDataset(Dataset):
    def __init__(self, path, tokenizer, max_len=256):
        with open(path, encoding="utf-8") as f:
            self.data = json.load(f)
        self.tokenizer = tokenizer
        self.max_len   = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item      = self.data[idx]
        label_ids = item["label_ids"]
        text      = " ".join(t for t in item["tokens"] if t not in ["[CLS]", "[SEP]", "[PAD]"])

        encoding = self.tokenizer(
            text,
            truncation=True,
            max_length=self.max_len,
            padding="max_length",
            return_tensors="pt"
        )

        # align labels to new tokenization
        seq_len = encoding["input_ids"].shape[1]
        if len(label_ids) < seq_len:
            label_ids = label_ids + [-100] * (seq_len - len(label_ids))
        else:
            label_ids = label_ids[:seq_len]

        return {
            "input_ids":      encoding["input_ids"].squeeze(),
            "attention_mask": encoding["attention_mask"].squeeze(),
            "labels":         torch.tensor(label_ids, dtype=torch.long)
        }

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions    = np.argmax(logits, axis=-1)

    true_labels, true_preds = [], []
    for pred_seq, label_seq in zip(predictions, labels):
        t, p = [], []
        for p_id, l_id in zip(pred_seq, label_seq):
            if l_id == -100:
                continue
            t.append(ID2LABEL.get(l_id, "O"))
            p.append(ID2LABEL.get(p_id, "O"))
        true_labels.append(t)
        true_preds.append(p)

    return {
        "f1":        f1_score(true_labels, true_preds),
        "precision": precision_score(true_labels, true_preds),
        "recall":    recall_score(true_labels, true_preds),
    }

def train():
    os.makedirs(OUT_DIR, exist_ok=True)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model     = AutoModelForTokenClassification.from_pretrained(
        MODEL_NAME,
        num_labels=len(LABELS),
        id2label=ID2LABEL,
        label2id=LABEL2ID
    )

    train_dataset = NERDataset(TRAIN_PATH, tokenizer)
    val_dataset   = NERDataset(VAL_PATH,   tokenizer)

    args = TrainingArguments(
        output_dir=OUT_DIR,
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        logging_dir="logs",
        logging_steps=10,
        fp16=torch.cuda.is_available(),
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
        data_collator=DataCollatorForTokenClassification(tokenizer)
    )

    print("Starting NER training...")
    print(f"Train samples: {len(train_dataset)}, Val samples: {len(val_dataset)}")
    print(f"Device: {'GPU' if torch.cuda.is_available() else 'CPU'}")

    trainer.train()
    trainer.save_model(OUT_DIR)
    tokenizer.save_pretrained(OUT_DIR)

    # print final report
    predictions = trainer.predict(val_dataset)
    preds = np.argmax(predictions.predictions, axis=-1)
    true_labels, true_preds = [], []
    for pred_seq, label_seq in zip(preds, predictions.label_ids):
        t, p = [], []
        for p_id, l_id in zip(pred_seq, label_seq):
            if l_id == -100:
                continue
            t.append(ID2LABEL.get(int(l_id), "O"))
            p.append(ID2LABEL.get(int(p_id), "O"))
        true_labels.append(t)
        true_preds.append(p)

    print("\nFinal Evaluation Report:")
    print(classification_report(true_labels, true_preds))
    print(f"Model saved to {OUT_DIR}")

if __name__ == "__main__":
    train()