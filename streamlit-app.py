import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from joblib import load
import plotly.express as px
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Home", layout="wide")


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


if st.button("Go to Questionnaire"):
    switch_page("questionnaire")