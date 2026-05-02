import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel
from src.utils.logger import get_logger

logger = get_logger("embedder")

MODEL_NAME = "emilyalsentzer/Bio_ClinicalBERT"

class ClinicalEmbedder:
    def __init__(self, model_name: str = MODEL_NAME):
        logger.info(f"Loading model: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model     = AutoModel.from_pretrained(model_name)
        self.model.eval()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        logger.info(f"Model loaded on {self.device}")

    def embed(self, texts: list, batch_size: int = 16) -> np.ndarray:
        """Convert list of texts to embeddings using mean pooling."""
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]

            encoded = self.tokenizer(
                batch,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt"
            ).to(self.device)

            with torch.no_grad():
                output = self.model(**encoded)

            # mean pooling over token embeddings
            attention_mask = encoded["attention_mask"]
            token_embeddings = output.last_hidden_state
            input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
            embeddings = torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)

            all_embeddings.append(embeddings.cpu().numpy())
            logger.info(f"Embedded batch {i // batch_size + 1}/{(len(texts) - 1) // batch_size + 1}")

        return np.vstack(all_embeddings)

    def embed_single(self, text: str) -> np.ndarray:
        """Embed a single text string."""
        return self.embed([text])[0]


if __name__ == "__main__":
    embedder = ClinicalEmbedder()
    test_texts = [
        "Patient diagnosed with diabetes and hypertension.",
        "Inclusion criteria: age 18-65, cancer diagnosis required."
    ]
    embeddings = embedder.embed(test_texts)
    print(f"Embedding shape: {embeddings.shape}")
    print(f"Sample embedding[:5]: {embeddings[0][:5]}")