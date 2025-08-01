# brain.py
import pickle
import json
from sklearn.feature_extraction.text import TfidfVectorizer

with open("models/intent_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("models/tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)
with open("intents_hinglish.json", "r") as f:
    intents = json.load(f)["intents"]

def predict_intent(text):
    X = vectorizer.transform([text])
    prediction = model.predict(X)[0]
    proba = model.predict_proba(X)[0]
    confidence = max(proba)

    print(f"🔍 Predicted: {prediction}, Confidence: {confidence:.2f}")

    question_keywords = ["what", "who", "when", "where", "why", "how", "explain", "define", "theory", "tell me"]
    if confidence < 0.6 or any(q in text.lower() for q in question_keywords):
        return None
    return prediction
