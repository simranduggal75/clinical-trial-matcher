import json
import os
import mlflow
import mlflow.pytorch
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
from seqeval.metrics import f1_score, precision_score, recall_score
from src.utils.logger import get_logger

logger = get_logger("mlflow_trainer")

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

def train_with_mlflow(params: dict = None):
    if params is None:
        params = {
            "epochs":     3,
            "batch_size": 8,
            "max_length": 256,
            "model_name": MODEL_NAME
        }

    mlflow.set_experiment("clinical-ner-training")

    with mlflow.start_run():
        # log params
        mlflow.log_params(params)
        logger.info(f"MLflow run started with params: {params}")

        tokenizer = AutoTokenizer.from_pretrained(params["model_name"])
        model     = AutoModelForTokenClassification.from_pretrained(
            params["model_name"],
            num_labels=len(LABELS),
            id2label=ID2LABEL,
            label2id=LABEL2ID
        )

        train_dataset = NERDataset(TRAIN_PATH, tokenizer, params["max_length"])
        val_dataset   = NERDataset(VAL_PATH,   tokenizer, params["max_length"])

        args = TrainingArguments(
            output_dir=OUT_DIR,
            num_train_epochs=params["epochs"],
            per_device_train_batch_size=params["batch_size"],
            per_device_eval_batch_size=params["batch_size"],
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

        logger.info("Starting training...")
        trainer.train()

        # evaluate and log metrics
        results = trainer.evaluate()
        mlflow.log_metrics({
            "eval_f1":        results.get("eval_f1", 0),
            "eval_precision": results.get("eval_precision", 0),
            "eval_recall":    results.get("eval_recall", 0),
            "eval_loss":      results.get("eval_loss", 0),
        })

        # log model
        mlflow.pytorch.log_model(model, "ner_model")
        trainer.save_model(OUT_DIR)
        tokenizer.save_pretrained(OUT_DIR)

        logger.info(f"Training complete. F1: {results.get('eval_f1', 0):.4f}")
        print(f"\nMLflow run complete.")
        print(f"F1: {results.get('eval_f1', 0):.4f}")
        print(f"View runs: mlflow ui")

if __name__ == "__main__":
    train_with_mlflow()