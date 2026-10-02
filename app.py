# Streamlit frontend banane ke liye Streamlit import karna
import streamlit as st

# FastAPI ko request bhejne ke liye requests import karna
import requests


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

# Browser page ka title aur layout set karna
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)


# ---------------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------------

# Main heading display karna
st.title("📊 Customer Churn Prediction")

# User ko project ka short purpose batana
st.write(
    "Enter customer information to predict the customer's "
    "churn probability."
)


# ---------------------------------------------------------
# CUSTOMER INFORMATION
# ---------------------------------------------------------

# Customer information ke liye section heading
st.header("Customer Information")


# Do columns create karna taake frontend clean lage
col1, col2 = st.columns(2)


# ---------------------------------------------------------
# LEFT COLUMN
# ---------------------------------------------------------

with col1:

    # Gender select karna
    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    # Senior citizen select karna
    senior = st.selectbox(
        "Senior Citizen",
        [0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No"
    )

    # Partner information
    partner = st.selectbox(
        "Partner",
        ["Yes", "No"]
    )

    # Dependents information
    dependents = st.selectbox(
        "Dependents",
        ["Yes", "No"]
    )

    # Customer kitne months se service use kar raha hai
    tenure = st.number_input(
        "Tenure (Months)",
        min_value=0,
        value=12
    )

    # Phone service
    phone_service = st.selectbox(
        "Phone Service",
        ["Yes", "No"]
    )

    # Multiple phone lines
    multiple_lines = st.selectbox(
        "Multiple Lines",
        ["No", "Yes", "No phone service"]
    )

    # Internet service type
    internet_service = st.selectbox(
        "Internet Service",
        ["DSL", "Fiber optic", "No"]
    )

    # Online security
    online_security = st.selectbox(
        "Online Security",
        ["Yes", "No", "No internet service"]
    )

    # Online backup
    online_backup = st.selectbox(
        "Online Backup",
        ["Yes", "No", "No internet service"]
    )


# ---------------------------------------------------------
# RIGHT COLUMN
# ---------------------------------------------------------

with col2:

    # Device protection
    device_protection = st.selectbox(
        "Device Protection",
        ["Yes", "No", "No internet service"]
    )

    # Technical support
    tech_support = st.selectbox(
        "Tech Support",
        ["Yes", "No", "No internet service"]
    )

    # TV streaming
    streaming_tv = st.selectbox(
        "Streaming TV",
        ["Yes", "No", "No internet service"]
    )

    # Movie streaming
    streaming_movies = st.selectbox(
        "Streaming Movies",
        ["Yes", "No", "No internet service"]
    )

    # Contract type
    contract = st.selectbox(
        "Contract",
        ["Month-to-month", "One year", "Two year"]
    )

    # Paperless billing
    paperless_billing = st.selectbox(
        "Paperless Billing",
        ["Yes", "No"]
    )

    # Payment method
    payment_method = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )

    # Monthly charges
    monthly_charges = st.number_input(
        "Monthly Charges",
        min_value=0.0,
        value=70.35
    )

    # Total charges
    total_charges = st.number_input(
        "Total Charges",
        min_value=0.0,
        value=844.20
    )


# ---------------------------------------------------------
# PREDICTION BUTTON
# ---------------------------------------------------------

# Predict button
predict_button = st.button(
    "🔍 Predict Churn",
    use_container_width=True
)


# ---------------------------------------------------------
# PREDICTION
# ---------------------------------------------------------

if predict_button:

    # Customer ki sari information ko dictionary mein store karna
    customer_data = {

        "gender": gender,

        "SeniorCitizen": senior,

        "Partner": partner,

        "Dependents": dependents,

        "tenure": tenure,

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

        "MonthlyCharges": monthly_charges,

        "TotalCharges": total_charges
    }


    # FastAPI prediction endpoint
    api_url = "http://127.0.0.1:8000/predict"


    try:

        # FastAPI ko customer data bhejna
        response = requests.post(
            api_url,
            json=customer_data,
            timeout=10
        )


        # Agar API successful response de
        if response.status_code == 200:

            # API response ko dictionary mein convert karna
            result = response.json()


            # Prediction value nikalna
            prediction = result["churn_prediction"]


            # Probability nikalna
            probability = result["churn_probability"]


            # Probability ko percentage mein convert karna
            probability_percentage = probability * 100


            # -------------------------------------------------
            # RESULT
            # -------------------------------------------------

            st.divider()

            st.header("Prediction Result")


            # Do result columns banana
            result_col1, result_col2 = st.columns(2)


            with result_col1:

                # Churn probability display karna
                st.metric(
                    "Churn Probability",
                    f"{probability_percentage:.2f}%"
                )


            with result_col2:

                # Prediction ko readable text mein convert karna
                if prediction == 1:

                    prediction_text = "Likely to Churn"

                else:

                    prediction_text = "Likely to Stay"


                # Prediction display karna
                st.metric(
                    "Churn Prediction",
                    prediction_text
                )


            # -------------------------------------------------
            # PREDICTION MESSAGE
            # -------------------------------------------------

            if prediction == 1:

                # Churn prediction hone par warning show karna
                st.error(
                    "⚠️ This customer is likely to churn."
                )

            else:

                # No churn prediction hone par success message
                st.success(
                    "✅ This customer is likely to stay."
                )


            # -------------------------------------------------
            # WHY DID THE MODEL MAKE THIS PREDICTION?
            # -------------------------------------------------

            with st.expander(
                "💡 Why did the model make this prediction?"
            ):

                st.write(
                    "The model uses the customer's information "
                    "to calculate the churn probability. "
                    "The following customer characteristics "
                    "may help explain the prediction:"
                )


                # Possible contributing factors ki list
                reasons = []


                # Short tenure ko check karna
                if tenure < 12:

                    reasons.append(
                        "• The customer has a relatively short tenure."
                    )


                # Long tenure ko check karna
                if tenure >= 24:

                    reasons.append(
                        "• The customer has been with the company "
                        "for a relatively long time."
                    )


                # Month-to-month contract ko check karna
                if contract == "Month-to-month":

                    reasons.append(
                        "• The customer has a month-to-month contract."
                    )


                # Long-term contract ko check karna
                if contract == "One year":

                    reasons.append(
                        "• The customer has a one-year contract."
                    )


                if contract == "Two year":

                    reasons.append(
                        "• The customer has a two-year contract."
                    )


                # Monthly charges check karna
                if monthly_charges >= 80:

                    reasons.append(
                        "• The customer's monthly charges are relatively high."
                    )


                # Low monthly charges check karna
                if monthly_charges < 40:

                    reasons.append(
                        "• The customer's monthly charges are relatively low."
                    )


                # Internet service check karna
                if internet_service == "Fiber optic":

                    reasons.append(
                        "• The customer uses fiber optic internet service."
                    )


                # Electronic check check karna
                if payment_method == "Electronic check":

                    reasons.append(
                        "• The customer uses electronic check as the payment method."
                    )


                # No tech support check karna
                if tech_support == "No":

                    reasons.append(
                        "• The customer does not have technical support."
                    )


                # No online security check karna
                if online_security == "No":

                    reasons.append(
                        "• The customer does not have online security."
                    )


                # No online backup check karna
                if online_backup == "No":

                    reasons.append(
                        "• The customer does not have online backup."
                    )


                # Agar koi possible factor mila
                if reasons:

                    for reason in reasons:

                        st.write(reason)

                else:

                    st.write(
                        "No specific simple factor was identified "
                        "from the selected customer information."
                    )


                # Important explanation
                st.caption(
                    "Note: These are possible contributing factors "
                    "based on the customer's inputs. They are not "
                    "guaranteed individual reasons for the prediction."
                )


        else:

            # API error display karna
            st.error(
                f"API request failed. Status code: {response.status_code}"
            )


    except requests.exceptions.RequestException:

        # Agar FastAPI server available na ho
        st.error(
            "Could not connect to the FastAPI server. "
            "Please make sure the API is running."
        )