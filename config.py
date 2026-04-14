"""
Configuration settings for Banking Customer Support AI Agent
"""

import os

# ==================== Model Configuration ====================
MODEL_NAME = "distilbert-base-uncased"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "models", "intent-distilbert")
NUM_LABELS = 3
BATCH_SIZE = 16
EPOCHS = 3
LEARNING_RATE = 2e-5
WEIGHT_DECAY = 0.01
LOGGING_STEPS = 10
MAX_LENGTH = 128

# ==================== Label Configuration ====================
LABEL_LIST = ["Query", "Positive Feedback", "Negative Feedback"]
LABEL2ID = {label: i for i, label in enumerate(LABEL_LIST)}
ID2LABEL = {i: label for label, i in LABEL2ID.items()}

# ==================== Dataset Configuration ====================
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TRAIN_CSV = os.path.join(DATA_DIR, "banking_support_dataset_train_model.csv")
TICKET_CSV = os.path.join(DATA_DIR, "support_tickets.csv")
TEST_SPLIT = 0.1
RANDOM_SEED = 42

# ==================== Ticket Configuration ====================
TICKET_ID_MIN = 100000
TICKET_ID_MAX = 999999

# ==================== Gradio Configuration ====================
GRADIO_SHARE = True
GRADIO_DEBUG = True
GRADIO_TITLE = "🏦 Banking Customer Support AI Agent"

# ==================== Paths ====================
# Ensure directories exist
os.makedirs(os.path.join(os.path.dirname(__file__), "models"), exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
