"""
Banking Customer Support AI Agent - Main Entry Point

This script provides a simple entry point to launch the application.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))


def main():
    """Main entry point for the application."""
    print("=" * 60)
    print("🏦 Banking Customer Support AI Agent")
    print("=" * 60)
    print()
    
    # Check if model exists
    from config import OUTPUT_DIR
    if not os.path.exists(OUTPUT_DIR):
        print("⚠️  Model not found. Please train the model first.")
        print()
        print("To train the model:")
        print("  1. Run the Jupyter notebook: Capstone_1_Banking_Customer_Support.ipynb")
        print("  2. Or use Python:")
        print("     from src.classifier import IntentClassifier")
        print("     classifier = IntentClassifier()")
        print("     train_ds, eval_ds = classifier.load_dataset()")
        print("     classifier.train(train_ds, eval_ds)")
        print()
        response = input("Do you want to train the model now? (y/n): ")
        if response.lower() == 'y':
            from src.classifier import IntentClassifier
            classifier = IntentClassifier()
            train_ds, eval_ds = classifier.load_dataset()
            classifier.train(train_ds, eval_ds)
            print("✅ Model trained successfully!")
        else:
            print("⚠️  Classification will not work until model is trained.")
            print()
    
    print()
    print("🚀 Launching Gradio web interface...")
    print()
    
    # Launch UI
    from src.ui import launch_ui
    launch_ui()


if __name__ == "__main__":
    main()
