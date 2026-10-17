from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
MODEL_PATH = Path(__file__).parent / "models" / "churn_model.pkl"
PREPROCESSOR_PATH = Path(__file__).parent / "models" / "preprocessor.pkl"  # adjust folder if different
THRESHOLD = 0.5  # change to your chosen decision threshold

# set_page_config must be the first Streamlit command
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="centered",
)

# Compact, readable styling (good for screenshots and demo videos)
st.markdown(
    """
    <style>
    .block-container { max-width: 860px; padding-top: 2rem; padding-bottom: 3rem; }
    label, .stSelectbox label, .stNumberInput label { font-size: 0.95rem !important; }
    .result-badge {
        display: inline-block; padding: 0.35rem 0.9rem; border-radius: 999px;
        font-weight: 600; font-size: 1rem;
    }
    .badge-low    { background: #e6f4ea; color: #1e7e34; }
    .badge-medium { background: #fff4e0; color: #b26a00; }
    .badge-high   { background: #fde8e8; color: #c0392b; }
    .signal { padding: 0.25rem 0; font-size: 0.97rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# MODEL
# ---------------------------------------------------------
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH), joblib.load(PREPROCESSOR_PATH)


try:
    model, preprocessor = load_model()
except FileNotFoundError as e:
    st.error(f"Model file not found: {e.filename}. Check the path and that the file is pushed to GitHub.")
    st.stop()
except Exception as e:
    st.error(f"Could not load the model: {e}")
    st.stop()


def predict_local(data: dict):
    """Returns (prediction 0/1, churn probability)."""
    df = pd.DataFrame([data])
    X = preprocessor.transform(df)
    prob = float(model.predict_proba(X)[0][1])
    return int(prob >= THRESHOLD), prob


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------
def risk_band(prob: float):
    """UI-only display bands (the model's own decision uses THRESHOLD)."""
    if prob < 0.30:
        return "Low risk", "badge-low"
    if prob < 0.60:
        return "Medium risk", "badge-medium"
    return "High risk", "badge-high"


def yes_no(label: str, key: str, disabled_value: str | None = None) -> str:
    """Yes/No select. If the parent service is off, lock to the 'No ... service' value."""
    if disabled_value:
        st.selectbox(label, [disabled_value], disabled=True, key=f"{key}_locked")
        return disabled_value
    return st.selectbox(label, ["Yes", "No"], key=key)


def build_signals(d: dict) -> list[tuple[str, str]]:
    """
    Simple rule-based signals from the inputs.
    These are NOT model explanations (no SHAP); they highlight well-known churn patterns.
    Returns a list of (kind, text) where kind is 'risk' or 'protect'.
    """
    s = []

    if d["tenure"] < 12:
        s.append(("risk", "Short tenure (under 12 months)"))
    elif d["tenure"] >= 24:
        s.append(("protect", "Long tenure (24+ months)"))

    if d["Contract"] == "Month-to-month":
        s.append(("risk", "Month-to-month contract"))
    else:
        s.append(("protect", f"{d['Contract']} contract"))

    if d["MonthlyCharges"] >= 80:
        s.append(("risk", "High monthly charges"))
    elif d["MonthlyCharges"] < 40:
        s.append(("protect", "Low monthly charges"))

    if d["InternetService"] == "Fiber optic":
        s.append(("risk", "Fiber optic internet"))

    if d["PaymentMethod"] == "Electronic check":
        s.append(("risk", "Pays by electronic check"))

    if d["InternetService"] != "No":
        if d["TechSupport"] == "No":
            s.append(("risk", "No tech support"))
        if d["OnlineSecurity"] == "No":
            s.append(("risk", "No online security"))
        if d["OnlineBackup"] == "No":
            s.append(("risk", "No online backup"))

    return s


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.header("About")
    st.caption(
        "Model trained on the IBM Telco Customer Churn dataset. "
        "The project also includes a FastAPI service, tests and Docker setup on GitHub."
    )


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.title("📊 Customer Churn Prediction")
st.caption("Enter customer details to estimate how likely they are to leave.")


# ---------------------------------------------------------
# INPUTS
# ---------------------------------------------------------
with st.container(border=True):
    st.subheader("👤 Customer profile")
    c1, c2 = st.columns(2)
    with c1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        partner = st.selectbox("Partner", ["Yes", "No"])
        tenure = st.number_input("Tenure (months)", min_value=0, max_value=100, value=12)
    with c2:
        senior = st.selectbox(
            "Senior citizen",
            [0, 1],
            format_func=lambda x: "Yes" if x == 1 else "No",
        )
        dependents = st.selectbox("Dependents", ["Yes", "No"])

with st.container(border=True):
    st.subheader("📞 Services")
    c1, c2 = st.columns(2)
    with c1:
        phone_service = st.selectbox("Phone service", ["Yes", "No"])
        if phone_service == "No":
            st.selectbox("Multiple lines", ["No phone service"], disabled=True, key="ml_locked")
            multiple_lines = "No phone service"
        else:
            multiple_lines = st.selectbox("Multiple lines", ["No", "Yes"], key="ml")
    with c2:
        internet_service = st.selectbox("Internet service", ["DSL", "Fiber optic", "No"])

    net_off = "No internet service" if internet_service == "No" else None

    c1, c2 = st.columns(2)
    with c1:
        online_security = yes_no("Online security", "os", net_off)
        online_backup = yes_no("Online backup", "ob", net_off)
        device_protection = yes_no("Device protection", "dp", net_off)
    with c2:
        tech_support = yes_no("Tech support", "ts", net_off)
        streaming_tv = yes_no("Streaming TV", "stv", net_off)
        streaming_movies = yes_no("Streaming movies", "smv", net_off)

with st.container(border=True):
    st.subheader("💳 Contract and billing")
    c1, c2 = st.columns(2)
    with c1:
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        paperless_billing = st.selectbox("Paperless billing", ["Yes", "No"])
        payment_method = st.selectbox(
            "Payment method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)",
            ],
        )
    with c2:
        monthly_charges = st.number_input("Monthly charges", min_value=0.0, value=70.35, step=1.0)
        total_charges = st.number_input("Total charges", min_value=0.0, value=844.20, step=10.0)

predict_button = st.button("🔍 Predict churn", type="primary", use_container_width=True)


# ---------------------------------------------------------
# PREDICTION
# ---------------------------------------------------------
if predict_button:
    customer_data = {
        "gender": gender,
        "SeniorCitizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": int(tenure),
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,
        "MonthlyCharges": float(monthly_charges),
        "TotalCharges": float(total_charges),
    }

    try:
        with st.spinner("Calculating churn probability..."):
            prediction, probability = predict_local(customer_data)

        st.session_state["result"] = {
            "prediction": prediction,
            "probability": probability,
            "signals": build_signals(customer_data),
        }
    except Exception as e:
        st.error(f"Prediction failed: {e}")


# ---------------------------------------------------------
# RESULT
# ---------------------------------------------------------
if "result" in st.session_state:
    res = st.session_state["result"]
    prob = res["probability"]
    band_text, band_class = risk_band(prob)

    st.divider()
    st.header("Prediction result")

    with st.container(border=True):
        m1, m2 = st.columns(2)
        m1.metric("Churn probability", f"{prob * 100:.2f}%")
        m2.metric(
            "Prediction",
            "Likely to churn" if res["prediction"] == 1 else "Likely to stay",
        )

        st.progress(min(max(prob, 0.0), 1.0))
        st.markdown(
            f'<span class="result-badge {band_class}">{band_text}</span>',
            unsafe_allow_html=True,
        )

        if res["prediction"] == 1:
            st.error("This customer is likely to churn. Consider a retention offer or a contract upgrade.")
        else:
            st.success("This customer is likely to stay.")

    with st.expander("💡 Key customer signals", expanded=True):
        st.caption(
            "Common churn patterns found in this customer's inputs. "
            "These are simple rules, not the model's exact reasoning."
        )
        for kind, text in res["signals"]:
            icon = "🔺" if kind == "risk" else "🟢"
            st.markdown(f'<div class="signal">{icon} {text}</div>', unsafe_allow_html=True)