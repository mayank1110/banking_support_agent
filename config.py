"""
Configuration settings for Banking Customer Support AI Agent
Loads configuration from environment variables with sensible defaults.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project root directory
BASE_DIR = Path(__file__).resolve().parent

# ==================== Application Configuration ====================
APP_NAME = os.getenv("APP_NAME", "banking_support_agent")
APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

# ==================== Model Configuration ====================
MODEL_NAME = os.getenv("MODEL_NAME", "distilbert-base-uncased")
OUTPUT_DIR = os.getenv("MODEL_PATH", str(BASE_DIR / "models" / "intent-distilbert"))
NUM_LABELS = int(os.getenv("NUM_LABELS", "3"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "16"))
EPOCHS = int(os.getenv("EPOCHS", "3"))
LEARNING_RATE = float(os.getenv("LEARNING_RATE", "2e-5"))
WEIGHT_DECAY = float(os.getenv("WEIGHT_DECAY", "0.01"))
LOGGING_STEPS = int(os.getenv("LOGGING_STEPS", "10"))
MAX_LENGTH = int(os.getenv("MAX_LENGTH", "128"))

# ==================== Label Configuration ====================
LABEL_LIST = os.getenv("LABEL_LIST", "Query,Positive Feedback,Negative Feedback").split(",")
LABEL2ID = {label: i for i, label in enumerate(LABEL_LIST)}
ID2LABEL = {i: label for label, i in LABEL2ID.items()}

# ==================== Dataset Configuration ====================
DATA_DIR = os.getenv("DATA_DIR", str(BASE_DIR / "data"))
TRAIN_CSV = os.getenv("TRAIN_CSV", str(BASE_DIR / "data" / "banking_support_dataset_train_model.csv"))
TICKET_CSV = os.getenv("TICKET_CSV", str(BASE_DIR / "data" / "support_tickets.csv"))
TEST_SPLIT = float(os.getenv("TEST_SPLIT", "0.1"))
RANDOM_SEED = int(os.getenv("RANDOM_SEED", "42"))

# ==================== Ticket Configuration ====================
TICKET_ID_MIN = int(os.getenv("TICKET_ID_MIN", "100000"))
TICKET_ID_MAX = int(os.getenv("TICKET_ID_MAX", "999999"))

# ==================== Gradio Configuration ====================
GRADIO_SHARE = os.getenv("GRADIO_SHARE", "False").lower() in ("true", "1", "yes")
GRADIO_DEBUG = os.getenv("GRADIO_DEBUG", "True").lower() in ("true", "1", "yes")
GRADIO_SERVER_NAME = os.getenv("GRADIO_SERVER_NAME", "127.0.0.1")
GRADIO_SERVER_PORT = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
GRADIO_TITLE = os.getenv("GRADIO_TITLE", "🏦 Banking Customer Support AI Agent")

# ==================== Logging Configuration ====================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", str(BASE_DIR / "logs" / "app.log"))

# ==================== Database Configuration (Future) ====================
DATABASE_URL = os.getenv("DATABASE_URL", None)
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))
DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "10"))

# ==================== API Configuration (Future) ====================
API_KEY = os.getenv("API_KEY", None)
API_RATE_LIMIT = int(os.getenv("API_RATE_LIMIT", "100"))

# ==================== Security Configuration ====================
SECRET_KEY = os.getenv("SECRET_KEY", None)

# ==================== Paths ====================
# Ensure directories exist
os.makedirs(os.path.dirname(OUTPUT_DIR), exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# ==================== Validation ====================
def validate_config():
    """Validate critical configuration values."""
    import sys
    
    # Check if training data exists
    if not os.path.exists(TRAIN_CSV):
        print(f"⚠️  Warning: Training data not found: {TRAIN_CSV}")
        print("   Please ensure the training dataset exists before training.")
    
    # Validate model path
    if not os.path.exists(os.path.dirname(OUTPUT_DIR)):
        os.makedirs(os.path.dirname(OUTPUT_DIR), exist_ok=True)
    
    # Validate ticket CSV path
    if not os.path.exists(os.path.dirname(TICKET_CSV)):
        os.makedirs(os.path.dirname(TICKET_CSV), exist_ok=True)
    
    # Validate required environment variables in production
    if APP_ENV == "production" and DEBUG:
        print("⚠️  Warning: DEBUG mode is enabled in production environment!")
        print("   Set DEBUG=False in .env for production deployments.")
    
    return True

# Run validation on import
validate_config()
