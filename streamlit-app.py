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


import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# Question and User Inputs Section
if sidebar == "Questionnaire":
    st.title("Questionnaire")
    st.write("Please answer the following questions:")

    # Create columns for more structured layout
    col1, col2 = st.columns(2)

    # Gender (placed in the first column)
    with col1:
        st.header("Personal Information")
        gender = st.radio("2. What is your gender?", ["Male", "Female"])
        gender_mapping = {"Male": 0, "Female": 1}
        gender_numeric = gender_mapping[gender]

    # Age (placed in the second column)
    with col2:
        age = st.slider("1. How old are you?", 15, 18, 16)

    # Study Time and Absences (side by side)
    col3, col4 = st.columns(2)
    with col3:
        average_time = st.slider("2. How many hours per week do you study on average?", 0, 25, 12)
    with col4:
        absences = st.slider("2. How many days were you absent?", 0, 30, 5)

    # Tutoring (placed in the first column)
    with col1:
        tutoring = st.radio("3. Have you received tutoring?", ["Yes", "No"])
        tutoring_mapping = {"Yes": 1, "No": 0}
        tutoring_numeric = tutoring_mapping[tutoring]

    # GPA (placed in the second column)
    with col2:
        performance = st.slider("5. What is your current GPA:", min_value=1.0, max_value=6.0, step=0.05)

    # Extracurricular Activities (multiselect with expanded section)
    st.header("Extracurricular Activities")
    col5, col6 = st.columns(2)
    with col5:
        sports = 0
        music = 0
        volunteering = 0
        extracurricular = 0

        spec_ex_activities = st.multiselect(
            "Which activities do you participate in?",
            ["Sports", "Music", "Volunteering", "Extracurricular Activities"]
        )
        
        # Set variables to 1 if the activity is selected
        if "Sports" in spec_ex_activities:
            sports = 1
        if "Music" in spec_ex_activities:
            music = 1
        if "Volunteering" in spec_ex_activities:
            volunteering = 1
        if "Extracurricular" in spec_ex_activities:
            extracurricular = 1

    # Support (select slider)
    st.header("Parental Support")
    support = st.select_slider("7. Rate the support from your parents:", ["No support", "Low", "Moderate", "High", "Very high"])
    degree_mapping_support = {"No support": 0, "Low": 1, "Moderate": 2, "High": 3, "Very high": 4}
    support_numeric = degree_mapping_support[support]

    # Parental Degree (radio)
    st.header("Parental Education")
    parental_degree = st.radio("8. What is the highest education level your parents completed?", ["No degree", "High School", "Bachelor's", "Master's", "PhD"])
    degree_mapping_parental = {"No degree": 0, "High School": 1, "Bachelor's": 2, "Master's": 3, "PhD": 4}
    parental_degree_numeric = degree_mapping_parental[parental_degree]

# Visualization Section
st.title("Compare Your Inputs to the Average")

# Categories and Min/Max values
categories = [
    "Age", 
    "Parental Education", 
    "Study Time Weekly", 
    "Absences", 
    "Parental Support",
    "Tutoring",
    "GPA",
    "Sports",
    "Music",
    "Volunteering",
    "Extracurricular Activities"
]

# Define min and max values for each category
min_values = {
    "Age": 15, 
    "Parental Education": 0, 
    "Study Time Weekly": 0, 
    "Absences": 0, 
    "Parental Support": 0,
    "Tutoring": 0,
    "GPA": 1,
    "Sports": 0,
    "Music": 0,
    "Volunteering": 0,
    "Extracurricular Activities": 0
}

max_values = {
    "Age": 18, 
    "Parental Education": 4, 
    "Study Time Weekly": 25, 
    "Absences": 30, 
    "Parental Support": 4,
    "Tutoring": 1,
    "GPA": 6,
    "Sports": 1,
    "Music": 1,
    "Volunteering": 1,
    "Extracurricular Activities": 1
}

# Average values for comparison (you can adjust these based on your data)
average_values = [16.46864548, 1.746237458, 9.771991919, 14.54138796, 2.122073579, 0.5, 4, 0.5, 0.5, 0.5, 0.5]

# User's values based on their inputs
user_values = [age, parental_degree_numeric, average_time, absences, support_numeric, tutoring_numeric, performance, sports, music, volunteering, extracurricular]

# Normalize the user values and the average values
def normalize(value, category):
    return (value - min_values[category]) / (max_values[category] - min_values[category])

# Apply normalization
normalized_user_values = [normalize(value, category) for value, category in zip(user_values, categories)]
normalized_average_values = [normalize(value, category) for value, category in zip(average_values, categories)]

# Close the radar chart by adding the first category again
categories += [categories[0]]
normalized_user_values += [normalized_user_values[0]]
normalized_average_values += [normalized_average_values[0]]

# Create DataFrames for both user inputs and average values
df_user = pd.DataFrame({
    'Category': categories,
    'Value': normalized_user_values,
    'Type': ['Your Inputs'] * len(categories)
})

df_average = pd.DataFrame({
    'Category': categories,
    'Value': normalized_average_values,
    'Type': ['Average'] * len(categories)
})

# Combine both DataFrames
df_combined = pd.concat([df_average, df_user])

# Plot radar chart using Plotly
fig = px.line_polar(
    df_combined, 
    r='Value', 
    theta='Category', 
    color='Type', 
    line_close=True
)

# Customize radar chart appearance
fig.update_layout(
    polar=dict(
        bgcolor="white",  
        radialaxis=dict(
            visible=True,
            range=[0, 1]
        ),
        angularaxis=dict(
            visible=True
        )
    ),
)

# Set fill color for user input and average areas
fig.update_traces(
    fill='toself',
    fillcolor="rgba(180, 180, 180, 0.4)",  
    line_color="gray",  
    selector=dict(name="Average")
)

fig.update_traces(
    fill='toself',
    fillcolor="rgba(225, 130, 180, 0.4)",  
    line_color="red",  
    selector=dict(name="Your Inputs")
)

# Display chart
st.plotly_chart(fig, use_container_width=True)
