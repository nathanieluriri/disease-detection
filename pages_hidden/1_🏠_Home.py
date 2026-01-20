# pages/1_🏠_Home.py
import streamlit as st
from PIL import Image

# 1. Authentication check (must remain first command)
if 'authentication_status' not in st.session_state or not st.session_state.authentication_status:
    st.warning("Please login from main app")
    st.stop()

# 2. Custom CSS loading
try:
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Custom styles not loaded")

# 3. Page content (your existing layout)
st.title(f"👋 Welcome back, {st.session_state['name']}!")
st.title("Kidney Health Companion")

# ... [rest of your home page content] ...

# Hero Section
col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("""
    ### Early Detection Saves Lives
    Assess your kidney health risk with our:
    - 🚀 5-minute Lite Check  
    - 🏥 Comprehensive Clinical Analysis
    """)
    
with col2:
    try:
        img = Image.open("image/fnalkidney-comp_1087847875.png")  # Changed from ../image/
        st.image(img, caption="Kidney Health Matters", width=300)
    except FileNotFoundError:
        st.warning("Kidney image not found")

# Feature Cards
st.divider()
col3, col4 = st.columns(2)
with col3:
    with st.container(border=True):
        st.markdown("### Lite Symptom Check")
        st.write("For quick risk assessment without medical data")
        if st.button("Start Lite Check"):
           st.switch_page("pages/2_💡_Lite_Check.py")  # Correct format


with col4:
    with st.container(border=True):
        st.markdown("### Full Clinical Analysis")
        st.write("For users with lab test results available")
        if st.button("Go to Clinical Mode"):
           st.switch_page("pages/3_🏥_Clinical.py")  # Correct format

