import streamlit as st
from auth import get_auth
import pandas as pd
import joblib

if 'authentication_status' not in st.session_state or not st.session_state.authentication_status:
    st.warning("Please login from main app")
    st.stop()


from tensorflow.keras.models import load_model # type: ignore

import joblib
import numpy as np
import pandas as pd
import streamlit as st


st.set_page_config(page_title="Heart Disease Prediction",page_icon="💝")
@st.cache_resource()
def predict_new_data(new_data):
    model = load_model("cardio_ann_model.h5")
    scaler= joblib.load("scaler.pkl")
    new_data = scaler.transform(new_data)  # Normalize
    prediction = (model.predict(new_data) > 0.5).astype("int32")
    return prediction
















st.title("Fill in the form to make a prediction")

def get_selectbox_indices():
    # Define the options for each selectbox
    label_dict = {
        "Glucose": "Whats your glucose level like", #set
        "Cholesterol": "Whats your cholesterol level like ", #set
        "Smoking": "Do you smoke frequently", #set
        "physicalActivity": "Have you participated in a Physical activity in the last 30 days", #set
        "Alcohol": "Do you drink alchohol frequently", #set
        "Gender": "Whats your sex", #set

    }
    options_dict = {
        "Glucose": ["Normal", "Above normal","Well Above Normal"], #set
        "Cholesterol": ["Normal", "Above normal","Well Above Normal"], #set
        "Smoking": ["No", "Yes"], #set
        "physicalActivity": ["No", "Yes"], #set
        "Alcohol": ["No", "Yes"], #set
        "Gender": ["Male", "Female"],  # set

    }
    
    # Get the indices of selected options
    selected_indices = {}
    
    for key, options in options_dict.items():
        selected_value = st.selectbox(
            label=label_dict[key],
            options=options,
            key=key
        )
        # Get the index of the selected value
        selected_index = options.index(selected_value)
        selected_indices[key] = selected_index
        
    # Return the dictionary of selected indices
    return selected_indices


def create_number_input():
    # Define the options for each selectbox
    label_dict = {
        "UserAge": "How Old Are you", #set
        "UserHeight": "How Tall Are You In Feet", #set
        "UserWeight": "How Much Do You Weigh In Kilograms", #set
        "sytolicBP": "Enter Your Systolic blood pressure", #set
        "diastolicBP": "Enter Your Diastolic blood pressure", #set
   

    }

    
    # Get the indices of selected options
    selected_indices = {}
    
    for key, options in label_dict.items():
        selected_value = st.number_input(
            label=label_dict[key],
            step=1,
            min_value=1,
            max_value=1000,
            key=key
        )
    
        selected_index = selected_value
        selected_indices[key] = selected_index
        
    # Return the dictionary of selected indices
    return selected_indices

indices = get_selectbox_indices()
numbers = create_number_input()


def create_feature_list(indices,numbers):
    """
    Create a list of features in the desired order:
    Age (days) – 50 (but should be in days, e.g., 50 * 365 if 50 years old)
    Gender – 1 (1 = Female, 2 = Male)
    Height (cm) – 160
    Weight (kg) – 70
    Systolic blood pressure – 120
    Diastolic blood pressure – 80
    Cholesterol – 1 (1 = Normal, 2 = Above normal, 3 = Well above normal)
    Glucose – 0 (1 = Normal, 2 = Above normal, 3 = Well above normal)
    Smoking – 0 (0 = Non-smoker, 1 = Smoker)
    Alcohol intake – 1 (0 = No, 1 = Yes)
    Physical activity – 1 (0 = No, 1 = Yes)
    """
    
    feature_list = [
        numbers['UserAge'] *365,             
        indices['Gender']+1,           
        numbers['UserHeight'],          
        numbers['UserWeight'],             
        numbers['sytolicBP'],             
        numbers['diastolicBP'],  
        indices['Cholesterol']+1,             
        indices['Glucose']+1,
        indices['Smoking'],  
        indices['Alcohol'], 
        indices['physicalActivity'],        
    ]
    
    return feature_list

column_names=['UserAge in days','Gender','UserHeight','UserWeight','sytolicBP','diastolicBP','Cholesterol','Glucose','Smoking','Alcohol','physicalActivity',]
features = create_feature_list(indices=indices,numbers=numbers)

if st.button("Make a prediction"):
    features = np.array([features])
    prediction = predict_new_data(features)
    df = pd.DataFrame([features[0]], columns=column_names)
    st.write("0- No Possibility of Cardio Vascular Disease")
    st.write("1- Possibility of Cardio Vascular Disease")
    st.write(prediction)
    st.write(df)
    print(prediction,type(prediction))