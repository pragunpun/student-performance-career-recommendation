import streamlit as st
import pandas as pd

# Load CSV with stream options
df = pd.read_csv('minor_project_cleaned.csv')
stream_options = ["Select"] + df['interested_stream'].dropna().unique().tolist()  # assuming column name


st.title("🎓 Student Performance & Career Recommendation System")

st.header("Enter Student Details")


# Input form
with st.form("student_form"):
    student_id = st.text_input("Student ID")
    gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"])
    attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0, step=0.1)

    st.subheader("Enter Subject Marks (out of 100)")
    eng_marks = st.number_input("English Marks", min_value=0, max_value=100, step=1)
    hindi_marks = st.number_input("Hindi Marks", min_value=0, max_value=100, step=1)
    math_marks = st.number_input("Math Marks", min_value=0, max_value=100, step=1)
    sci_marks = st.number_input("Science Marks", min_value=0, max_value=100, step=1)
    social_marks = st.number_input("Social Science Marks", min_value=0, max_value=100, step=1)
    computer_marks = st.number_input("Computer Marks", min_value=0, max_value=100, step=1)
    
    study_hours_per_day = st.number_input("Average Study Hours Per Day", min_value=0.0, max_value=24.0, value=0.0)
    
    prefer_to_study_in = st.selectbox("Prefer to Study in", ["Select", "Morning", "Afternoon", "Evening", "Night", "Anytime"])

    interested_stream = st.selectbox("Interested Area / Stream", stream_options)
    
    hobbies = st.text_input("Hobbies")

    extracurricular_activities = st.radio("Participates in Extracurricular Activities?", ["Yes", "No"])

    social_media_hours = st.number_input("Social Media Usage (hours/day)",min_value=0.0, max_value=24.0, value=0.0)

    stress_level = st.slider("Stress Level (out of 10)", 0, 10, 5)

    
    # Submit button
    submitted = st.form_submit_button("Submit")

if submitted:
    st.session_state["student_id"] = student_id
    st.session_state["attendance"] = attendance
    st.session_state["study_hours"] = study_hours_per_day
    st.session_state["interest_area"] = interested_stream
    st.session_state["extracurricular"] = extracurricular_activities

    st.session_state["eng_marks"] = eng_marks
    st.session_state["hindi_marks"] = hindi_marks
    st.session_state["math_marks"] = math_marks
    st.session_state["sci_marks"] = sci_marks
    st.session_state["social_marks"] = social_marks
    st.session_state["computer_marks"] = computer_marks

    st.session_state["prefer_to_study_in"] = prefer_to_study_in
    st.session_state["social_media"] = social_media_hours
    st.session_state["stress_level"] = stress_level

    st.success(f"Welcome, Student ID: {student_id}! 🎉")
    st.info("Now use the sidebar to navigate to Performance, Career, or Report pages.")
else:
    st.warning("⚠️ Please fill all fields before continuing.")
