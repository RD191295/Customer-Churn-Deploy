import streamlit as st
import requests

# --- Page Configuration ---
st.set_page_config(page_title="Bank Churn Prediction", page_icon="💳", layout="wide")

# --- Custom CSS Styling ---
st.markdown("""
    <style>
    body {
        font-family: 'Helvetica', sans-serif;
        background-color: #F7FAFC;
    }
    .main {
        text-align: center;
        color: #2D3748;
    }
    h1 {
        color: #2B6CB0;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 8px;
        padding: 8px 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>label, .stSelectbox>label, .stNumberInput>label {
        color: #4A4A4A;
        font-weight: 600;
    }
    .stMarkdown {
        font-size: 16px;
        color: #444444;
    }
    .error-message {
        color: #FF4C4C;
        font-weight: bold;
        font-size: 16px;
    }
    .success-message {
        color: #2ECC71;
        font-weight: bold;
        font-size: 16px;
    }
    .info-box {
        background-color: #EDF2F7;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border-left: 5px solid #3182CE;
    }
    footer {
        text-align: center;
        font-size: 14px;
        color: #888888;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1>💳 Bank Churn Prediction</h1>", unsafe_allow_html=True)
st.markdown("<p class='main'>Predict whether a customer will churn based on their profile.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("🔍 Input Customer Details")
    
    credit_score = st.number_input('Credit Score', min_value=300, max_value=900, value=650)
    geography = st.selectbox('Geography', ['France', 'Spain', 'Germany'])
    gender = st.selectbox('Gender', ['Female', 'Male'])
    age = st.number_input('Age', min_value=18, max_value=100, value=35)
    tenure = st.number_input('Tenure (Years)', min_value=0, max_value=10, value=3)
    balance = st.number_input('Balance', min_value=0.0, value=50000.0)
    num_of_products = st.number_input('Number of Products', min_value=1, max_value=4, value=1)
    has_cr_card = st.selectbox('Has Credit Card?', [0, 1])
    is_active_member = st.selectbox('Is Active Member?', [0, 1])
    estimated_salary = st.number_input('Estimated Salary', min_value=0.0, value=100000.0)

    submit_button = st.button('🚀 Predict Churn')

# --- Main Area ---
if submit_button:
    data = {
        'CreditScore': credit_score,
        'Geography': geography,
        'Gender': gender,
        'Age': age,
        'Tenure': tenure,
        'Balance': balance,
        'NumOfProducts': num_of_products,
        'HasCrCard': has_cr_card,
        'IsActiveMember': is_active_member,
        'EstimatedSalary': estimated_salary
    }

    # Display input summary
    st.markdown("### 📊 Customer Summary")
    with st.container():
        st.markdown(f"""
        <div class="info-box">
        <strong>Age:</strong> {age} &nbsp;&nbsp;|&nbsp;&nbsp;
        <strong>Geography:</strong> {geography} &nbsp;&nbsp;|&nbsp;&nbsp;
        <strong>Gender:</strong> {gender}<br>
        <strong>Credit Score:</strong> {credit_score} &nbsp;&nbsp;|&nbsp;&nbsp;
        <strong>Balance:</strong> ${balance:,.2f} &nbsp;&nbsp;|&nbsp;&nbsp;
        <strong>Tenure:</strong> {tenure} years<br>
        <strong>Products:</strong> {num_of_products} &nbsp;&nbsp;|&nbsp;&nbsp;
        <strong>Credit Card:</strong> {"Yes" if has_cr_card else "No"} &nbsp;&nbsp;|&nbsp;&nbsp;
        <strong>Active:</strong> {"Yes" if is_active_member else "No"}<br>
        <strong>Estimated Salary:</strong> ${estimated_salary:,.2f}
        </div>
        """, unsafe_allow_html=True)

    # --- API Call ---
    try:
        response = requests.post('https://customer-churn-deploy-phi3.onrender.com/predict', json=data)

        if response.status_code == 200:
            result = response.json()
            churn_probability = result.get('churn_probability', 0.0)
            churned = result.get('churned', False)

            # --- Result Display ---
            st.markdown("### 🧠 Prediction Result")
            st.write(f"**Churn Probability:** `{churn_probability:.2f}`")

            # Progress bar
            st.progress(churn_probability)

            # Message based on risk level
            if churn_probability > 0.7:
                st.markdown("#### 🚨 High Risk of Churn!", unsafe_allow_html=True)
            elif churn_probability > 0.4:
                st.markdown("#### ⚠️ Moderate Risk of Churn", unsafe_allow_html=True)
            else:
                st.markdown("#### ✅ Low Risk of Churn", unsafe_allow_html=True)

            # Emoji & Image Status
            if churned:
                st.markdown(f"<p class='error-message'>⚠️ The customer is likely to churn.</p>", unsafe_allow_html=True)
                st.image("https://image.shutterstock.com/image-vector/business-woman-running-away-from-boring-260nw-1442371227.jpg", width=200)
            else:
                st.markdown(f"<p class='success-message'>🎉 The customer is likely to stay.</p>", unsafe_allow_html=True)
                st.image("https://image.shutterstock.com/image-vector/success-businessman-high-fiving-colleague-260nw-1066596234.jpg", width=200)

        else:
            st.markdown("<p class='error-message'>❌ API request failed. Please try again later.</p>", unsafe_allow_html=True)

    except Exception as e:
        st.markdown(f"<p class='error-message'>⚠️ Error: {e}</p>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<footer>
    <hr>
    <p>© 2025 BankAI Inc. | Made with ❤️ for smarter banking decisions.</p>
</footer>
""", unsafe_allow_html=True)
