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
st.header("Analyse and boost your semester performance")
st.markdown("""
*Dear Students and Teachers,*

*We warmly welcome you to our website. This website is designed for students aged 15 to 18 and their teachers living in Switzerland.*
*GradeBoost helps you identify areas where performance may be below average compared to others and provides valuable insights*
*and personalised tips to address these challenges.*
Our mission is to guide you in continuously improving your performance and achieving a successful semester.*
*Good luck! 🍀*
""")


if st.button("Go to Questionnaire"):
    switch_page("questionnaire")
