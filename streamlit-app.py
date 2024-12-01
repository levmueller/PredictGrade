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