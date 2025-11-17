"""
Chatbot Machine Learning Trainer
Trains intent classification model using scikit-learn
"""
import os
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import sys

# Add parent directory to path to import training data
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from data.chatbot_training_data import get_all_training_samples, get_intent_labels

class ChatbotMLTrainer:
    """Machine learning trainer for chatbot intent classification"""

    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.pipeline = None
        self.intent_labels = get_intent_labels()

    def prepare_training_data(self):
        """
        Prepare training data from the training dataset
        Returns X (texts) and y (intent labels)
        """
        samples = get_all_training_samples()

        # Separate features and labels
        X = [sample[0] for sample in samples]
        y = [sample[1] for sample in samples]

        print(f"Loaded {len(X)} training samples across {len(set(y))} intents")

        return X, y

    def create_model(self):
        """
        Create the machine learning pipeline
        Uses TF-IDF vectorization + Multinomial Naive Bayes
        """
        # Create pipeline with TF-IDF vectorizer and Naive Bayes classifier
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                ngram_range=(1, 3),  # Use unigrams, bigrams, and trigrams
                max_features=5000,
                min_df=1,
                max_df=0.8,
                lowercase=True,
                strip_accents='unicode',
                stop_words='english'
            )),
            ('classifier', MultinomialNB(alpha=0.1))
        ])

        return self.pipeline

    def train(self, X, y, test_size=0.2, random_state=42):
        """
        Train the intent classification model

        Args:
            X: Training texts
            y: Intent labels
            test_size: Proportion of data for testing
            random_state: Random seed for reproducibility
        """
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )

        print(f"Training set: {len(X_train)} samples")
        print(f"Test set: {len(X_test)} samples")

        # Create and train the model
        self.create_model()
        print("\nTraining the model...")
        self.pipeline.fit(X_train, y_train)

        # Evaluate on test set
        print("\nEvaluating model performance...")
        y_pred = self.pipeline.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        print(f"\nTest Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")

        # Cross-validation
        print("\nPerforming 5-fold cross-validation...")
        cv_scores = cross_val_score(self.pipeline, X, y, cv=5)
        print(f"Cross-validation scores: {cv_scores}")
        print(f"Average CV accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

        # Detailed classification report
        print("\n" + "="*60)
        print("CLASSIFICATION REPORT")
        print("="*60)
        print(classification_report(y_test, y_pred))

        # Confusion matrix
        print("\n" + "="*60)
        print("CONFUSION MATRIX")
        print("="*60)
        cm = confusion_matrix(y_test, y_pred, labels=self.intent_labels)
        print(cm)

        return accuracy, y_test, y_pred

    def save_model(self, model_path='models/chatbot_intent_classifier.pkl'):
        """
        Save the trained model to disk

        Args:
            model_path: Path to save the model
        """
        # Create models directory if it doesn't exist
        os.makedirs(os.path.dirname(model_path), exist_ok=True)

        # Save the entire pipeline
        with open(model_path, 'wb') as f:
            pickle.dump(self.pipeline, f)

        print(f"\nModel saved to {model_path}")

    def load_model(self, model_path='models/chatbot_intent_classifier.pkl'):
        """
        Load a trained model from disk

        Args:
            model_path: Path to the saved model
        """
        with open(model_path, 'rb') as f:
            self.pipeline = pickle.load(f)

        print(f"Model loaded from {model_path}")
        return self.pipeline

    def predict_intent(self, text):
        """
        Predict the intent of a given text

        Args:
            text: Input text

        Returns:
            Predicted intent label
        """
        if self.pipeline is None:
            raise ValueError("Model not trained or loaded. Please train or load a model first.")

        return self.pipeline.predict([text])[0]

    def predict_intent_with_confidence(self, text):
        """
        Predict intent with confidence scores

        Args:
            text: Input text

        Returns:
            Dictionary with predicted intent and confidence scores for all intents
        """
        if self.pipeline is None:
            raise ValueError("Model not trained or loaded. Please train or load a model first.")

        # Get probability scores for all intents
        proba = self.pipeline.predict_proba([text])[0]

        # Get the predicted intent
        predicted_intent = self.pipeline.predict([text])[0]

        # Create confidence scores dictionary
        intent_scores = {}
        for intent, score in zip(self.pipeline.classes_, proba):
            intent_scores[intent] = float(score)

        return {
            'intent': predicted_intent,
            'confidence': float(max(proba)),
            'all_scores': intent_scores
        }

    def test_predictions(self, test_texts):
        """
        Test the model on a list of sample texts

        Args:
            test_texts: List of texts to test
        """
        print("\n" + "="*60)
        print("TESTING PREDICTIONS")
        print("="*60)

        for text in test_texts:
            result = self.predict_intent_with_confidence(text)
            print(f"\nInput: '{text}'")
            print(f"Predicted Intent: {result['intent']}")
            print(f"Confidence: {result['confidence']:.4f} ({result['confidence']*100:.2f}%)")

            # Show top 3 intents
            sorted_scores = sorted(result['all_scores'].items(), key=lambda x: x[1], reverse=True)[:3]
            print("Top 3 intents:")
            for intent, score in sorted_scores:
                print(f"  - {intent}: {score:.4f} ({score*100:.2f}%)")


def train_and_save_model():
    """
    Main function to train and save the chatbot intent classifier
    """
    print("="*60)
    print("CHATBOT INTENT CLASSIFIER TRAINING")
    print("="*60)

    # Initialize trainer
    trainer = ChatbotMLTrainer()

    # Prepare training data
    X, y = trainer.prepare_training_data()

    # Train the model
    accuracy, y_test, y_pred = trainer.train(X, y)

    # Save the model
    model_path = os.path.join(os.path.dirname(__file__), '../../models/chatbot_intent_classifier.pkl')
    trainer.save_model(model_path)

    # Test with sample inputs
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

    trainer.test_predictions(test_texts)

    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print(f"Final Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print("="*60)

    return trainer


if __name__ == '__main__':
    # Train and save the model
    trainer = train_and_save_model()
