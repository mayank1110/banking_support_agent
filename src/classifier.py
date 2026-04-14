"""
Intent Classification Module
Fine-tuned transformer model for classifying customer support messages.
"""

import os
import numpy as np
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    pipeline,
)
from datasets import Dataset
import evaluate
import pandas as pd

from config import (
    MODEL_NAME,
    OUTPUT_DIR,
    NUM_LABELS,
    BATCH_SIZE,
    EPOCHS,
    LEARNING_RATE,
    WEIGHT_DECAY,
    LOGGING_STEPS,
    MAX_LENGTH,
    LABEL_LIST,
    LABEL2ID,
    ID2LABEL,
    TRAIN_CSV,
    TEST_SPLIT,
    RANDOM_SEED,
)


class IntentClassifier:
    """Intent classification model for banking customer support."""

    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.classifier = None
        self._prepare_directories()

    def _prepare_directories(self):
        """Ensure model output directory exists."""
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    def load_dataset(self, csv_path: str = None):
        """Load and preprocess training dataset."""
        csv_path = csv_path or TRAIN_CSV

        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Training dataset not found: {csv_path}")

        df = pd.read_csv(csv_path)
        print(f"Loaded dataset with {len(df)} rows")

        # Validate labels
        expected_labels = set(LABEL_LIST)
        actual_labels = set(df["label"].astype(str).unique().tolist())
        if not actual_labels.issubset(expected_labels):
            raise ValueError(
                f"Dataset contains invalid labels. Expected: {expected_labels}, Got: {actual_labels}"
            )

        # Map labels to IDs
        df["label_id"] = df["label"].map(LABEL2ID)

        # Create Hugging Face Dataset
        dataset = Dataset.from_pandas(
            df[["text", "label_id"]].rename(columns={"text": "text", "label_id": "label"})
        )

        # Split dataset
        dataset = dataset.train_test_split(test_size=TEST_SPLIT, seed=RANDOM_SEED)
        return dataset["train"], dataset["test"]

    def preprocess(self, batch):
        """Tokenize text data."""
        return self.tokenizer(
            batch["text"], truncation=True, padding="max_length", max_length=MAX_LENGTH
        )

    def train(self, train_dataset, eval_dataset):
        """Train the intent classification model."""
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

        # Preprocess datasets
        train_dataset = train_dataset.map(self.preprocess, batched=True)
        eval_dataset = eval_dataset.map(self.preprocess, batched=True)

        # Set format for PyTorch
        train_dataset.set_format(
            type="torch", columns=["input_ids", "attention_mask", "label"]
        )
        eval_dataset.set_format(
            type="torch", columns=["input_ids", "attention_mask", "label"]
        )

        # Load model
        self.model = AutoModelForSequenceClassification.from_pretrained(
            MODEL_NAME,
            num_labels=NUM_LABELS,
            id2label=ID2LABEL,
            label2id=LABEL2ID,
        )

        # Load metrics
        metric = evaluate.load("accuracy")

        def compute_metrics(eval_pred):
            logits, labels = eval_pred
            preds = np.argmax(logits, axis=-1)
            return metric.compute(predictions=preds, references=labels)

        # Training arguments
        training_args = TrainingArguments(
            output_dir=OUTPUT_DIR,
            do_eval=True,
            learning_rate=LEARNING_RATE,
            per_device_train_batch_size=BATCH_SIZE,
            per_device_eval_batch_size=BATCH_SIZE,
            num_train_epochs=EPOCHS,
            weight_decay=WEIGHT_DECAY,
            logging_steps=LOGGING_STEPS,
            push_to_hub=False,
        )

        # Initialize trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            compute_metrics=compute_metrics,
        )

        # Train model
        print("Starting training...")
        trainer.train()

        # Save model and tokenizer
        trainer.save_model(OUTPUT_DIR)
        self.tokenizer.save_pretrained(OUTPUT_DIR)
        print(f"Model saved to {OUTPUT_DIR}")

        return trainer

    def load_model(self, model_dir: str = None):
        """Load trained model for inference."""
        model_dir = model_dir or OUTPUT_DIR

        if not os.path.exists(model_dir):
            raise FileNotFoundError(
                f"Model directory not found: {model_dir}. Please train the model first."
            )

        self.classifier = pipeline(
            "text-classification",
            model=model_dir,
            tokenizer=model_dir,
            return_all_scores=False,
        )

    def classify(self, text: str) -> str:
        """Classify input text into intent category."""
        if not isinstance(text, str) or text.strip() == "":
            return "Query"

        if self.classifier is None:
            self.load_model()

        output = self.classifier(text)[0]
        label = output["label"]

        # Normalize labels if needed
        if label not in LABEL_LIST:
            if label.startswith("LABEL_"):
                idx = int(label.split("_")[1])
                return ID2LABEL.get(idx, "Query")
            return "Query"

        return label


# Singleton instance
_classifier_instance = None


def get_classifier() -> IntentClassifier:
    """Get or create classifier instance."""
    global _classifier_instance
    if _classifier_instance is None:
        _classifier_instance = IntentClassifier()
    return _classifier_instance


def hf_model_classify(text: str) -> str:
    """
    Classify input text into intent category.
    
    Args:
        text: Input customer message
        
    Returns:
        Intent category: "Query", "Positive Feedback", or "Negative Feedback"
    """
    classifier = get_classifier()
    return classifier.classify(text)


if __name__ == "__main__":
    # Example usage
    samples = [
        "Thanks, that was helpful",
        "My card was declined and I need help",
        "What is the status of 123456",
    ]

    for sample in samples:
        print(f"{sample} -> {hf_model_classify(sample)}")
