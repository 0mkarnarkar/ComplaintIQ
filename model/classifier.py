"""
ComplaintIQ Classifier
TF-IDF + Logistic Regression pipeline for complaint classification.
Trains on sample data (or CFPB data if available) and exposes a predict() function.
"""

import os
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score

MODEL_DIR = os.path.join(os.path.dirname(__file__))
CATEGORY_MODEL_PATH = os.path.join(MODEL_DIR, "category_model.pkl")
URGENCY_MODEL_PATH = os.path.join(MODEL_DIR, "urgency_model.pkl")

# Human-readable labels
CATEGORY_LABELS = {
    "card_issue": "Card Issue",
    "upi_failure": "UPI Failure",
    "loan": "Loan",
    "account_access": "Account Access",
    "fraud": "Fraud",
}

URGENCY_LABELS = {
    "low": "Low",
    "medium": "Medium",
    "high": "High",
    "critical": "Critical",
}

# Routing map — which team handles each category
ROUTING_MAP = {
    "card_issue": "Cards & Payments Team",
    "upi_failure": "Digital Payments Team",
    "loan": "Lending & Collections Team",
    "account_access": "Core Banking Operations",
    "fraud": "Fraud Investigation Unit",
}


def _build_pipeline():
    """Build a TF-IDF + Logistic Regression pipeline."""
    return Pipeline([
        ("tfidf", TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words="english",
            sublinear_tf=True,
        )),
        ("clf", LogisticRegression(
            max_iter=1000,
            C=5.0,
            solver="lbfgs",
            multi_class="multinomial",
            class_weight="balanced",
        )),
    ])


def train_models(force=False):
    """
    Train category and urgency models using sample data.
    Returns cross-validation accuracy for both models.
    """
    if not force and os.path.exists(CATEGORY_MODEL_PATH) and os.path.exists(URGENCY_MODEL_PATH):
        return None  # Already trained

    from model.sample_data import get_training_data
    texts, categories, urgencies = get_training_data()

    # Train category classifier
    cat_pipeline = _build_pipeline()
    cat_scores = cross_val_score(cat_pipeline, texts, categories, cv=3, scoring="accuracy")
    cat_pipeline.fit(texts, categories)
    joblib.dump(cat_pipeline, CATEGORY_MODEL_PATH)

    # Train urgency classifier
    urg_pipeline = _build_pipeline()
    urg_scores = cross_val_score(urg_pipeline, texts, urgencies, cv=3, scoring="accuracy")
    urg_pipeline.fit(texts, urgencies)
    joblib.dump(urg_pipeline, URGENCY_MODEL_PATH)

    return {
        "category_cv_accuracy": round(float(np.mean(cat_scores)), 4),
        "urgency_cv_accuracy": round(float(np.mean(urg_scores)), 4),
    }


def _load_model(path):
    """Load a pickled model pipeline, auto-training if missing or corrupted."""
    if not os.path.exists(path):
        train_models(force=True)
    try:
        return joblib.load(path)
    except Exception:
        train_models(force=True)
        return joblib.load(path)


def predict(complaint_text: str) -> dict:
    """
    Classify a complaint and return category, urgency, confidence, and routing.

    Args:
        complaint_text: The raw complaint narrative.

    Returns:
        dict with keys: category, category_label, urgency, urgency_label,
                        confidence, routed_to
    """
    cat_model = _load_model(CATEGORY_MODEL_PATH)
    urg_model = _load_model(URGENCY_MODEL_PATH)

    # Category prediction
    cat_pred = cat_model.predict([complaint_text])[0]
    cat_proba = cat_model.predict_proba([complaint_text])[0]
    cat_confidence = float(max(cat_proba))

    # Urgency prediction
    urg_pred = urg_model.predict([complaint_text])[0]
    urg_proba = urg_model.predict_proba([complaint_text])[0]
    urg_confidence = float(max(urg_proba))

    # Combined confidence (geometric mean)
    combined_confidence = round((cat_confidence * urg_confidence) ** 0.5, 4)

    return {
        "category": cat_pred,
        "category_label": CATEGORY_LABELS.get(cat_pred, cat_pred),
        "urgency": urg_pred,
        "urgency_label": URGENCY_LABELS.get(urg_pred, urg_pred),
        "confidence": combined_confidence,
        "category_confidence": round(cat_confidence, 4),
        "urgency_confidence": round(urg_confidence, 4),
        "routed_to": ROUTING_MAP.get(cat_pred, "General Support"),
    }
