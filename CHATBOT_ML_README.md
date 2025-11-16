# DialSmart Chatbot with Machine Learning

## Overview

The DialSmart chatbot has been upgraded with **machine learning-powered intent classification** and **intelligent phone recommendations** based on detailed specifications from the database.

## Features

### 1. ML-Based Intent Classification
- **14 Intent Categories**: greeting, budget_query, recommendation, comparison, specification, brand_query, usage_type, feature_query, camera_query, performance_query, battery_query, display_query, storage_query, help
- **TF-IDF Vectorization** with Naive Bayes classifier
- **Fallback to keyword matching** if ML model is not available or confidence is low
- **275+ training samples** across all intents

### 2. Smart Recommendation Engine
The chatbot now uses specification-based filtering to recommend phones intelligently:

- **Budget filtering**: Find phones within specific price ranges
- **Brand filtering**: Show phones from specific manufacturers
- **Usage-based recommendations**:
  - Gaming (high refresh rate, powerful processor, good RAM)
  - Photography (high MP cameras, multiple lenses)
  - Business (good battery, 5G, performance)
  - Entertainment (large screen, AMOLED, good battery)
  - Social Media (good cameras, performance)
- **Feature filtering**: 5G, wireless charging, water resistance, expandable storage, etc.
- **Performance filtering**: Flagship processors, high RAM
- **Camera filtering**: High MP, specific camera features
- **Battery filtering**: Large capacity, fast charging
- **Display filtering**: AMOLED, high refresh rate, large screens
- **Storage filtering**: Specific storage capacities

### 3. Response Templates
Dynamic, context-aware responses that:
- Vary based on intent
- Include personalized recommendations
- Provide helpful guidance when information is missing
- Use natural, conversational language

## Training the Model

### First Time Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Train the model**:
   ```bash
   python train_chatbot_model.py
   ```

   This will:
   - Load 275+ training samples from `data/chatbot_training_data.py`
   - Train a TF-IDF + Naive Bayes classifier
   - Evaluate model performance with cross-validation
   - Save the model to `models/chatbot_intent_classifier.pkl`
   - Display sample predictions

### Retraining the Model

To retrain the model (e.g., after adding more training data):

```bash
python train_chatbot_model.py
```

## Training Data Structure

### Training Data File: `data/chatbot_training_data.py`

Contains Python dictionaries mapping intents to example phrases:

```python
TRAINING_DATA = {
    'greeting': [
        "hello",
        "hi",
        "hey there",
        ...
    ],
    'budget_query': [
        "phones under rm2000",
        "cheap phones",
        ...
    ],
    ...
}
```

### Training Questions CSV: `data/chatbot_training_questions.csv`

CSV file with question examples, their intents, and expected actions:

```csv
question,intent,expected_action
"hello","greeting","greet_user"
"show me phones under rm2000","budget_query","filter_by_budget"
...
```

## Adding New Intents or Training Data

1. **Edit `data/chatbot_training_data.py`**:
   - Add new intent category
   - Add training examples for the intent

2. **Update `app/modules/chatbot_responses.py`**:
   - Add response templates for the new intent

3. **Update `app/modules/chatbot.py`**:
   - Add handler for the new intent in `_generate_response()` method

4. **Retrain the model**:
   ```bash
   python train_chatbot_model.py
   ```

## How the Chatbot Works

1. **User sends a message** to the chatbot
2. **Intent Detection**:
   - ML model predicts intent with confidence score
   - If confidence > 30%, use ML prediction
   - Otherwise, fall back to keyword matching
3. **Response Generation**:
   - Extract relevant information (budget, brand, features, etc.)
   - Query database using Smart Recommendation Engine
   - Filter phones based on specifications
   - Score and rank results
   - Generate response using templates
4. **Return response** with phone recommendations

## Example Queries

### Budget Queries
- "Show me phones under RM2000"
- "I have a budget of RM1500"
- "Phones between RM1000 and RM3000"

### Usage-Based Queries
- "Best phone for gaming"
- "I need a phone for photography"
- "Phone for business use"

### Brand Queries
- "Show me Samsung phones"
- "What Xiaomi phones do you have?"
- "Apple iPhones"

### Feature Queries
- "Phones with 5G"
- "Waterproof phones"
- "Phones with wireless charging"

### Camera Queries
- "Best camera phone"
- "Phone with 108MP camera"
- "Good selfie camera"

### Performance Queries
- "Fastest phone"
- "Flagship phones"
- "Phones with Snapdragon processor"

### Battery Queries
- "Long battery life phone"
- "Phones with 5000mAh battery"
- "Fast charging phones"

### Display Queries
- "Phones with AMOLED display"
- "120Hz refresh rate phones"
- "Large screen phones"

### Storage Queries
- "Phones with 256GB storage"
- "Expandable storage phones"
- "512GB phones"

### Combined Queries
- "Gaming phone under RM3000"
- "Samsung phones with good camera"
- "5G phones with large battery"

## Files Added/Modified

### New Files
- `data/chatbot_training_data.py` - Training data for ML model
- `data/chatbot_training_questions.csv` - CSV with training questions
- `app/modules/chatbot_ml_trainer.py` - ML training module
- `app/modules/smart_recommendation_engine.py` - Specification-based recommendation engine
- `app/modules/chatbot_responses.py` - Response templates
- `train_chatbot_model.py` - Training script
- `models/chatbot_intent_classifier.pkl` - Trained ML model (generated)

### Modified Files
- `app/modules/chatbot.py` - Updated to use ML and smart recommendations
- `requirements.txt` - Added scikit-learn and numpy

## Model Performance

- **Training samples**: 275
- **Intent categories**: 14
- **Test accuracy**: ~55-65%
- **Cross-validation accuracy**: ~55%

The model performs well on common queries and falls back to keyword matching for edge cases.

## Architecture

```
User Message
    ↓
Intent Detection (ML + Keywords)
    ↓
Information Extraction (Budget, Brand, Features, etc.)
    ↓
Smart Recommendation Engine
    ↓
Database Query (Filter by specifications)
    ↓
Scoring & Ranking
    ↓
Response Generation (Templates)
    ↓
Return to User
```

## Future Improvements

1. **More training data**: Add more examples to improve accuracy
2. **Advanced ML models**: Try deep learning approaches (BERT, transformers)
3. **Context awareness**: Remember previous conversation turns
4. **Multi-intent detection**: Handle queries with multiple intents
5. **Personalization**: Learn user preferences over time
6. **Sentiment analysis**: Understand user satisfaction
7. **Entity extraction**: Better extraction of specs (RAM, storage, etc.)

## Support

For questions or issues, please refer to the main project documentation or contact the development team.
