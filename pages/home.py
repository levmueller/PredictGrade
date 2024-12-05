import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from joblib import load
import plotly.express as px

st.set_page_config(layout="wide")

# Session state to track responses
if 'responses' not in st.session_state:
    st.session_state.responses = []


st.title("Welcome to GradeBoost! 🚀")
st.header("Assess and boost your semester performance")
st.markdown("""
*Dear Student,*
*We warmly welcome you to our website. Enter relevant factors and calculate your provisional grade for the semester.*
*Good luck! 🍀*
""")


#Switching to the next page (login page) with an interactive button
from streamlit_extras.switch_page_button import switch_page
continue_to_login = st.button("Reserve a Seat")
if continue_to_login:
        switch_page("quesionnaire")

