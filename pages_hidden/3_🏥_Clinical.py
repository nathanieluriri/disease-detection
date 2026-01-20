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
st.title(f"Clinical Analysis for {st.session_state['name']}")
st.markdown("---")

# Add home button in the main content area
col1, col2 = st.columns([5,1])
with col2:
    if st.button("🏠 Home", key="home_btn_main"):
        st.switch_page("pages/1_🏠_Home.py")

# Your existing page content below... 

# 3. Your Clinical Form
with st.form("clinical_form"):
    st.subheader("Clinical Parameters")
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=2, max_value=90, value=45)
        bp = st.number_input("Blood Pressure (mmHg)", min_value=50, max_value=200, value=120)
        sg = st.selectbox("Urine Specific Gravity", [1.005, 1.010, 1.015, 1.020, 1.025])
        al = st.selectbox("Albumin (0-4 scale)", [0, 1, 2, 3, 4])
        su = st.selectbox("Sugar in Urine (0-5 scale)", [0, 1, 2, 3, 4, 5])
        
    with col2:
        rbc = st.selectbox("RBC Appearance", ["normal", "abnormal"])
        pc = st.selectbox("Pus Cells", ["normal", "abnormal"])
        pcc = st.selectbox("Pus Cell Clumps", ["notpresent", "present"])
        hemo = st.number_input("Hemoglobin (g/dL)", min_value=3.0, max_value=17.0, value=12.0)
        pcv = st.number_input("Packed Cell Volume (%)", min_value=9, max_value=60, value=38)
        sc = st.number_input("Serum Creatinine (mg/dL)", min_value=0.5, max_value=10.0, value=0.8)
        bu = st.number_input("Blood Urea Nitrogen (mg/dL)", min_value=5, max_value=100, value=12)

    submitted = st.form_submit_button("Analyze Results")

if submitted:
    # Prepare input data
    input_data = {
        'age': age,
        'bp': bp,
        'sg': sg,
        'al': al,
        'su': su,
        'rbc': rbc,
        'pc': pc,
        'pcc': pcc,
        'hemo': hemo,
        'pcv': pcv,
        'sc': sc,
        'bu': bu
    }
    
    # Create DataFrame with all expected features
    input_df = pd.DataFrame([input_data])
    input_df = pd.get_dummies(input_df)
    
    # Ensure all expected columns exist
    for col in feature_names:
        if col not in input_df.columns:
            input_df[col] = 0
    
    # Reorder columns to match training data
    input_df = input_df[feature_names]
    
    # Make prediction
    proba = model.predict_proba(input_df)[0][1]
    prediction = 1 if proba > 0.7 else 0
    
    # Display results
    st.subheader("Results")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("CKD Probability", f"{proba:.0%}")
        if prediction == 1:
            st.error("CKD Detected")
        else:
            st.success("No CKD Detected")
    
    with col2:
        st.write("Key Factors:")
        importances = pd.Series(model.feature_importances_, index=feature_names)
        top_factors = importances.nlargest(3)
        for factor, weight in top_factors.items():
            st.write(f"- {factor}: {weight*100:.1f}%")