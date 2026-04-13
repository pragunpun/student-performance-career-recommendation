import streamlit as st
import pandas as pd
import joblib

# --------------------------------
# Load Model + Data
# --------------------------------
df = pd.read_csv("minor_project_new_cleaned.csv")
model = joblib.load("career_recommendation_model.pkl")
scaler = joblib.load("career_scaler.pkl")
features = joblib.load("career_features.pkl")

st.title("🎯 Career Recommendation")

# Map detailed streams to grouped streams
stream_group_map = {
    "Science": ["Science", "Engineering", "Medical", "Pharmacy", "Agriculture"],
    "Commerce": ["Commerce", "Management", "Hotel-management"],
    "Arts": ["Arts", "Law"]
}

# --------------------------------
# MAIN CHECK
# --------------------------------
if "student_id" in st.session_state:
    student_id = st.session_state["student_id"]
    attendance = float(st.session_state["attendance"])
    extracurricular = st.session_state["extracurricular"]
    interest_area = st.session_state["interest_area"]
    study_hours = float(st.session_state["study_hours"])

    eng = st.session_state["eng_marks"]
    hindi = st.session_state["hindi_marks"]
    math = st.session_state["math_marks"]
    sci = st.session_state["sci_marks"]
    social = st.session_state["social_marks"]
    comp = st.session_state["computer_marks"]

    # -----------------------------
    # Create input DF
    # -----------------------------
    df_input = pd.DataFrame([{
        "attendance_percentage": attendance,
        "eng_marks": eng,
        "hindi_marks": hindi,
        "math_marks": math,
        "sci_marks": sci,
        "social_marks": social,
        "computer_marks": comp,
        "study_hours_per_day": study_hours
    }])

    # Derived features
    df_input["total_marks"] = df_input.sum(axis=1)
    df_input["avg_marks"] = df_input["total_marks"] / 6
    df_input["sci_avg"] = df_input[["math_marks", "sci_marks", "computer_marks"]].mean(axis=1)
    df_input["arts_avg"] = df_input[["eng_marks", "hindi_marks", "social_marks"]].mean(axis=1)
    df_input["commerce_avg"] = df_input[["math_marks", "social_marks", "eng_marks"]].mean(axis=1)
    df_input["study_efficiency"] = df_input["avg_marks"] / max(study_hours, 1)

    # Match model input
    X = pd.DataFrame(columns=features)
    for c in df_input.columns:
        if c in X.columns:
            X[c] = df_input[c]
    X = X.fillna(0)

    # Scale & Predict
    X_scaled = scaler.transform(X)
    predicted_stream = model.predict(X_scaled)[0]


    # --------------------------------
    # CAREER + INSTITUTIONS DATABASE
    # --------------------------------

    career_data = {

        "Science": {
            "Careers": ["Data Science & Artificial Intelligence / Machine Learning", "Engineering", "Biotechnology", "Medical", "Environmental Science"],
            "Courses":["B.Sc (Biology, Physics, Chemistry, Math)", "MBBS (Medicine)", "B.Tech (Engineering)", "B.Sc Biotechnology", "B.Sc Forensic Science"],
            "Reason": "Strong knowledge in Mathematics, Science, Computer Science.",
            "Institutions": [
                ("IIT Delhi", "https://home.iitd.ac.in"),
                ("IIT Bombay", "https://www.iitb.ac.in"),
                ("AIIMS Delhi", "https://www.aiims.edu"),
                ("Indian Institute of Science (IISc), Bengaluru", "https://www.iisc.ac.in"),
                ("Delhi University", "https://www.du.ac.in")
            ]
        },

        "Engineering": {
            "Careers": ["Software Engineer / Software Developer", "Mechanical Engineer", "Civil Engineer", "Electrical / Electronics Engineer", "Aerospace Engineer"],
            "Courses":["B.Tech / B.E Computer Science (CSE)", "B.Tech Mechanical Engineering", "B.Tech Civil Engineering", "B.Tech Electrical / Electronics & Communication (ECE)", "B.Tech Aerospace Engineering"],
            "Reason": "Strong knowledge in Mathematics, Science, Computer Science.",
            "Institutions": [
                ("IIT Madras", "https://www.iitm.ac.in"),
                ("IIT Delhi", "https://home.iitd.ac.in"),
                ("NIT Trichy", "https://www.nitt.edu"),
                ("Indian Institute of Science (IISc), Bengaluru", "https://www.iisc.ac.in"),
                ("BITS Pilani", "https://www.bits-pilani.ac.in")
            ]
        },

        "Arts": {
            "Careers": ["Journalist / Media & Communication", "Psychologist / Counselor", "Teacher", "Civil Services (IAS / IPS / IFS / UPSC)", "Lawyer / Advocate / Legal Consultant"],
            "Courses":["BA in Psychology", "BA in Political Science / Sociology", "BA LLB (Law)", "BA Journalism & Mass Communication (BJMC)", "Bachelor of Fine Arts (BFA) / Fashion Designing"],
            "Reason": "Strong knowledge in English, Social Science, Computer Science.",
            "Institutions": [
                ("Delhi University", "https://www.du.ac.in"),
                ("Jamia Millia Islamia", "https://www.jmi.ac.in"),
                ("JNU Delhi", "https://www.jnu.ac.in"),
                ("National Institute of Fashion Technology (NIFT)", "https://nift.ac.in"),
                ("Ashoka University", "https://www.ashoka.edu.in")
            ]
        },

        "Commerce": {
            "Careers": ["Chartered Accountant (CA)", "Company Secretary (CS)", "Investment Banker / Financial Analyst", "Accountant / Tax Consultant", "Marketing & Business Manager"],
            "Courses":["B.Com (Bachelor of Commerce)", "BBA (Bachelor of Business Administration)", "CA (Chartered Accountancy)", "BBM / BMS (Management Studies)"],
            "Reason": "Strong knowledge in Mathematics, English, Computer Science.",
            "Institutions": [
                ("Shri Ram College of Commerce (SRCC), DU", "https://www.srcc.edu"),
                ("St. Xavier’s College, Mumbai", "https://xaviers.edu"),
                ("Christ University, Bengaluru", "https://christuniversity.in"),
                ("Hansraj College, DU", "https://www.hansrajcollege.ac.in"),
                ("Loyola College, Chennai", "https://www.loyolacollege.edu")
            ]
        },

        "Medical": {
            "Careers": ["Doctor", "Nursing", "Dentist", "Pharmacist", "Physiotherapist"],
            "Courses":["MBBS (Bachelor of Medicine, Bachelor of Surgery)", "BDS (Bachelor of Dental Surgery)", "B.Sc Nursing", "B.Pharm (Bachelor of Pharmacy)", "BPT (Bachelor of Physiotherapy)"],
            "Institutions": [
                ("AIIMS Delhi", "https://www.aiims.edu"),
                ("Christian Medical College (CMC) Vellore", "https://www.cmch-vellore.edu"),
                ("JIPMER, Puducherry", "https://jipmer.edu.in"),
                ("Armed Forces Medical College (AFMC), Pune", "https://afmc.nic.in"),
                ("Maulana Azad Medical College (MAMC), Delhi", "https://www.mamc.ac.in")
            ],
            "Reason": "Strong knowledge in Science, Mathematics, English."
        },

        "Law": {
            "Careers": ["Corporate Lawyer", "Criminal Lawyer", "Legal Advisor", "Judge", "Civil Lawyer"],
            "Courses":["BA LLB (Integrated 5-year course)", "BBA LLB (Business + Law)", "LLB (3-year after graduation)", "LLM (Master of Law)", "B.Com LLB (Commerce + Law)"],
            "Institutions": [
                ("National Law School of India University (NLSIU), Bangalore", "https://www.nls.ac.in"),
                ("National Law University (NLU), Delhi", "https://nludelhi.ac.in"),
                ("NALSAR University of Law, Hyderabad", "https://www.nalsar.ac.in"),
                ("Symbiosis Law School (SLS), Pune", "https://www.symlaw.ac.in"),
                ("National Law University (NLU), Jodhpur", "https://nlujodhpur.ac.in")
            ],
           "Reason": "Strong knowledge in English, Social Science."
        },

        "Hotel-management": {
            "Careers": ["Chef", "Hotel Manager", "Event Manager", "Travel Coordinator", "Hospitality Executive"],
            "Courses":["Bachelor of Hotel Management (BHM)", "Diploma in Hotel Management", "B.Sc in Hospitality & Hotel Administration (HHA)", "Master of Hotel Management (MHM)", "MBA in Hospitality / Hospitality Management"],
            "Institutions": [
                ("IHM Delhi", "https://www.ihmddelhi.com"),
                ("IHM Mumbai", "https://www.ihm.edu"),
                ("IHM Bangalore", "https://www.ihmbangalore.com"),
                ("Amity University", "https://www.amity.edu"),
                ("Lovely Professional University", "https://lpu.in")
            ],
            "Reason": "Strong knowledge in English, Mathematics."
        },

        "Management": {
            "Careers": ["Business Manager", "Marketing Manager", "Human Resources (HR) Manager", "Operations Manager", "Product Manager"],
            "Courses":["MBA(Master of Business Administration)", "BBA (Bachelor of Business Administration)", "PGDM (Post Graduate Diploma in Management)", "Executive MBA / PGDM for Working Professionals", "MBA in Business Analytics / MBA in International Business / Specialized MBA"],
            "Institutions": [
                ("IIM Ahmedabad", "https://www.iima.ac.in"),
                ("IIM Bangalore", "https://www.iimb.ac.in"),
                ("IIM Calcutta", "https://www.iimcal.ac.in"),
                ("FMS Delhi", "https://fms.edu"),
                ("XLRI Jamshedpur", "https://xlri.ac.in")
            ],
            "Reason": "Strong knowledge in Mathematics, English, Computer Science."
        },

        "Pharmacy": {
            "Careers": ["Pharmacist", "Drug Researcher", "Chemical Analyst", "Quality Control Officer", "Biomedical Scientist"],
            "Courses":["D.Pharm (Diploma in Pharmacy – 2 years)", "B.Pharm (Bachelor of Pharmacy – 4 years)", "M.Pharm (Master of Pharmacy – 2 years)", "Pharm.D (Doctor of Pharmacy – 6 years)", "B.Pharm (Hons) / B.Pharm + MBA"],
            "Institutions": [
                ("National Institute of Pharmaceutical Education and Research (NIPER), Mohali", "https://www.niper.gov.in"),
                ("BITS Pilani Pharmacy", "https://www.bits-pilani.ac.in"),
                ("ICT Mumbai", "https://www.ictmumbai.edu.in"),
                ("JSS College of Pharmacy(Ooty / Mysore)", "https://www.jssuni.edu.in"),
                ("Manipal College of Pharmaceutical Sciences (MCOPS), Manipal", "https://manipal.edu")
            ],
           "Reason": "Strong knowledge in Science, Mathematics, English."
        },

        "Agriculture": {
            "Careers": ["Agricultural Officer", "Food Technologist / Quality Control Officer", "Agricultural Engineer", "Agronomist / Crop Scientist", "Agri Business Manager"],
            "Courses":["B.Sc Agriculture (4 Years)", "B.Tech Agricultural Engineering (4 Years)", "B.Sc Horticulture", "B.Sc Forestry", "M.Sc Agriculture / MBA Agri-Business"],
            "Institutions": [
                ("ICAR – Indian Agricultural Research Institute (IARI), New Delhi", "https://www.iari.res.in"),
                ("Punjab Agricultural University (PAU), Ludhiana", "https://www.pau.edu"),
                ("GB Pant University of Agriculture & Technology, Uttarakhand", "https://www.gbpuat.ac.in"),
                ("Tamil Nadu Agricultural University (TNAU), Coimbatore", "https://tnau.ac.in"),
                ("Junagadh Agricultural University", "https://www.jau.in")
            ],
            "Reason": "Strong knowledge in Science, Mathematics, English, Computer Science."
        }
    }


    
    # --------------------------------
    # SHOW PREDICTION SUMMARY
    # --------------------------------
    st.subheader("📘 Prediction Summary")
    st.markdown(f"⚡ Your Interested Stream: **{interest_area}**  |  🎯 Predicted Stream Based On Performance: **{predicted_stream}**", unsafe_allow_html=True)

    # =====================================================================
    # CASE 1 : INTEREST MATCHES
    # =====================================================================
    if interest_area == predicted_stream:
        st.success(f"Perfect! Your interest matches your performance → **{predicted_stream}**")
        data = career_data[predicted_stream]
        
        # SAVE DATA (THIS WAS MISSING)
        st.session_state["interest_area"] = interest_area
        st.session_state["predicted_stream"] = predicted_stream
        st.session_state["career_data"] = data
        
         # Top 5 Careers
        st.write("### 🌟 Top 5 Career Recommendations:")
        for idx, career in enumerate(data["Careers"], 1):
            st.write(f"{idx}. {career}")

        # Top 5 Courses
        st.write("### 🎓 Top Courses for This Stream:")
        for idx, course in enumerate(data["Courses"], 1):
            st.write(f"{idx}. {course}")

        # Top 5 Institutions in table
        st.write("### Top 5 Institutions:")
        html = "<table style='border-collapse: collapse; width: 100%;'>"
        html += "<tr style='border-bottom: 1px solid #ddd;'><th>No.</th><th>Institution</th><th>Website</th></tr>"
        for idx, (inst, link) in enumerate(data["Institutions"], 1):
            html += f"<tr style='border-bottom: 1px solid #ddd;'><td>{idx}</td><td>{inst}</td><td><a href='{link}' target='_blank'>Link</a></td></tr>"
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)


    # =====================================================================
    # CASE 2 : INTEREST DOES NOT MATCH
    # =====================================================================
    else:
        st.warning(f"⚠️ Your interest is **{interest_area}**, but prediction suggests **{predicted_stream}**.")

        pred_data = career_data[predicted_stream]

        # Careers based on predicted stream
        st.write("### 📈 You Might Excel In:")
        st.markdown(f"**Reason:** {pred_data['Reason']}")
        for idx, career in enumerate(pred_data["Careers"], 1):
            st.write(f"{idx}. {career}")

        # Courses based on predicted stream
        st.write("### 🎓 Top Courses for This Stream:")
        for idx, course in enumerate(pred_data["Courses"], 1):
            st.write(f"{idx}. {course}")
        
        # Institutions table
        st.write("### Top 5 Institutions:")
        html = "<table style='border-collapse: collapse; width: 100%;'>"
        html += "<tr style='border-bottom: 1px solid #ddd;'><th>No.</th><th>Institution</th><th>Website</th></tr>"
        for idx, (inst, link) in enumerate(pred_data["Institutions"], 1):
            html += f"<tr style='border-bottom: 1px solid #ddd;'><td>{idx}</td><td>{inst}</td><td><a href='{link}' target='_blank'>Link</a></td></tr>"
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)

        # Interest stream suggestions
        st.info("💡 If You Want to Pursue Your Interest Stream")
        interest_data = career_data.get(interest_area)
        if interest_data:
            st.write(f"### ⭐ Your Interest Stream: **{interest_area}**")
            
            st.write("### Top 5 Career Options in Your Interest Area:")
            for idx, career in enumerate(interest_data["Careers"], 1):
                st.write(f"{idx}. {career}")
                
            # Top Courses
            st.write("### 🎓 Top Courses for Your Interest Stream:")
            for idx, course in enumerate(interest_data["Courses"], 1):
                st.write(f"{idx}. {course}")

            #top Institutions
            st.write("### Top 5 Institutions:")
            html_interest = "<table style='border-collapse: collapse; width: 100%;'>"
            html_interest += "<tr style='border-bottom: 1px solid #ddd;'><th>No.</th><th>Institution</th><th>Website</th></tr>"
            for idx, (inst, link) in enumerate(interest_data["Institutions"], 1):
                html_interest += f"<tr style='border-bottom: 1px solid #ddd;'><td>{idx}</td><td>{inst}</td><td><a href='{link}' target='_blank'>Link</a></td></tr>"
            html_interest += "</table>"
            st.markdown(html_interest, unsafe_allow_html=True)

        
        st.subheader("🧭 Improvement Tips")
        st.write("- Improve marks in subjects related to your interest stream.")
        st.write("- Increase study hours gradually.")
        st.write("- Reduce stress and avoid distractions.")
        st.write("- Explore projects or internships related to your chosen field.")
        
        # SAVE EVERYTHING IN SESSION STATE
        st.session_state["interest_area"] = interest_area
        st.session_state["predicted_stream"] = predicted_stream
        st.session_state["career_data"] = career_data.get(predicted_stream, {})



# --------------------------------
# FINAL ELSE: Missing student data
# --------------------------------
else:
    st.warning("⚠️ Please fill student details on Home page first.")
