import streamlit as st
import base64
import requests
import pandas as pd
from dotenv import load_dotenv
import os

 
# Sidebar für Navigation
sidebar = st.sidebar.selectbox(
    "Choose a page:",
    ["Home", "Questionnaire", "GitHub API"]
)
 
# Fragebogen-Daten speichern
if 'responses' not in st.session_state:
    st.session_state.responses = []
 
# Home-Seite
if sidebar == "Home":
    st.title("Welcome to GradeBoost! 🚀")
    st.header("Assess and boost your semester performance")
    st.markdown("""
    *Dear Student,*
    *We warmly welcome you to our website. Enter relevant factors and calculate your provisional grade for the semester.*
    *Good luck! 🍀*
    """)
 
# Fragebogen-Seite
elif sidebar == "Questionnaire":
    st.title("Questionnaire")
    st.write("Answer the following questions:")
 
    # Fragebogen mit verschiedenen Eingaben
    age = st.slider("1. How old are you?", 15, 18, 16)
    average_time = st.slider("2. How many hours per week do you study on average?", 0, 25, 12)
    tutoring = st.radio("3. Have you received tutoring?", ["Yes", "No"])
    absences = st.radio("4. How many days were you absent?", ["0-5 days", "6-10 days", "11-15 days", "16-20 days", "21-25 days", "more than 25 days"])
    performance_as = st.select_slider("5. Rate your academic performance:", ["1.0", "2.0", "3.0", "4.0", "5.0", "6.0"])
    ex_activities = st.radio("6. Do you participate in extracurricular activities?", ["Yes", "No"])
 
    # Zusätzliche Auswahl bei extracurricular activities
    if ex_activities == "Yes":
        spec_ex_activities = st.multiselect("Which activities?", ["Sports", "Music", "Volunteering", "Other"])
        if "Other" in spec_ex_activities:
            other_activity = st.text_input("Specify other activities:")
 
    support = st.select_slider("7. Rate the support from your parents:", ["No support", "Low", "Moderate", "High", "Very high"])
    parental_degree = st.radio("8. What is the highest education level your parents completed?", ["No degree", "High School", "Bachelor's", "Master's", "PhD"])
 
    # Neue Frage: Frühere GradeBoost-Nutzung
    previous_activity = st.radio(
        "9. Have you already used GradeBoost this semester? ❗️*Disclaimer: If yes, please provide information about the number of times you used GradeBoost this semester, as well as the calculated grade(s).*",
        options=["Yes", "No"]
    )
   
    grades = []
    if previous_activity == "Yes":
        num_previous_activity = st.selectbox(
            "How many times did you calculate your estimated Grade using GradeBoost this semester?",
            options=[1, 2, 3, 4, 5]
        )
 
        # Textfelder für die vorherigen berechneten Noten
        for i in range(num_previous_activity):
            grade = st.text_input(f'Enter grade {i + 1}:')
            grades.append(grade)
   
    # Zeige die eingegebenen Noten an
    if grades:
        st.write('Entered grades:')
        for i, grade in enumerate(grades):
            st.write(f'Grade {i + 1}: {grade}')
 
    # Daten speichern
    if st.button("Submit"):
        st.session_state.responses.append({
            'Age': age,
            'Study Time': average_time,
            'Tutoring': tutoring,
            'Absences': absences,
            'Performance': performance_as,
            'Extracurricular': ex_activities,
            'Support': support,
            'Parental Degree': parental_degree,
            'Previous Activity': previous_activity,
            'Previous Grades': grades
        })
        st.success("Thank you for your responses!")
 
        # Zeige die neuesten Antworten als Tabelle an
        if len(st.session_state.responses) > 0:
            latest_response = st.session_state.responses[-1]
            st.write("Here are your responses:")
            st.write(pd.DataFrame([latest_response]))  # Konvertiere das Dictionary in ein DataFrame für eine übersichtliche Anzeige
        else:
            st.write("No responses yet.")
