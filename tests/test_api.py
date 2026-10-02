# Project root ka path Python ko batane ke liye os aur sys import karna
import os
import sys
# Project root directory ko Python path mein add karna
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



# FastAPI application ko test karne ke liye TestClient import karna
from fastapi.testclient import TestClient
# API application ko import karna
from api.main import app


# FastAPI app ka test client banana
client = TestClient(app)

# FastAPI application ko test karne ke liye TestClient import karna
from fastapi.testclient import TestClient

# API application ko import karna
from api.main import app

# FastAPI app ka test client banana
client = TestClient(app)



# Health endpoint ko test karna
def test_health():

    # /health endpoint par GET request bhejna
    response = client.get("/health")

    # Check karna ke response successful hai
    assert response.status_code == 200

    # Check karna ke API expected response de rahi hai
    assert response.json() == {"status": "ok"}



# Model information endpoint ko test karna
def test_model_info():

    # /model/info endpoint par GET request bhejna
    response = client.get("/model/info")

    # Check karna ke response successful hai
    assert response.status_code == 200

    # Check karna ke model ki basic information correct hai
    assert response.json() == {
        "model": "Logistic Regression",
        "problem": "Customer Churn Prediction",
        "target": "Churn"
    }



    # Prediction endpoint ko test karna
def test_predict():

    # Sample customer data banana
    customer_data = {
        "gender": "Male",
        "SeniorCitizen": 0,
        "Partner": "Yes",
        "Dependents": "No",
        "tenure": 12,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "DSL",
        "OnlineSecurity": "No",
        "OnlineBackup": "Yes",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 70.35,
        "TotalCharges": 844.2
    }

    # /predict endpoint par POST request bhejna
    response = client.post("/predict", json=customer_data)

    # Check karna ke response successful hai
    assert response.status_code == 200

    # Response ko dictionary mein convert karna
    result = response.json()

    # Check karna ke required keys response mein maujood hain
    assert "churn_prediction" in result
    assert "churn_probability" in result





    # Invalid customer data ko test karna
def test_predict_invalid_input():

    # Intentionally incomplete data dena
    invalid_data = {
        "gender": "Male"
    }

    # /predict endpoint par invalid request bhejna
    response = client.post("/predict", json=invalid_data)

    # FastAPI validation error expected hai
    assert response.status_code == 422