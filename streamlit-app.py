import streamlit as st


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


import streamlit as st
import plotly.express as px
import pandas as pd





# Data
categories = [
    "Age",
    "Parental Education",
    "Study Time Weekly",
    "Absences",
    "Parental Support"
]
values = [16.46864548, 1.746237458, 9.771991919, 14.54138796, 2.122073579]

# Duplicate the first value to close the radar chart
categories += [categories[0]]
values += [values[0]]

# Plot radar chart
fig = px.line_polar(
    r=values,
    theta=categories,
    line_close=True
)

# Customize only the radar chart background
fig.update_layout(
    polar=dict(
        bgcolor="gray",  # Background of the radar chart itself
    )
)

# Display in Streamlit
st.title("Netzdiagram Example")
st.plotly_chart(fig, use_container_width=True)
