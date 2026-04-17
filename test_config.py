"""
Test script to verify environment variable configuration
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import (
    APP_NAME,
    APP_ENV,
    DEBUG,
    MODEL_NAME,
    OUTPUT_DIR,
    NUM_LABELS,
    BATCH_SIZE,
    EPOCHS,
    LEARNING_RATE,
    GRADIO_SHARE,
    GRADIO_SERVER_PORT,
    LOG_LEVEL,
    DATABASE_URL,
    validate_config,
)

def test_environment_variables():
    """Test that environment variables are loaded correctly."""
    print("=" * 60)
    print("Testing Environment Variable Configuration")
    print("=" * 60)
    print()
    
    # Test application config
    print("✅ Application Settings:")
    print(f"   APP_NAME: {APP_NAME}")
    print(f"   APP_ENV: {APP_ENV}")
    print(f"   DEBUG: {DEBUG}")
    print()
    
    # Test model config
    print("✅ Model Settings:")
    print(f"   MODEL_NAME: {MODEL_NAME}")
    print(f"   OUTPUT_DIR: {OUTPUT_DIR}")
    print(f"   NUM_LABELS: {NUM_LABELS}")
    print(f"   BATCH_SIZE: {BATCH_SIZE}")
    print(f"   EPOCHS: {EPOCHS}")
    print(f"   LEARNING_RATE: {LEARNING_RATE}")
    print()
    
    # Test Gradio config
    print("✅ Gradio Settings:")
    print(f"   GRADIO_SHARE: {GRADIO_SHARE}")
    print(f"   GRADIO_SERVER_PORT: {GRADIO_SERVER_PORT}")
    print()
    
    # Test logging config
    print("✅ Logging Settings:")
    print(f"   LOG_LEVEL: {LOG_LEVEL}")
    print()
    
    # Test database config (should be None for now)
    print("✅ Database Settings:")
    print(f"   DATABASE_URL: {DATABASE_URL}")
    print(f"   (Not configured yet - this is expected)")
    print()
    
    # Run validation
    print("✅ Running Configuration Validation...")
    if validate_config():
        print("   Validation passed!")
    print()
    
    print("=" * 60)
    print("✅ All environment variables loaded successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Edit .env file to customize settings")
    print("2. Run 'python train_model.py' to train the model")
    print("3. Run 'python app.py' to launch the application")
    print()

if __name__ == "__main__":
    test_environment_variables()
