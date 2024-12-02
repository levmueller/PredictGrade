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

    # Gender
    gender = st.radio("2. What is your gender?", ["Male", "Female"])
    gender_mapping = {
        "Male": 0,
        "Female": 1,
    }
    # Convert the selected degree to its numerical representation
    gender_numeric = gender_mapping[gender]


    age = st.slider("1. How old are you?", 15, 18, 16)

    average_time = st.slider("2. How many hours per week do you study on average?", 0, 25, 12)

    absences = st.slider("2. How many days were you absent?", 0, 30, 5)


    # Tutoring
    tutoring = st.radio("3. Have you received tutoring?", ["Yes", "No"])
    tutoring_mapping = {
        "Yes": 1,
        "No": 0,
    }
    # Convert the selected degree to its numerical representation
    tutoring_numeric = tutoring_mapping[tutoring]


    performance = st.slider("5. What is your current GPA:", min_value=1.0, max_value=6.0, step=0.05)



    ex_activities = st.radio("6. Do you participate in extracurricular activities?", ["Yes", "No"])
 
    # Zusätzliche Auswahl bei extracurricular activities
    if ex_activities == "Yes":
        spec_ex_activities = st.multiselect("Which activities?", ["Sports", "Music", "Volunteering", "Other"])
        if "Other" in spec_ex_activities:
            other_activity = st.text_input("Specify other activities:")
 



    # Support 
    support = st.select_slider("7. Rate the support from your parents:", ["No support", "Low", "Moderate", "High", "Very high"])

    degree_mapping_support = {
        "No support": 0,
        "Low": 1,
        "Moderate": 2,
        "High": 3,
        "Very high": 4
    }

    # Convert the selected degree to its numerical representation
    support_numeric = degree_mapping_support[support]

    # Parental degree
    parental_degree = st.radio("8. What is the highest education level your parents completed?", ["No degree", "High School", "Bachelor's", "Master's", "PhD"])

    degree_mapping_parental = {
        "No degree": 0,
        "High School": 1,
        "Bachelor's": 2,
        "Master's": 3,
        "PhD": 4
    }

    # Convert the selected degree to its numerical representation
    parental_degree_numeric = degree_mapping_parental[parental_degree]








import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# Define average values (as in your provided example)
categories = [
    "Age", 
    "Parental Education", 
    "Study Time Weekly", 
    "Absences", 
    "Parental Support",
    "Tutoring",
]

# Define min and max values for each category (these should ideally come from the data or domain knowledge)
min_values = {
    "Age": 15, 
    "Parental Education": 0, 
    "Study Time Weekly": 0, 
    "Absences": 0, 
    "Parental Support": 0,
    "Tutoring": 0
}

max_values = {
    "Age": 18, 
    "Parental Education": 4, 
    "Study Time Weekly": 25, 
    "Absences": 30, 
    "Parental Support": 4,
    "Tutoring": 1
}

# Change averages
average_values = [16.46864548, 1.746237458, 9.771991919, 14.54138796, 2.122073579, 0.5]

# Streamlit inputs for user data
st.title("Netzdiagram: Compare Your Inputs to the Average")

# Create a list of the user's values
user_values = [age, parental_degree_numeric, average_time, absences, support_numeric, tutoring_numeric]

# Normalize the user values and the average values
def normalize(value, category):
    return (value - min_values[category]) / (max_values[category] - min_values[category])

# Apply normalization for both user values and average values
normalized_user_values = [normalize(value, category) for value, category in zip(user_values, categories)]
normalized_average_values = [normalize(value, category) for value, category in zip(average_values, categories)]

# Duplicate the first value to close the radar chart
categories += [categories[0]]
normalized_user_values += [normalized_user_values[0]]
normalized_average_values += [normalized_average_values[0]]

# Create a DataFrame for both user inputs and average values
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
df_combined = pd.concat([df_average, df_user])  # Notice the order: average is first

# Plot radar chart using Plotly
fig = px.line_polar(
    df_combined, 
    r='Value', 
    theta='Category', 
    color='Type', 
    line_close=True
)

# Customize the radar chart appearance
fig.update_layout(
    polar=dict(
        bgcolor="white",  # Background of the radar chart itself
        radialaxis=dict(
            visible=True,
            range=[0, 1]  # Set the range of the radial axis to 0-1
        ),
        angularaxis=dict(
            visible=True
        )
    ),
)

# Set the fill color for the user input and average areas
fig.update_traces(
    fill='toself',  # Fill the area inside the radar chart
    fillcolor="rgba(180, 180, 180, 0.4)",  # Average fill color (light gray)
    line_color="gray",  # Average outline color
    selector=dict(name="Average")
)

fig.update_traces(
    fill='toself',  # Fill the average area with a transparent color
    fillcolor="rgba(225, 130, 180, 0.4)",  # User input fill color (light pink)
    line_color="red",  # User input outline color
    selector=dict(name="Your Inputs")
)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)
