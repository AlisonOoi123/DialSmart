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
from sklearn.pipeline import Pipeline, FeatureUnion
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

    # Create dual vectorizer (word + character n-grams)
    print("\nCreating optimized feature extractors...")

    # Word-level TF-IDF - optimized
    word_vectorizer = TfidfVectorizer(
        analyzer='word',
        ngram_range=(1, 2),  # Reduced from (1,3) to avoid overfitting
        max_features=5000,  # Reduced from 10000 to focus on most important features
        min_df=2,  # Increased from 1 to reduce noise
        max_df=0.8,  # Reduced from 0.85 to filter common words
        lowercase=True,
        strip_accents='unicode',
        stop_words='english',
        sublinear_tf=True,
        use_idf=True,
        norm='l2'
    )

    # Character-level TF-IDF - optimized
    char_vectorizer = TfidfVectorizer(
        analyzer='char',
        ngram_range=(3, 4),  # Adjusted from (2,5) for better patterns
        max_features=3000,  # Reduced from 5000
        lowercase=True,
        sublinear_tf=True,
        use_idf=True,
        norm='l2'
    )

    # Combine both vectorizers for powerful feature extraction
    vectorizer = FeatureUnion([
        ('word', word_vectorizer),
        ('char', char_vectorizer)
    ])

    # Use GridSearchCV to find optimal hyperparameters
    print("Building optimized Linear SVM classifier with GridSearchCV...")

    # Create base pipeline
    pipeline = Pipeline([
        ('tfidf', vectorizer),
        ('classifier', LinearSVC(random_state=42, class_weight='balanced', dual=False, max_iter=20000))
    ])

    # Parameter grid for optimization
    param_grid = {
        'classifier__C': [0.1, 0.3, 0.5, 1.0],  # Regularization strength
        'classifier__loss': ['hinge', 'squared_hinge'],  # Loss function
        'classifier__tol': [1e-4, 1e-5],  # Convergence tolerance
    }

    print("Performing GridSearchCV to find optimal hyperparameters (this may take 2-3 minutes)...")
    grid_search = GridSearchCV(
        pipeline,
        param_grid,
        cv=3,  # 3-fold CV for speed
        scoring='accuracy',
        n_jobs=-1,  # Use all CPU cores
        verbose=1
    )

    grid_search.fit(X_train, y_train)

    print(f"\nBest parameters found: {grid_search.best_params_}")
    print(f"Best cross-validation accuracy: {grid_search.best_score_:.4f} ({grid_search.best_score_*100:.2f}%)")

    # Use the best estimator
    pipeline = grid_search.best_estimator_

    # Evaluate
    print("\nEvaluating model performance...")
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\nTest Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")

    # Detailed classification report
    print("\n" + "="*70)
    print("DETAILED CLASSIFICATION REPORT (Per-Intent Performance)")
    print("="*70)
    print(classification_report(y_test, y_pred, zero_division=0))

    # Cross-validation
    print("\nPerforming 5-fold cross-validation...")
    cv_scores = cross_val_score(pipeline, X, y, cv=5)
    print(f"Cross-validation scores: {cv_scores}")
    print(f"Average CV accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

    # Show min/max CV scores
    print(f"Min CV score: {cv_scores.min():.4f} ({cv_scores.min()*100:.2f}%)")
    print(f"Max CV score: {cv_scores.max():.4f} ({cv_scores.max()*100:.2f}%)")

    # Save model
    model_path = 'models/chatbot_intent_classifier.pkl'
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    with open(model_path, 'wb') as f:
        pickle.dump(pipeline, f)

    print(f"\nModel saved to {model_path}")

    # Test predictions - including critical test cases
    test_texts = [
        "hello there",
        "show me phones under rm2000",
        "i need a gaming phone",
        "gaming phone within rm3000",  # Critical test case
        "for senior citizen",  # Persona test
        "student gaming phone",  # Persona + usage test
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
        predicted_intent = pipeline.predict([text])[0]
        # LinearSVC uses decision_function instead of predict_proba
        try:
            decision = pipeline.decision_function([text])[0]
            # Normalize decision scores to pseudo-probabilities
            confidence = max(decision) / (sum(abs(decision)) + 1e-10)
        except:
            confidence = 1.0  # Fallback if decision_function fails

        print(f"\nInput: '{text}'")
        print(f"Predicted Intent: {predicted_intent}")
        print(f"Confidence Score: {confidence:.4f}")

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
    print("- 1600+ balanced training examples")
    print("- Dual TF-IDF vectorization (word + char n-grams)")
    print("- LinearSVC classifier with GridSearchCV optimization")
    print("- Stratified 5-fold cross-validation")
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
