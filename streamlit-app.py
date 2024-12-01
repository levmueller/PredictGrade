import streamlit as st
import base64
import requests
import pandas as pd
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import numpy as np
 
# Lade die .env-Datei
load_dotenv()
 
# Greife auf das GitHub-Token zu
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
 
# GitHub Repository Details
REPO_OWNER = "392000"
REPO_NAME = "student_performance"
FILE_PATH = "Student_performance_data%20_.csv"  # Achte darauf, dass das Leerzeichen als %20 eingefügt wird
 
# Funktion: Lade Datei von GitHub API herunter
def fetch_github_file():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
 
    if response.status_code == 200:
        data = response.json()
        file_content = base64.b64decode(data['content'])
        with open("sample-dataset.csv", "wb") as file:
            file.write(file_content)
        return pd.read_csv("sample-dataset.csv")
    else:
        st.error(f"Error fetching file: {response.status_code}")
        return None
 
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
 
    parental_support = st.select_slider("7. Rate the support from your parents:", ["No support", "Low", "Moderate", "High", "Very high"])
    parental_degree = st.radio("8. What is the highest education level your parents completed?", ["No degree", "High School", "Bachelor's", "Master's", "PhD"])
 
    # Daten speichern
    if st.button("Submit"):
        st.session_state.responses.append({
            'Age': age,
            'Study Time': average_time,
            'Tutoring': tutoring,
            'Absences': absences,
            'Performance': performance_as,
            'Extracurricular': ex_activities,
            'Parental Support': parental_support,  # Update column name to 'Parental Support'
            'Parental Degree': parental_degree
        })
        st.success("Thank you for your responses!")
 
# GitHub API-Seite
elif sidebar == "GitHub API":
    st.title("GitHub API Integration")
    st.write("Fetching the student performance data from GitHub...")
 
    # Daten abrufen
    dataset = fetch_github_file()
 
    if dataset is not None:
        st.write("Here's the data fetched from GitHub:")
        st.dataframe(dataset)
 
# Umwandlung der Werte in numerische Form für das Radar-Diagramm
def transform_data(df):
    # Alter: 15-18 -> 0-1
    df['Age'] = (df['Age'] - 15) / 3
   
    # Study Time: 0-25 -> 0-1
    df['Study Time'] = df['Study Time'] / 25
   
    # Absences: Umwandlung in Zahlen (0-5 days -> 0, 6-10 days -> 1, etc.)
    abs_map = {
        '0-5 days': 0,
        '6-10 days': 1,
        '11-15 days': 2,
        '16-20 days': 3,
        '21-25 days': 4,
        'more than 25 days': 5
    }
    df['Absences'] = df['Absences'].map(abs_map)
   
    # Parental Support: Mappe 'Parental Support' auf eine Skala von 0-1
    support_map = {
        'No support': 0,
        'Low': 0.25,
        'Moderate': 0.5,
        'High': 0.75,
        'Very high': 1
    }
    df['Parental Support'] = df['Parental Support'].map(support_map)
   
    # Parental Education: Umwandlung auf einer Skala von 0-1
    education_map = {
        "No degree": 0,
        "High School": 0.2,
        "Bachelor's": 0.4,
        "Master's": 0.6,
        "PhD": 1
    }
    df['Parental Degree'] = df['Parental Degree'].map(education_map)
   
    # Academic Performance: Mappe akademische Leistung auf eine Skala von 0-1
    performance_map = {
        "1.0": 1,
        "2.0": 0.8,
        "3.0": 0.6,
        "4.0": 0.4,
        "5.0": 0.2,
        "6.0": 0
    }
    df['Performance'] = df['Performance'].map(performance_map)
   
    return df
 
# Erstellen des Netzdiagramms
def radar_chart(data):
    categories = ['Age', 'Parental Support', 'Parental Degree', 'Study Time', 'Absences', 'Performance']  # Use 'Parental Support'
   
    # Überprüfen, ob alle erforderlichen Spalten im DataFrame vorhanden sind
    missing_cols = [col for col in categories if col not in data.columns]
    if missing_cols:
        st.error(f"Missing columns in data: {missing_cols}")
        return
 
    values = data[categories].values.flatten().tolist()
 
    # Radar chart
    num_vars = len(categories)
 
    # Winkel der Kategorien
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
 
    # Wiederhole den ersten Wert, um den Kreis zu schließen
    values += values[:1]
    angles += angles[:1]
 
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='red', alpha=0.25)
    ax.plot(angles, values, color='red', linewidth=2)
 
    ax.set_yticklabels([])  # Keine Y-Achsen-Beschriftungen
    ax.set_xticks(angles[:-1])  # Entfernen des letzten Werts (der wiederholt wird)
    ax.set_xticklabels(categories)
 
    plt.title('Student Performance Radar Chart')
    st.pyplot(fig)
   
# Füge das Radar-Diagramm für die neuesten Antworten hinzu
if len(st.session_state.responses) > 0:
    latest_response = st.session_state.responses[-1]
    transformed_data = transform_data(pd.DataFrame([latest_response]))
    radar_chart(transformed_data)
