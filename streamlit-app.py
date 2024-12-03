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

    # Personal Information
    st.subheader("Personal Information")
    gender = st.radio("1. What is your gender?", ["Male", "Female"])
    gender_mapping = {"Male": 0, "Female": 1}
    gender_numeric = gender_mapping[gender]

    age = st.slider("2. How old are you?", 15, 18, 16)

    # Academic Information
    st.subheader("Academic Information")
    average_time = st.slider("3. How many hours per week do you study on average?", 0, 25, 12)
    absences = st.slider("4. How many days were you absent?", 0, 30, 5)

    tutoring = st.radio("5. Have you received tutoring?", ["Yes", "No"])
    tutoring_mapping = {"Yes": 1, "No": 0}
    tutoring_numeric = tutoring_mapping[tutoring]

    performance = st.slider("6. What is your current GPA?", min_value=1.0, max_value=6.0, step=0.05)

    # Extracurricular Activities
    st.subheader("Extracurricular Activities")
    activities = st.multiselect(
        "7. Which activities do you participate in?",
        ["Sports", "Music", "Volunteering", "Extracurricular Activities"]
    )
    sports = int("Sports" in activities)
    music = int("Music" in activities)
    volunteering = int("Volunteering" in activities)
    extracurricular = int("Extracurricular Activities" in activities)

    # Parental Support & Education
    st.subheader("Parental Support & Education")
    support = st.select_slider("8. Rate the support from your parents:", ["No support", "Low", "Moderate", "High", "Very high"])
    support_mapping = {"No support": 0, "Low": 1, "Moderate": 2, "High": 3, "Very high": 4}
    support_numeric = support_mapping[support]

    parental_degree = st.radio(
        "9. What is the highest education level your parents completed?", 
        ["No degree", "High School", "Bachelor's", "Master's", "PhD"]
    )
    degree_mapping = {"No degree": 0, "High School": 1, "Bachelor's": 2, "Master's": 3, "PhD": 4}
    parental_degree_numeric = degree_mapping[parental_degree]

    # Save inputs for prediction
    st.session_state.responses = [
        age, gender_numeric, parental_degree_numeric, average_time, absences, tutoring_numeric, 
        support_numeric, extracurricular, sports, music, volunteering, performance
    ]

# Prediction page
if sidebar == "Prediction":
    st.title("Predict Your Grade")
    if st.session_state.responses:
        try:

            scaler = load('scaler.pkl')  # Make sure to load the correct scaler (used during training)

            # Correct the new_data to have 12 features in each row
            new_data = np.array([
                [1, 2, 19.833723, 7, 1, 2, 0, 0, 1, 0, 2.929196, 2.0],
                [1, 18, 0, 1, 15.408756, 0, 0, 1, 0, 0, 0, 3.042915],
                [2, 15, 0, 3, 4.210570, 26, 0, 2, 0, 0, 0, 0.112602],
                [3, 17, 1, 3, 10.028829, 14, 0, 3, 1, 0, 0, 2.054218],
                [4, 17, 1, 2, 4.672495, 17, 1, 3, 0, 0, 0, 1.288061]
            ])

            # Step 2: Apply the scaling to new data (using the previously fitted scaler)
            new_data_scaled = scaler.transform(new_data)  # Use transform to scale new data without fitting again

            # Step 3: Load the pre-trained model (if it's saved)

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

            model = load('random_forest_model.pkl')  # Make sure to load the correct model

            # Step 4: Make predictions using the trained model
            predictions = model.predict(new_data_scaled)
            probabilities = model.predict_proba(new_data_scaled)

        except Exception as e:
            st.error(f"Error loading model or making predictions: {e}")
    else:
        st.warning("Please complete the questionnaire first!")
