import streamlit as st
from auth import get_auth
import pandas as pd
import joblib

if 'authentication_status' not in st.session_state or not st.session_state.authentication_status:
    st.warning("Please login from main app")
    st.stop()

# Load model (add this at the top)
try:
    model_data = joblib.load('model/ckd_rf_model.pkl')
    model = model_data['model']
    feature_names = model_data['feature_names']
except Exception as e:
    st.error(f"Failed to load model: {str(e)}")
    st.stop()

# 2. Page Header
st.title(f"Quick CKD Check for {st.session_state['name']}")
st.markdown("---")

# Add home button in the main content area
col1, col2 = st.columns([5,1])
with col2:
    if st.button("🏠 Home", key="home_btn_main"):
        st.switch_page("pages/1_🏠_Home.py")

# Your existing page content below...
# 3. Your Lite Version Form
with st.form("lite_form"):
    st.subheader("Your Health Background")
    col1, col2 = st.columns(2)
    
    with col1:
        diabetes = st.checkbox("Diagnosed with diabetes?")
        hypertension = st.checkbox("High blood pressure?")
        family_ckd = st.checkbox("Family history of kidney disease?")
    
    with col2:
        heart_disease = st.checkbox("History of heart disease?")
        over_60 = st.checkbox("Over 60 years old?")
        smoker = st.checkbox("Current smoker?")

    st.subheader("Recent Symptoms")
    symptom_col1, symptom_col2 = st.columns(2)
    
    with symptom_col1:
        swelling = st.selectbox("Swelling in legs/face", ["None", "Mild", "Severe"])
        fatigue = st.selectbox("Fatigue level", ["Normal", "Tired often", "Exhausted daily"])
        urination = st.selectbox("Urine changes", ["Normal", "Foamy", "Dark/Red", "Less urine"])
    
    with symptom_col2:
        appetite = st.selectbox("Appetite changes", ["Normal", "Reduced", "Very poor"])
        nausea = st.checkbox("Frequent nausea/vomiting?")
        itchiness = st.checkbox("Unusual skin itchiness?")

    submitted = st.form_submit_button("Check My Risk")

if submitted:
    # Convert inputs to model features
    input_data = {
        'age': 65 if over_60 else 45,
        'bp': 150 if hypertension else 120,
        'al': 2 if urination == "Foamy" else (3 if urination == "Dark/Red" else 0),
        'su': 3 if diabetes else 0,
        'hemo': 10 if fatigue != "Normal" else 14,
        'pcv': 35 if swelling != "None" else 42,
        'bu': 25 if nausea else 12,
        'sc': 1.4 if (family_ckd and over_60) else 0.9,
        'htn': 1 if hypertension else 0,
        'dm': 1 if diabetes else 0
    }

    # Create DataFrame with all expected features
    input_df = pd.DataFrame([input_data])
    input_df = pd.get_dummies(input_df)

    # Ensure all training columns exist
    for col in feature_names:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[feature_names]

    # Get prediction
    proba = model.predict_proba(input_df)[0][1]
    
    # Clinical override rules
    if (not diabetes and 
        not hypertension and 
        urination == "Normal" and 
        swelling == "None"):
        proba = max(proba - 0.3, 0.01)

    # Display results
    st.subheader("Results")
    st.metric("CKD Risk Probability", f"{proba:.0%}")
    
    if proba > 0.7:
        st.error("High risk detected - please consult a doctor")
    elif proba > 0.4:
        st.warning("Moderate risk - consider getting checked")
    else:
        st.success("Low risk detected")