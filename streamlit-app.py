import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from joblib import load
import plotly.express as px

# Sidebar for navigation
sidebar = st.sidebar.selectbox(
    "Choose a page:",
    ["Home", "Questionnaire"]
)
st.set_page_config(layout="wide")
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

    age = st.slider("2. How old are you?", 15, 18, 15)

    # Academic Information
    st.subheader("Academic Information")
    average_time = st.slider("3. How many hours per week do you study on average?", 0, 25, 0)
    absences = st.slider("4. How many days were you absent?", 0, 30, 0)

    tutoring = st.radio("5. Have you received tutoring?", ["No", "Yes"])
    tutoring_mapping = {"No": 0, "Yes": 1}
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


    # Visualization Section
    st.title("Analysis of Results")
    st.write("Below is a comparison of your inputs against the overall average.")

    # Categories and Min/Max values
    categories = [
        "Age", 
        "Parental Education", 
        "Weekly Study Time", 
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
        "Weekly Study Time": 0, 
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
        "Weekly Study Time": 25, 
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
    average_values = [16.46864548, 1.746237458, 9.771991919, 14.54138796, 2.122074, 0.301421, 4, 0.303512, 0.196906, 0.157191, 0.383361]

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

    if st.session_state.responses:
            try:
                # Retrieve responses from session state
                age, gender_numeric, parental_degree_numeric, average_time, absences, tutoring_numeric, support_numeric, extracurricular, sports, music, volunteering, performance = st.session_state.responses
                

                def swiss_to_us_gpa(swiss_grade):
                    return 2 + ((swiss_grade - 1) / 5) * 2

                # Example usage:
                swiss_grade = performance  # Example Swiss grade
                us_gpa = swiss_to_us_gpa(swiss_grade)

                scaler = load('scaler.pkl')  # Make sure to load the correct scaler (used during training)

                # Correct the new_data to have 12 features in each row
                new_data = np.array([
                    [age, gender_numeric, parental_degree_numeric, average_time, absences, tutoring_numeric, support_numeric, extracurricular, sports, music, volunteering, us_gpa]
                    # Add more rows for prediction if needed
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

                # Step 6: Mapping grades to new values: 0 -> 6, 1 -> 5, 2 -> 4, 3 -> 3, 4 -> 2
                grade_mapping = {0: 6, 1: 5, 2: 4, 3: 3, 4: 2}

                # Step 7: Custom color palette: white -> gray -> red
                color_palette = ['#a3f0a3', '#c9f7c9', '#f4e1a1', '#f8b4b4', '#ff7373']  # From light green to pastel red

                # Step 8: Output the predictions and probabilities and create pie charts
                for i, (prediction, prob) in enumerate(zip(predictions, probabilities)):
                    
                    # Map the grade labels in the pie chart (only for labeling)
                    mapped_labels = [f'Grade: {grade_mapping[j]}' for j in range(len(prob))]

                    # Plot the probabilities in a pie chart with borders
                    fig, ax = plt.subplots(figsize=(2, 2))  # Create a smaller figure and axis for matplotlib
                    wedges, texts, autotexts = ax.pie(
                        prob, labels=mapped_labels, autopct='%1.1f%%', startangle=140, colors=color_palette,
                        wedgeprops={'edgecolor': 'gray', 'linewidth': 0.5}  # Adding gray border around each wedge
                    )

                    for text in texts + autotexts:
                        text.set_fontsize(4)  # Adjust font size for the labels and percentage text

                    # Add a border to the entire pie chart (outside border)
                    ax.add_patch(plt.Circle((0, 0), 1, edgecolor='lightgray', facecolor='none', lw=0.5))  # Border around pie chart

                    # Map the predicted grade using grade_mapping for the title
                    mapped_grade = grade_mapping[prediction]

                    # Extract the probability of the predicted class
                    predicted_prob = prob[np.argmax(prob)]  # Correct index for the highest probability class

                    # Display prediction text
                    st.write(f"Based on your input, there is a {predicted_prob:.1%} probability that your grade will be a {mapped_grade}.")

                    # Display the pie chart in Streamlit
                    st.pyplot(fig)  # Display the smaller pie chart in Streamlit


            except Exception as e:
                st.error(f"Error loading model or making predictions: {e}")


