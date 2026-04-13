import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib

# Load CSV and model 
df = pd.read_csv('minor_project_cleaned.csv')
model = joblib.load("student_performance_model.pkl")

st.title("📘 Student Performance")

# Check if data exists from Home.py
if "student_id" in st.session_state:

    # Fetch student inputs from Home.py
    student_id = st.session_state["student_id"]
    attendance = float(st.session_state["attendance"])
    extracurricular = st.session_state["extracurricular"]
    study_hours = float(st.session_state["study_hours"])
    interest_area = st.session_state["interest_area"]
    social_media = int(float(st.session_state.get("social_media", 0)))
    stress_level = int(float(st.session_state.get("stress_level", 0)))
    extracurricular = extracurricular.strip().lower()
    prefer_to_study_in = st.session_state.get("prefer_to_study_in", "anytime")
    prefer_to_study_in = prefer_to_study_in.strip().lower()

   
    # Subject marks
    subjects = ["English", "Hindi", "Math", "Science", "Social Science", "Computer"]
    marks = [
        st.session_state["eng_marks"],
        st.session_state["hindi_marks"],
        st.session_state["math_marks"],
        st.session_state["sci_marks"],
        st.session_state["social_marks"],
        st.session_state["computer_marks"]
    ]
    # DataFrame for visualization
    marks_df = pd.DataFrame({"Subject": subjects, "Marks": marks})

    # Performance calculations
    total = sum(marks)
    avg_marks = total / len(marks)
    percent = round((total / (len(marks) * 100)) * 100, 2)

    # Grade
    if percent >= 90:
        grade = "A+"
    elif percent >= 80:
        grade = "A"
    elif percent >= 70:
        grade = "B"
    elif percent >= 60:
        grade = "C"
    elif percent >= 50:
        grade = "D"
    else:
        grade = "F"


    # Student Info Section
    st.markdown("### 🧾 Student Details")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Student ID:** {student_id}")
    with col2:
        st.write(f"**Total Attendance:** {attendance}%")

    
    # Overall Performance Summary 
    col1, col2 = st.columns(2)
    with col1:
        st.info(
            f"**Total Marks:** {total} / {len(subjects)*100}\n\n"
            f"**Percentage:** {percent:.2f}%\n\n"
        )
    with col2:
        st.info(
            f"**Average Marks:** {avg_marks:.2f}\n\n"
            f"**Grade:** {grade}\n\n"
        )
    
    # Subject-wise performance Chart
    st.subheader("📈 Subject-wise Performance")
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(marks_df["Subject"], marks_df["Marks"], color='skyblue', edgecolor='black')
    ax.set_ylim(0, 100)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)  # light dotted grid lines
    
    ax.set_xlabel("Subjects", fontsize=11, fontweight='bold')
    ax.set_ylabel("Marks", fontsize=11, fontweight='bold')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 1,
                f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    st.pyplot(fig)


    # Strongest & Weakest Subjects 
    max_mark = max(marks)
    min_mark = min(marks)
    strongest_subjects = [subjects[i] for i, m in enumerate(marks) if m == max_mark]
    weakest_subjects = [subjects[i] for i, m in enumerate(marks) if m == min_mark]

    st.success(f"**Strongest Subjects:** {', '.join(strongest_subjects)}")
    st.error(f"**Weakest Subjects:** {', '.join(weakest_subjects)}")


    # Weak subject tips
    tips = {
        "Math": [
            "Solve at least 10–15 practice problems daily.",
            "Learn shortcuts and tricks for calculations to save time.",
            "Watch tutorial videos for difficult topics.",
            "Solve previous years’ questions to understand exam patterns."
        ],
        "Science": [
            "Make short notes for each topic to summarize important concepts.",
            "Use diagrams and flowcharts to understand processes.",
            "Do experiments or practical learning.",
            "Solve previous years’ questions to understand exam patterns."
        ],
        "English": [
            "Read short stories, articles, or news daily to improve vocabulary and comprehension.",
            "Write short essays or paragraphs to improve writing skills.",
            "Practice grammar exercises and sentence correction.",
            "Listen to English podcasts or videos to improve listening and speaking.",
            "Solve previous years’ questions to understand exam patterns."
        ],
        "Hindi": [
            "Listen to English podcasts or videos to improve listening and speaking.",
            "Practice writing essays, letters, and grammar exercises.",
            "Revise important poems and chapters frequently.",
            "Solve previous years’ questions to understand exam patterns."
        ],
        "Social Science": [
            "Create mind maps for history & civics of important dates and events.",
            "Watch documentaries for better memory.",
            "Revise daily with short notes.",
            "Solve previous years’ questions to understand exam patterns."
        ],
        "Computer": [
            "Practice coding or exercises daily for programming subjects.",
            "Build small projects.",
            "Follow online courses and watch tutorials for difficult topics like algorithms or data structures.",
            "Solve previous years’ questions to understand exam patterns."
        ]
    }

   # Show weakest subject tips
    weak_tips_final = {}
    for sub in weakest_subjects:
        if sub in tips:
            st.subheader(f"📘 Improvement Tips for {sub}")
            for t in tips[sub]:
                st.write(f"- {t}")
                weak_tips_final[sub] = tips[sub]   # save for report
        else:
            st.write(f"No tips available for {sub}")


    
    # Study Advice & Suggestions
    st.markdown("### 🧠 Study Advice & Suggestions")
    advice = []

     # Attendance advice
    if attendance < 75:
        advice.append("Your attendance is below 75%. Attend classes more regularly for better understanding.")

    # Study hours advice
    if study_hours < 2:
        advice.append("Increase study hours to at least 2–3 hours/day for better performance.")
    elif study_hours >= 6:
        advice.append("Avoid overstudying. Take breaks and rest to maintain focus.")
    else:
        advice.append("Study hours seems well-balanced!")

    # Extracurricular activity advice
    if extracurricular == "no":
        advice.append("Try joining extracurriculars to reduce stress and improve focus.") 
    else:
        advice.append("Keep balancing studies with activities you enjoy. Extracurriculars help in overall development.")
    
    # Social media advice
    if social_media > 4:
        advice.append("Too much screen time affects focus. Try to cut down social media use gradually (reduce by 30 mins/day).")

    # Stress level advice
    if stress_level >= 7:
        advice.append("You seem stressed. Practice relaxation, exercise, or hobbies to refresh your mind.")
    elif stress_level >= 4:
        advice.append("Normal stress level — quite normal for students. Manage your schedule with short study breaks.")
    else:
        advice.append("Low stress — great balance! Keep following your study routine.")
        
    # Study timing advice
    if prefer_to_study_in == "anytime":
        advice.append("Try choosing a fixed study time daily. A fixed routine improves focus and productivity.")
   
    # Output advice
    for a in advice:
        st.markdown(f"- {a}")


    
    # Overall recommendations
    st.markdown("## 💡Overall Recommendation")
    if avg_marks < 50:
        st.warning(" You need to improve overall performance. Try to review weak subjects daily.")
    elif avg_marks <= 75:
        st.info(" You’re doing well, but focus on improving consistency and revising weak topics.")
    else:
        st.success("✅ Excellent performance! Keep maintaining your study habits and balance extracurriculars.")

    # SAVE EVERYTHING IN SESSION STATE   
    st.session_state["performance_total"] = total
    st.session_state["performance_average"] = avg_marks
    st.session_state["performance_percentage"] = percent
    st.session_state["performance_grade"] = grade

    st.session_state["performance_strongest"] = strongest_subjects
    st.session_state["performance_weakest"] = weakest_subjects
    st.session_state["performance_tips"] = weak_tips_final
    st.session_state["performance_advice"] = advice
    st.session_state["performance_marks_df"] = marks_df
    st.session_state["prefer_to_study_in"] = prefer_to_study_in
    

else:
    st.warning("No student data found. Please fill the form in Home page first.")