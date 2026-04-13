import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from io import BytesIO

st.title("📄 Report")

# ----------------------------------
# Check session state
# ----------------------------------
if "student_id" not in st.session_state:
    st.warning("⚠️ No student data found. Please fill details in Home page.")
    st.stop()

# Load data
student_id = st.session_state["student_id"]
attendance = st.session_state["attendance"]
extracurricular = st.session_state["extracurricular"]

total = st.session_state["performance_total"]
average = st.session_state["performance_average"]
percentage = st.session_state["performance_percentage"]
grade = st.session_state["performance_grade"]

strongest = st.session_state["performance_strongest"]
weakest = st.session_state["performance_weakest"]
improvement_tips = st.session_state["performance_tips"]  
study_advice = st.session_state["performance_advice"]
marks_df = st.session_state["performance_marks_df"]

interest_area = st.session_state.get("interest_area", "Not Available")
predicted_stream = st.session_state.get("predicted_stream", "Not Available")
career_info = st.session_state.get("career_data", {})

careers_list = career_info.get("Careers", [])
courses_list = career_info.get("Courses", [])
institutions_list = career_info.get("Institutions", [])



# ----------------------------------
# UI
# ----------------------------------
st.subheader(f"Student Report : {student_id}")
st.write("---")

left, right = st.columns(2)

# ---------------- LEFT SIDE ----------------
with left:
    st.subheader("📘 Overview")
    st.info(
        f"**Attendance:** {attendance}%\n\n"
        f"**Extracurricular Activities:** {extracurricular}\n\n"
        f"**Total Marks:** {total}\n\n"
        f"**Average Marks:** {average:.2f}\n\n"
        f"**Percentage:** {percentage}%\n\n"
        f"**Grade:** {grade}\n\n"
    )

    st.write("### 📌 Study Advice")
    for a in study_advice:
        st.markdown(f"- {a}")


# ---------------- RIGHT SIDE ----------------
with right:
    st.subheader("📊 Performance Details")
    st.success(f"**Strongest Subjects:** {', '.join(strongest)}")
    st.error(f"**Weakest Subjects:** {', '.join(weakest)}")

    # Histogram
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

    st.write("### 📌 Improvement Tips (Weak Subjects)")
    for subject, tips in improvement_tips.items():
        st.markdown(f"**{subject}:**")
        for t in tips:
            st.markdown(f"- {t}")

img_buffer = BytesIO()
fig.savefig(img_buffer, format="png")
img_buffer.seek(0)

# ----------------------------------
# Career Section
# ----------------------------------
st.write("---")
st.subheader("🎯 Career Recommendation")

# ---------- Stream Match / Mismatch Block ----------
if interest_area != predicted_stream:
    st.info(f"⚠️ Your interest is **{interest_area}**, but performance prediction suggests **{predicted_stream}**.")
else:
    st.info(f"✅ Perfect! Your interest matches your performance → **{predicted_stream}**" )

st.write("### 💡 Reasoning:")
st.write(career_info.get("Reason", "Not Available"))

st.write("### 🌟 Top 5 Careers (Predicted Stream)")
if careers_list:
    for i, c in enumerate(careers_list, 1):
        st.write(f"{i}. {c}")
else:
    st.write("Not Available")

st.write("### 🎓 Top Courses")
if courses_list:
    for i, course in enumerate(courses_list, 1):
        st.write(f"{i}. {course}")
else:
    st.write("Not Available")

st.write("### 🏫 Top 5 Institutions")

# Create dataframe first
inst_df = pd.DataFrame(institutions_list, columns=["Institution", "Official Website"])

# Fix index to start from 1
inst_df.index = inst_df.index + 1

# Display table
st.table(inst_df)



# ---------------------- PDF DOWNLOAD ----------------------
if st.button("📥 Download Report (PDF)"):

    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Header
    story.append(Paragraph(f"<b>Student Report – {student_id}</b>", styles["Title"]))
    story.append(Spacer(1, 12))

    # Overview
    story.append(Paragraph("<b>📘 Overview</b>", styles["Heading2"]))
    story.append(Paragraph(f"Attendance: {attendance}%", styles["Normal"]))
    story.append(Paragraph(f"Extracurricular: {extracurricular}", styles["Normal"]))
    story.append(Paragraph(f"Total Marks: {total}", styles["Normal"]))
    story.append(Paragraph(f"Average Marks: {average:.2f}", styles["Normal"]))
    story.append(Paragraph(f"Percentage: {percentage}%", styles["Normal"]))
    story.append(Paragraph(f"Grade: {grade}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # Performance
    story.append(Paragraph("<b>📊 Performance Details</b>", styles["Heading2"]))
    story.append(Paragraph(f"Strongest Subjects: {', '.join(strongest)}", styles["Normal"]))
    story.append(Paragraph(f"Weakest Subjects: {', '.join(weakest)}", styles["Normal"]))

    story.append(Paragraph("<b>Improvement Tips:</b>", styles["Heading3"]))
    for subject, tips in improvement_tips.items():
        story.append(Paragraph(f"<b>{subject}</b>", styles["Normal"]))
        for t in tips:
            story.append(Paragraph(f"- {t}", styles["Normal"]))

    story.append(Paragraph("<b>Study Advice:</b>", styles["Heading3"]))
    for a in study_advice:
        story.append(Paragraph(f"- {a}", styles["Normal"]))

    story.append(Spacer(1, 12))

    # Histogram
    story.append(Paragraph("<b>📈 Subject Performance Chart</b>", styles["Heading2"]))
    img_buffer.seek(0)
    story.append(Image(img_buffer, width=400, height=250))
    story.append(Spacer(1, 12))

    # Career Recommendation
    # Match Section in PDF
    if interest_area == predicted_stream:
        story.append(Paragraph(
            f"<b>🎯 Perfect Match:</b> Your interest and predicted stream both are <b>{predicted_stream}</b>.",
            styles["Normal"]
        ))
    else:
        story.append(Paragraph(
            f"<b>⚠️ Stream Mismatch:</b> Interest: <b>{interest_area}</b> | Predicted: <b>{predicted_stream}</b>",
            styles["Normal"]
        ))

    story.append(Spacer(1, 10))
    
    # Reasoning
    story.append(Paragraph(f"<b>Reason:</b> {career_info.get('Reason','Not Available')}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # Careers
    story.append(Paragraph("<b>🌟 Top 5 Careers</b>", styles["Heading3"]))
    if careers_list:
        for c in careers_list:
            story.append(Paragraph(f"• {c}", styles["Normal"]))
    else:
        story.append(Paragraph("Not Available", styles["Normal"]))
    story.append(Spacer(1, 10))

    # Courses
    story.append(Paragraph("<b>🎓 Best Courses</b>", styles["Heading3"]))
    if courses_list:
        for i, course in enumerate(courses_list, 1):
            story.append(Paragraph(f"{i}. {course}", styles["Normal"]))
    else:
        story.append(Paragraph("Not Available", styles["Normal"]))
    story.append(Spacer(1, 10))
    
    # Institutions
    story.append(Paragraph("<b>🏫 Top 5 Institutions</b>", styles["Heading3"]))
    inst_table = [["Institution", "Official Website"]]

    for i, inst in enumerate(institutions_list, 1):
        inst_table.append([f"{i}. {inst[0]}", inst[1]])
        
    table = Table(inst_table, colWidths=[200, 200])
    table.setStyle(TableStyle([ 
        ("BACKGROUND", (0,0), (-1,0), colors.lightblue),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
    ]))
    story.append(table)


    # Build PDF
    doc.build(story)

    st.download_button(
        label="Download PDF",
        data=pdf_buffer.getvalue(),
        file_name=f"student_report_{student_id}.pdf",
        mime="application/pdf"
    )
