"""Tests for ComplaintIQ API."""

import sys
import os
import json
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import app


@pytest.fixture
def client():
    """Create a test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        res = client.get("/health")
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data["status"] == "healthy"
        assert data["service"] == "ComplaintIQ"


class TestClassifyEndpoint:
    def test_classify_card_issue(self, client):
        res = client.post("/classify", json={
            "complaint": "My credit card was charged twice for the same transaction at a restaurant."
        })
        assert res.status_code == 200
        data = json.loads(res.data)
        assert "category" in data
        assert "urgency" in data
        assert "confidence" in data
        assert "routed_to" in data
        assert data["category"] in ["card_issue", "upi_failure", "loan", "account_access", "fraud"]

    def test_classify_fraud(self, client):
        res = client.post("/classify", json={
            "complaint": "Someone stole my card details and made unauthorized purchases totaling $5000 on my account."
        })
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data["category"] == "fraud"

    def test_classify_upi(self, client):
        res = client.post("/classify", json={
            "complaint": "UPI payment failed but money was debited from my account. Transaction shows pending for 3 days."
        })
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data["category"] == "upi_failure"

    def test_classify_loan(self, client):
        res = client.post("/classify", json={
            "complaint": "My home loan interest rate was increased without any prior notice from the bank."
        })
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data["category"] == "loan"

    def test_classify_account_access(self, client):
        res = client.post("/classify", json={
            "complaint": "I cannot log into my net banking account. It says my account is locked after failed attempts."
        })
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data["category"] == "account_access"

    def test_missing_complaint_field(self, client):
        res = client.post("/classify", json={"text": "hello"})
        assert res.status_code == 400

    def test_empty_complaint(self, client):
        res = client.post("/classify", json={"complaint": ""})
        assert res.status_code == 400

    def test_short_complaint(self, client):
        res = client.post("/classify", json={"complaint": "help"})
        assert res.status_code == 400

    def test_no_json_body(self, client):
        res = client.post("/classify")
        assert res.status_code == 400

    def test_confidence_range(self, client):
        res = client.post("/classify", json={
            "complaint": "My debit card is not working at any ATM. It keeps getting rejected."
        })
        data = json.loads(res.data)
        assert 0 <= data["confidence"] <= 1
        assert 0 <= data["category_confidence"] <= 1
        assert 0 <= data["urgency_confidence"] <= 1

    def test_routing_present(self, client):
        res = client.post("/classify", json={
            "complaint": "Unauthorized transaction on my credit card for online shopping I never did."
        })
        data = json.loads(res.data)
        assert data["routed_to"] != ""


class TestRetrainEndpoint:
    def test_retrain_returns_metrics(self, client):
        res = client.post("/retrain")
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data["status"] == "retrained"
        assert "metrics" in data


class TestWebInterface:
    def test_index_page_loads(self, client):
        res = client.get("/")
        assert res.status_code == 200
        assert b"ComplaintIQ" in res.data
