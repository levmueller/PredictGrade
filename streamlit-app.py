import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from joblib import load
import plotly.express as px

# Sidebar for navigation
sidebar = st.sidebar.selectbox(
    "Choose a page:",
    ["Home", "Questionnaire", "Prediction"]
)

# Session state to track responses
if 'responses' not in st.session_state:
    st.session_state.responses = []

# Home page
if sidebar == "Home":
    st.title("Welcome to GradeBoost! 🚀")
    st.header("Assess and boost your semester performance")
    st.markdown("""
    *Dear Student,*
    *We warmly welcome you to our website. Enter relevant factors and calculate your provisional grade for the semester.*
    *Good luck! 🍀*
    """)

# Questionnaire page
if sidebar == "Questionnaire":
    st.title("Questionnaire")
    st.write("Please answer the following questions to calculate your expected grade.")
    # Inputs for the model
    age = st.slider("Age:", 15, 18, 16)
    gender = st.radio("Gender:", ["Male", "Female"])
    average_time = st.slider("Weekly Study Time (hours):", 0, 25, 12)
    absences = st.slider("Number of Absences:", 0, 30, 5)
    tutoring = st.radio("Received Tutoring:", ["Yes", "No"])
    performance = st.slider("Current GPA:", 1.0, 6.0, 3.0)
    extracurricular = st.multiselect("Extracurricular Activities:", ["Sports", "Music", "Volunteering", "Other"])
    parental_support = st.select_slider("Parental Support:", ["None", "Low", "Moderate", "High", "Very High"])
    parental_degree = st.radio("Parental Education Level:", ["No degree", "High School", "Bachelor's", "Master's", "PhD"])

    # Mapping inputs to numeric values for the model
    gender_numeric = {"Male": 0, "Female": 1}[gender]
    tutoring_numeric = {"Yes": 1, "No": 0}[tutoring]
    parental_support_numeric = {"None": 0, "Low": 1, "Moderate": 2, "High": 3, "Very High": 4}[parental_support]
    parental_degree_numeric = {"No degree": 0, "High School": 1, "Bachelor's": 2, "Master's": 3, "PhD": 4}[parental_degree]
    extracurricular_numeric = int(len(extracurricular) > 0)  # Example: 1 if activities exist, 0 otherwise

    # Save inputs for prediction
    st.session_state.responses = [
        age, gender_numeric, average_time, absences, tutoring_numeric, performance, 
        extracurricular_numeric, parental_support_numeric, parental_degree_numeric
    ]

# Prediction page
if sidebar == "Prediction":
    st.title("Predict Your Grade")
    
    if st.session_state.responses:
        # Step 1: Load the pre-trained scaler and model
        try:
            scaler = load('scaler.pkl')  # Load scaler

            def reassemble_file(output_file, chunk_files):
                with open(output_file, 'wb') as output:
                    for chunk_file in chunk_files:
                        with open(chunk_file, 'rb') as file:
                            output.write(file.read())

            chunk_files = [
                'random_forest_model.pkl.part0',
                'random_forest_model.pkl.part1',
                # Add other parts if applicable
            ]
            reassemble_file('random_forest_model.pkl', chunk_files)
                    

            model = load('random_forest_model.pkl')  # Load model
            
            # Step 2: Prepare and scale input
            input_data = np.array([st.session_state.responses])
            input_scaled = scaler.transform(input_data)
            
            # Step 3: Predict grade and probabilities
            prediction = model.predict(input_scaled)[0]
            probabilities = model.predict_proba(input_scaled)[0]
            
            # Step 4: Grade mapping
            grade_mapping = {0: 6, 1: 5, 2: 4, 3: 3, 4: 2}
            predicted_grade = grade_mapping[prediction]
            
            # Display results
            st.subheader(f"Predicted Grade: **{predicted_grade}**")
            st.write(f"Probability Distribution:")
            
            # Step 5: Pie chart for probabilities
            prob_df = pd.DataFrame({
                "Grade": [grade_mapping[i] for i in range(len(probabilities))],
                "Probability": probabilities
            })
            fig = px.pie(
                prob_df, 
                names='Grade', 
                values='Probability', 
                title="Probability Distribution of Predicted Grades",
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            st.plotly_chart(fig, use_container_width=True)
        
        except Exception as e:
            st.error(f"Error loading model or making predictions: {e}")
    else:
        st.warning("Please complete the questionnaire first!")
