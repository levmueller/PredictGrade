import streamlit as st


sidebar = st.sidebar.selectbox(
    "Choose a page:",
    ["Home", "Questionnaire", "GitHub API"]
)




# Title
st.title("My First Streamlit App 2.0")

# Text
st.write("Welcome to my first Streamlit app! Feel free to interact with the elements below.")

# Input form
name = st.text_input("Enter your name:")
age = st.number_input("Enter your age:", min_value=1, max_value=100, value=18)

# Button interaction
if st.button("Submit"):
    if name:
        st.success(f"Hello, {name}! You are {age} years old.")
    else:
        st.warning("Please enter your name!")

# Sidebar
st.sidebar.title("About")
st.sidebar.write("This is a basic Streamlit app example.")
