st.title("Questionnaire")
st.write("Please answer the following questions to calculate your expected grade.")

st.markdown("---")

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
    ["Sports", "Music", "Volunteering", "Other Extracurricular Activities (Theatre, Arts, etc.)"]
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
