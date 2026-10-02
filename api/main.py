# FastAPI import karna
from fastapi import FastAPI

# Joblib se saved model aur preprocessor load karna
import joblib

# Pandas DataFrame banane ke liye
import pandas as pd

# FastAPI input validation ke liye
from pydantic import BaseModel


# FastAPI application create karna
app = FastAPI(
    title="Customer Churn Prediction API",
    description="API for predicting customer churn",
    version="1.0.0"
)


# Saved preprocessor load karna
preprocessor = joblib.load("models/preprocessor.pkl")

# Saved Logistic Regression model load karna
model = joblib.load("models/churn_model.pkl")

# Customer ki input fields define karna
class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float

# Health check endpoint
@app.get("/health")
def health_check():
    # API running hai ya nahi, ye check karta hai
    return {"status": "ok"}

# Model information endpoint
@app.get("/model/info")
def model_info():
    # API mein use hone wale model ki basic information return karna
    return {
        "model": "Logistic Regression",
        "problem": "Customer Churn Prediction",
        "target": "Churn"
    }

    # Customer churn prediction endpoint
@app.post("/predict")
def predict_churn(customer: CustomerData):

    # Customer input ko dictionary mein convert karna
    customer_data = customer.model_dump()

    # Dictionary ko DataFrame mein convert karna
    customer_df = pd.DataFrame([customer_data])

    # Saved preprocessor se customer data ko transform karna
    customer_processed = preprocessor.transform(customer_df)

    # Trained model se churn prediction lena
    prediction = model.predict(customer_processed)[0]

    # Churn ki probability nikalna
    probability = model.predict_proba(customer_processed)[0][1]

    # Prediction aur probability return karna
    return {
        "churn_prediction": int(prediction),
        "churn_probability": round(float(probability), 4)
    }