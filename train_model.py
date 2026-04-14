"""
Training script for Banking Customer Support AI Agent
"""

from src.classifier import IntentClassifier

def main():
    print("=" * 60)
    print("🚀 Training Intent Classification Model")
    print("=" * 60)
    print()
    
    # Create classifier instance
    classifier = IntentClassifier()
    
    # Load dataset
    print("📊 Loading dataset...")
    train_dataset, eval_dataset = classifier.load_dataset()
    print(f"✅ Loaded {len(train_dataset)} training samples")
    print(f"✅ Loaded {len(eval_dataset)} evaluation samples")
    print()
    
    # Train model
    print("🔥 Starting training...")
    print("This may take 5-15 minutes depending on your hardware.")
    print()
    
    trainer = classifier.train(train_dataset, eval_dataset)
    
    print()
    print("=" * 60)
    print("✅ Model training completed successfully!")
    print("=" * 60)
    print()
    print(f"📁 Model saved to: ./models/intent-distilbert")
    print()
    
    # Test the model
    print("🧪 Testing trained model...")
    test_samples = [
        "Thanks, that was helpful",
        "My card was declined and I need help",
        "What is the status of my account",
    ]
    
    from src.classifier import hf_model_classify
    
    for sample in test_samples:
        result = hf_model_classify(sample)
        print(f"  '{sample}' → {result}")
    
    print()
    print("🎉 Training complete! Ready to run the application.")

if __name__ == "__main__":
    main()