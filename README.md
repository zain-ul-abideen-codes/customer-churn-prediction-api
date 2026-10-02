# Customer Churn Prediction API

A beginner-friendly Machine Learning project that predicts whether a telecom customer is likely to **churn (leave the service)** or **stay**.

The project includes:

* Machine Learning model
* Data preprocessing
* Model evaluation
* FastAPI backend
* Swagger API documentation
* API testing with Pytest
* Streamlit frontend
* Docker support

---

## 📌 Project Overview

Customer churn means a customer stops using a company's service.

This project uses customer information such as:

* Contract type
* Tenure
* Monthly charges
* Internet service
* Payment method
* Online security
* Tech support
* And other customer details

The trained Machine Learning model predicts:

```text
0 → Customer is likely to stay
1 → Customer is likely to churn
```

The API also returns a **churn probability**.

For example:

```text
Churn Probability = 0.2977
```

This means the model estimates approximately:

```text
29.77% chance of churn
```

The project currently uses a **0.50 threshold**:

```text
Probability > 0.50 → Churn Prediction = 1
Probability ≤ 0.50 → Churn Prediction = 0
```

---

# 🎯 Project Goals

The main goals of this project are:

1. Understand customer churn data.
2. Clean and preprocess the data.
3. Train a Machine Learning classification model.
4. Evaluate the model.
5. Save the trained model.
6. Build a REST API using FastAPI.
7. Test the API.
8. Create a simple frontend using Streamlit.
9. Containerize the API using Docker.

---

# 🛠️ Tech Stack

## Machine Learning

* Python
* Pandas
* NumPy
* Scikit-learn
* Joblib

## Backend

* FastAPI
* Pydantic
* Uvicorn

## Testing

* Pytest
* HTTPX

## Frontend

* Streamlit
* Requests

## Deployment / Containerization

* Docker

---

# 📊 Dataset

The project uses the **IBM Telco Customer Churn Dataset**.

Dataset size:

```text
7043 rows
21 columns
```

The target column is:

```text
Churn
```

Target values:

```text
No  → 0
Yes → 1
```

### Churn Distribution

```text
No  → 5174 customers
Yes → 1869 customers
```

Approximately:

```text
No  → 73.46%
Yes → 26.54%
```

---

# 🧹 Data Preprocessing

The following preprocessing steps were performed:

### 1. Remove Customer ID

`customerID` is an identifier and is not useful for prediction.

### 2. Convert TotalCharges

`TotalCharges` was initially stored as text, so it was converted into numeric values.

### 3. Separate Features and Target

```text
X → Customer features
y → Churn
```

### 4. Train/Test Split

The dataset was divided into:

```text
80% → Training data
20% → Testing data
```

Stratified splitting was used to maintain the churn class distribution.

### 5. Numerical Features

The numerical features are:

* SeniorCitizen
* tenure
* MonthlyCharges
* TotalCharges

Numerical preprocessing includes:

* Missing value handling
* StandardScaler

### 6. Categorical Features

The remaining customer attributes are categorical.

Categorical preprocessing includes:

* Missing value handling
* One-Hot Encoding

---

# 🤖 Machine Learning Model

The project uses:

```text
Logistic Regression
```

Logistic Regression is a classification algorithm suitable for predicting two classes:

```text
0 → No Churn
1 → Churn
```

The model was trained using the preprocessed training data.

---

# 🔄 Machine Learning Workflow

The complete workflow is:

```text
Raw Dataset
     ↓
Data Cleaning
     ↓
EDA
     ↓
Feature Selection
     ↓
Train/Test Split
     ↓
Preprocessing
     ↓
One-Hot Encoding
     ↓
Scaling
     ↓
Logistic Regression
     ↓
Model Evaluation
     ↓
Save Model
     ↓
FastAPI
     ↓
Streamlit Frontend
     ↓
Docker
```

---

# 📈 Model Evaluation

The model was evaluated using:

* Accuracy
* Precision
* Recall
* F1-score
* Confusion Matrix
* ROC-AUC
* PR-AUC

A **Dummy Classifier** was also used as a baseline to compare the trained model against a simple majority-class prediction.

---

# 💾 Saved Models

The trained files are stored inside:

```text
models/
```

Files:

```text
models/
├── preprocessor.pkl
└── churn_model.pkl
```

### preprocessor.pkl

Contains the preprocessing pipeline used for:

* Missing value handling
* Scaling
* One-Hot Encoding

### churn_model.pkl

Contains the trained Logistic Regression model.

---

# 🚀 FastAPI Backend

The API is located at:

```text
api/main.py
```

The API provides three main endpoints.

---

## 1. Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

This endpoint checks whether the API is running.

---

## 2. Model Information

```http
GET /model/info
```

Example response:

```json
{
  "model": "Logistic Regression",
  "problem": "Customer Churn Prediction",
  "target": "Churn"
}
```

---

## 3. Churn Prediction

```http
POST /predict
```

This endpoint receives customer information and returns a churn prediction.

### Example Input

```json
{
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
```

### Example Response

```json
{
  "churn_prediction": 0,
  "churn_probability": 0.2977
}
```

### Response Explanation

```text
churn_prediction = 0
```

means the model predicts that the customer is likely to stay.

```text
churn_probability = 0.2977
```

means the model estimates approximately a:

```text
29.77% chance of churn
```

---

# 📋 API Input Features

The API currently requires these 19 customer features:

| Feature          | Description                          |
| ---------------- | ------------------------------------ |
| gender           | Customer gender                      |
| SeniorCitizen    | Whether customer is a senior citizen |
| Partner          | Whether customer has a partner       |
| Dependents       | Whether customer has dependents      |
| tenure           | Number of months with the company    |
| PhoneService     | Whether customer has phone service   |
| MultipleLines    | Multiple phone lines                 |
| InternetService  | Type of internet service             |
| OnlineSecurity   | Online security service              |
| OnlineBackup     | Online backup service                |
| DeviceProtection | Device protection service            |
| TechSupport      | Technical support service            |
| StreamingTV      | Streaming TV service                 |
| StreamingMovies  | Streaming movies service             |
| Contract         | Contract type                        |
| PaperlessBilling | Paperless billing status             |
| PaymentMethod    | Payment method                       |
| MonthlyCharges   | Monthly customer charges             |
| TotalCharges     | Total amount charged                 |

---

# 🖥️ Streamlit Frontend

The project also contains a simple Streamlit frontend.

Frontend file:

```text
app.py
```

The frontend allows the user to enter customer information through a form.

The frontend then:

```text
User Input
    ↓
Streamlit
    ↓
FastAPI
    ↓
ML Model
    ↓
Prediction
    ↓
Streamlit Result
```

The frontend displays:

* Churn prediction
* Churn probability
* Possible contributing factors

The explanation shown in the frontend is a simple rule-based explanation. It should be treated as an understandable guide rather than a complete model-explainability method.

---

# 🧪 API Testing

API tests are located at:

```text
tests/test_api.py
```

The project tests:

### Health Endpoint

```text
/health
```

### Model Information

```text
/model/info
```

### Prediction

```text
/predict
```

### Invalid Input

Checks whether invalid input is handled correctly.

Run tests using:

```powershell
pytest
```

The project currently has:

```text
4 tests
```

and all four tests pass.

---

# 🐳 Docker

The API can also be run inside a Docker container.

Dockerfile:

```text
Dockerfile
```

Docker image:

```text
customer-churn-api
```

Container:

```text
customer-churn-api-container
```

### Build Docker Image

From the project directory:

```powershell
docker build -t customer-churn-api .
```

### Run Container

```powershell
docker run -d -p 8000:8000 --name customer-churn-api-container customer-churn-api
```

### Check API

Open:

```text
http://127.0.0.1:8000/docs
```

### Start Existing Container

```powershell
docker start customer-churn-api-container
```

### Stop Container

```powershell
docker stop customer-churn-api-container
```

---

# 📁 Project Structure

```text
customer-churn-prediction-api/
│
├── api/
│   ├── __init__.py
│   └── main.py
│
├── data/
│   └── WA_Fn-UseC_-Telco-Customer-Churn.csv
│
├── models/
│   ├── preprocessor.pkl
│   └── churn_model.pkl
│
├── notebooks/
│   └── churn_analysis.ipynb
│
├── tests/
│   └── test_api.py
│
├── app.py
├── Dockerfile
├── .gitignore
├── README.md
├── requirements.txt
└── .venv/
```

---

# ⚙️ Installation

## 1. Open Project

```powershell
cd D:\AI-Ml_Roadmap\customer-churn-prediction-api
```

## 2. Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

## 3. Install Requirements

```powershell
pip install -r requirements.txt
```

---

# ▶️ Simple Run Guide

Agar future mein project simply run karna ho, ye steps follow karo.

## Step 1 — Project Folder

```powershell
cd D:\AI-Ml_Roadmap\customer-churn-prediction-api
```

## Step 2 — Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

## Step 3 — FastAPI Start

```powershell
uvicorn api.main:app --reload
```

## Step 4 — Swagger Open

Browser mein:

```text
http://127.0.0.1:8000/docs
```

Yahan API ko test kar sakte ho.

---

## Step 5 — Streamlit Start

Ek **new PowerShell terminal** kholo:

```powershell
cd D:\AI-Ml_Roadmap\customer-churn-prediction-api
```

Virtual environment activate karo:

```powershell
.\.venv\Scripts\Activate.ps1
```

Phir:

```powershell
streamlit run app.py
```

## Step 6 — Frontend Open

Browser mein:

```text
http://localhost:8501
```

Ab customer information enter karke:

```text
Predict Churn
```

button press karo.

---

# 🛑 Project Band Karna

FastAPI ya Streamlit terminal mein:

```text
Ctrl + C
```

press karo.

---

# 🐳 Simple Docker Run

Agar Docker ke through API run karni ho:

```powershell
docker start customer-churn-api-container
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

Docker band karne ke liye:

```powershell
docker stop customer-churn-api-container
```

---

# 📌 Important Commands

### FastAPI

```powershell
uvicorn api.main:app --reload
```

### Streamlit

```powershell
streamlit run app.py
```

### Tests

```powershell
pytest
```

### Docker Build

```powershell
docker build -t customer-churn-api .
```

### Docker Start

```powershell
docker start customer-churn-api-container
```

### Docker Stop

```powershell
docker stop customer-churn-api-container
```

---

# ✅ Project Status

| Component             | Status |
| --------------------- | ------ |
| Data Loading          | ✅      |
| Data Cleaning         | ✅      |
| EDA                   | ✅      |
| Feature Preprocessing | ✅      |
| Train/Test Split      | ✅      |
| Model Training        | ✅      |
| Model Evaluation      | ✅      |
| Baseline Comparison   | ✅      |
| Model Saving          | ✅      |
| FastAPI Backend       | ✅      |
| Swagger Documentation | ✅      |
| API Testing           | ✅      |
| Streamlit Frontend    | ✅      |
| Docker                | ✅      |
| Git/GitHub            | ⏳      |

---

# 🔮 Future Improvements

Possible future improvements include:

* Better model comparison
* Hyperparameter tuning
* Feature selection
* Better model explainability
* SHAP-based explanations
* Improved Streamlit UI
* Cloud deployment
* Database integration
* Authentication
* Monitoring

---

# 📚 What This Project Demonstrates

This project demonstrates a complete beginner-friendly Machine Learning workflow:

```text
Dataset
   ↓
Cleaning
   ↓
EDA
   ↓
Preprocessing
   ↓
Machine Learning
   ↓
Evaluation
   ↓
Model Saving
   ↓
FastAPI
   ↓
Testing
   ↓
Streamlit
   ↓
Docker
```

It therefore covers not only Machine Learning but also the basic process of turning an ML model into a usable application.
