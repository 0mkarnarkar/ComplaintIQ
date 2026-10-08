"""
ComplaintIQ — AI-powered bank complaint classifier.
Flask REST API + Web Interface.
"""

import os
import sys
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from model.classifier import predict, train_models  # noqa: E402

# ── App Setup ────────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# ── Train model on startup ──────────────────────────────────────────────
with app.app_context():
    logger.info("Training models on startup (if not already trained)...")
    result = train_models()
    if result:
        logger.info(
            f"Models trained — Category CV Accuracy: {result['category_cv_accuracy']}, "
            f"Urgency CV Accuracy: {result['urgency_cv_accuracy']}"
        )
    else:
        logger.info("Models already trained, skipping.")


# ── Routes ───────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the web interface."""
    return render_template("index.html")


@app.route("/classify", methods=["POST"])
def classify():
    """
    Classify a complaint.

    Request JSON:
        { "complaint": "string" }

    Response JSON:
        {
            "category": "card_issue",
            "category_label": "Card Issue",
            "urgency": "high",
            "urgency_label": "High",
            "confidence": 0.92,
            "category_confidence": 0.95,
            "urgency_confidence": 0.89,
            "routed_to": "Cards & Payments Team"
        }
    """
    data = request.get_json(silent=True)

    if not data or "complaint" not in data:
        return jsonify({"error": "Missing 'complaint' field in request body"}), 400

    complaint_text = data["complaint"].strip()
    if not complaint_text:
        return jsonify({"error": "Complaint text cannot be empty"}), 400

    if len(complaint_text) < 10:
        return jsonify({"error": "Complaint text too short, provide at least 10 characters"}), 400

    try:
        result = predict(complaint_text)
        logger.info(
            f"Classified: category={result['category']}, urgency={result['urgency']}, "
            f"confidence={result['confidence']}"
        )
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Classification error: {e}")
        return jsonify({"error": "Internal classification error"}), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "ComplaintIQ"}), 200


@app.route("/retrain", methods=["POST"])
def retrain():
    """Force retrain models."""
    try:
        result = train_models(force=True)
        return jsonify({"status": "retrained", "metrics": result}), 200
    except Exception as e:
        logger.error(f"Retrain error: {e}")
        return jsonify({"error": str(e)}), 500


# ── Main ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
