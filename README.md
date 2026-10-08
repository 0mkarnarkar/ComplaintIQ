# ComplaintIQ 🧠

> AI-powered bank complaint classifier — categorizes complaints, assesses urgency, and routes to the right team.

## Architecture

```
┌──────────────┐     POST /classify     ┌──────────────────────┐
│   Web UI     │ ───────────────────►   │   Flask REST API     │
│  (HTML/JS)   │ ◄───────────────────   │                      │
└──────────────┘     JSON response      │  ┌────────────────┐  │
                                        │  │  TF-IDF +      │  │
                                        │  │  LogReg Model  │  │
                                        │  └────────────────┘  │
                                        └──────────────────────┘
```

## Features

- **5-Class Classification**: Card Issue, UPI Failure, Loan, Account Access, Fraud
- **4-Level Urgency**: Low, Medium, High, Critical
- **Auto-Routing**: Maps category → responsible bank team
- **Confidence Scores**: Per-prediction probability with animated visualization
- **REST API**: `POST /classify` with JSON request/response
- **Web Interface**: Glassmorphism dark-themed UI with animated results
- **Docker**: Production-ready containerization with health checks
- **CI/CD**: GitHub Actions pipeline with tests and Docker smoke test

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py

# Open http://localhost:5000
```

### Docker

```bash
# Build and run
docker-compose up --build

# Or manually
docker build -t complaintiq .
docker run -p 5000:5000 complaintiq
```

### API Usage

```bash
# Classify a complaint
curl -X POST http://localhost:5000/classify \
  -H "Content-Type: application/json" \
  -d '{"complaint": "My card was declined at the ATM even though I have balance"}'

# Response
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

# Health check
curl http://localhost:5000/health

# Force retrain
curl -X POST http://localhost:5000/retrain
```

## ML Pipeline

| Component | Choice |
|-----------|--------|
| Vectorizer | TF-IDF (5000 features, bigrams, sublinear TF) |
| Classifier | Logistic Regression (multinomial, balanced classes) |
| Training Data | 60 samples modeled on CFPB Consumer Complaints |
| Cross-Validation | 3-fold stratified |

## Running Tests

```bash
pytest tests/ -v
```

## Cloud Deployment (IBM Cloud)

See the deployment guide for step-by-step instructions to deploy on IBM Cloud Code Engine.

## Project Structure

```
ComplaintIQ/
├── app.py                      # Flask application
├── model/
│   ├── classifier.py           # TF-IDF + LogReg pipeline
│   └── sample_data.py          # Training dataset
├── templates/
│   └── index.html              # Web interface
├── static/
│   ├── style.css               # Dark theme styles
│   └── script.js               # Frontend logic
├── tests/
│   └── test_api.py             # API tests
├── Dockerfile                  # Container config
├── docker-compose.yml          # Compose config
├── requirements.txt            # Python dependencies
└── .github/workflows/ci.yml    # CI pipeline
```

## License

MIT
