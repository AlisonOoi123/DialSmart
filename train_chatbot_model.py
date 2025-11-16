#!/usr/bin/env python3
"""
Train Chatbot Intent Classification Model
Run this script to train the ML model for intent classification
"""
import sys
import os
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.chatbot_training_data import get_all_training_samples, get_intent_labels

def train_and_save_model():
    """Train and save the chatbot intent classifier"""
    print("Preparing training data...")
    samples = get_all_training_samples()
    X = [sample[0] for sample in samples]
    y = [sample[1] for sample in samples]

    print(f"Loaded {len(X)} training samples across {len(set(y))} intents")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Training set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")

    # Create improved TF-IDF vectorizer
    print("\nCreating optimized feature extractor...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 3),  # Use up to 3-grams for better context
        max_features=8000,   # Features for better discrimination
        min_df=1,
        max_df=0.90,
        lowercase=True,
        strip_accents='unicode',
        stop_words='english',
        sublinear_tf=True,   # Use sublinear TF scaling
        use_idf=True,
        norm='l2'
    )

    # Use Linear SVC which typically performs better for text classification
    print("Building Linear SVM classifier (best for text)...")

    # Linear SVC - very good for text classification with better accuracy
    base_classifier = LinearSVC(
        C=1.0,
        max_iter=5000,
        random_state=42,
        class_weight='balanced',  # Handle class imbalance
        dual=False  # Better for n_samples > n_features
    )

    # Calibrate to get probability estimates
    classifier = CalibratedClassifierCV(base_classifier, cv=3)

    # Create pipeline
    pipeline = Pipeline([
        ('tfidf', vectorizer),
        ('classifier', classifier)
    ])

    print("Training and calibrating Linear SVM model (this may take a minute)...")
    pipeline.fit(X_train, y_train)

    # Evaluate
    print("\nEvaluating model performance...")
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\nTest Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")

    # Cross-validation
    print("\nPerforming 5-fold cross-validation...")
    cv_scores = cross_val_score(pipeline, X, y, cv=5)
    print(f"Cross-validation scores: {cv_scores}")
    print(f"Average CV accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

    # Save model
    model_path = 'models/chatbot_intent_classifier.pkl'
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    with open(model_path, 'wb') as f:
        pickle.dump(pipeline, f)

    print(f"\nModel saved to {model_path}")

    # Test predictions
    test_texts = [
        "hello there",
        "show me phones under rm2000",
        "i need a gaming phone",
        "compare iphone and samsung",
        "what phones have good cameras",
        "show me xiaomi phones",
        "help me find a phone",
        "phones with 5g",
        "best battery life phone",
        "phones with amoled display"
    ]

    print("\n" + "="*60)
    print("TESTING SAMPLE PREDICTIONS")
    print("="*60)

    for text in test_texts:
        proba = pipeline.predict_proba([text])[0]
        predicted_intent = pipeline.predict([text])[0]
        confidence = max(proba)

        print(f"\nInput: '{text}'")
        print(f"Predicted Intent: {predicted_intent}")
        print(f"Confidence: {confidence:.4f} ({confidence*100:.2f}%)")

    return accuracy

if __name__ == '__main__':
    print("="*70)
    print("DIALSMART CHATBOT ML MODEL TRAINING")
    print("="*70)
    print()
    print("This script will train the intent classification model")
    print("for the DialSmart chatbot using machine learning.")
    print()
    print("Training data includes:")
    print("- 14 intent categories")
    print("- Multiple training examples per intent")
    print("- TF-IDF vectorization + Naive Bayes classifier")
    print()
    print("="*70)
    print()

    try:
        # Train and save the model
        accuracy = train_and_save_model()

        print()
        print("="*70)
        print("✓ Training completed successfully!")
        print(f"✓ Model accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        print("✓ Model saved to models/chatbot_intent_classifier.pkl")
        print("✓ The chatbot will now use ML-based intent classification")
        print("="*70)

    except Exception as e:
        print()
        print("="*70)
        print("✗ Error during training:")
        print(f"  {str(e)}")
        import traceback
        traceback.print_exc()
        print("="*70)
        sys.exit(1)
