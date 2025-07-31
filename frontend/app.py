import streamlit as st
import requests

# Set page configuration with an app icon, title, and layout style
st.set_page_config(page_title="Bank Churn Prediction", page_icon="💳", layout="wide")

# Custom CSS styling to enhance the app appearance
st.markdown("""
    <style>
    body {
        font-family: 'Helvetica', sans-serif;
        background-color: #F0F4F8;
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
        font-size: 18px;
        border-radius: 10px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>label {
        color: #4A4A4A;
    }
    .stSelectbox>label {
        color: #4A4A4A;
    }
    .stMarkdown {
        font-size: 18px;
        color: #555555;
    }
    .error-message {
        color: #FF6347;
        font-weight: bold;
        font-size: 16px;
    }
    .success-message {
        color: #28a745;
        font-weight: bold;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and introductory message
st.markdown("<h1>Bank Churn Prediction</h1>", unsafe_allow_html=True)
st.markdown("<p class='main'>Predict whether a customer will churn based on their information.</p>", unsafe_allow_html=True)

# Sidebar: Collecting customer details through interactive form inputs
with st.sidebar:
    st.header("Customer Information")
    
    credit_score = st.number_input('Credit Score', min_value=300, max_value=900, value=650)
    geography = st.selectbox('Geography', ['France', 'Spain', 'Germany'])
    gender = st.selectbox('Gender', ['Female', 'Male'])
    age = st.number_input('Age', min_value=18, max_value=100, value=35)
    tenure = st.number_input('Tenure (Years)', min_value=0, max_value=10, value=3)
    balance = st.number_input('Balance', min_value=0.0, value=50000.0)
    num_of_products = st.number_input('Number of Products', min_value=1, max_value=4, value=1)
    has_cr_card = st.selectbox('Has Credit Card', [0, 1])
    is_active_member = st.selectbox('Is Active Member', [0, 1])
    estimated_salary = st.number_input('Estimated Salary', min_value=0.0, value=100000.0)

    submit_button = st.button('Predict Churn')

# Main Area: Display results and visuals
if submit_button:
    # Prepare the data to send to the API
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

    # Send POST request to the prediction API
    try:
        response = requests.post('http://localhost:8000/predict', json=data)
        
        if response.status_code == 200:
            result = response.json()
            churn_probability = result.get('churn_probability', 0.0)
            churned = result.get('churned', False)

            # Display result with interactive elements
            st.markdown(f"<h2>Prediction Result</h2>", unsafe_allow_html=True)
            st.write(f"Churn Probability: **{churn_probability:.2f}**")

            # Use progress bar for visualizing churn probability
            progress = st.progress(churn_probability)

            # Add emojis for better UX
            if churn_probability > 0.7:
                st.markdown("### 🚨 High Risk of Churn 🚨", unsafe_allow_html=True)
            elif churn_probability > 0.4:
                st.markdown("### ⚠️ Moderate Risk of Churn ⚠️", unsafe_allow_html=True)
            else:
                st.markdown("### ✅ Low Risk of Churn ✅", unsafe_allow_html=True)

            # Display customer churn status with emojis
            if churned:
                st.markdown(f"<p class='error-message'>⚠️ This customer is likely to churn.</p>", unsafe_allow_html=True)
                st.image("https://image.shutterstock.com/image-vector/business-woman-running-away-from-boring-260nw-1442371227.jpg", width=200)
            else:
                st.markdown(f"<p class='success-message'>✅ This customer is likely to stay with the bank.</p>", unsafe_allow_html=True)
                st.image("https://image.shutterstock.com/image-vector/success-businessman-high-fiving-colleague-260nw-1066596234.jpg", width=200)

        else:
            st.markdown("<p class='error-message'>❌ Prediction Failed. Please try again later.</p>", unsafe_allow_html=True)
    
    except Exception as e:
        st.markdown(f"<p class='error-message'>⚠️ An error occurred: {e}</p>", unsafe_allow_html=True)

# Footer Section (Optional branding or company attribution)
st.markdown("""
    <footer style='text-align: center; color: #808080; margin-top: 50px;'>
""", unsafe_allow_html=True)
