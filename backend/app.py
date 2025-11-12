import streamlit as st
import json
import os
import shutil
import pandas as pd
import plotly.express as px

from model.resume_ranker import rank_resumes_combined
from model.skill_extractor import extract_skills_from_text
from utils.pdf_parser import extract_text_from_pdf
from utils.text_preprocessing import clean_and_lemmatize

# -------------------------------------------------------
# 🧠 AI Resume Ranker + Skill Preview
# Minor Project Final Version (Enhanced)
# -------------------------------------------------------

# ---------- PAGE SETTINGS ----------
st.set_page_config(
    page_title="AI Resume Ranker",
    page_icon="🧠",
    layout="wide",
)

# ---------- HEADER ----------
st.title("🧠 AI Resume Analyzer & Ranker (Hybrid Model)")
st.markdown(
    """
    Welcome to the **AI Resume Ranker** built with NLP and Machine Learning.  
    This app offers two modes:
    - 🎯 **Skill Preview:** Quickly test resume skill extraction accuracy.  
    - 📊 **Resume Ranker:** Rank candidates using a Hybrid Model (Skills + TF-IDF).  
    """
)

# ---------- TAB LAYOUT ----------
tab1, tab2 = st.tabs(["🎯 Skill Preview", "📊 Resume Ranker"])

# -------------------------------------------------------
# TAB 1️⃣: SKILL PREVIEW
# -------------------------------------------------------
with tab1:
    st.subheader("🎯 Skill Extraction Preview")
    st.write("Upload resumes to view the automatically extracted skills before running ranking analysis.")

    uploaded_files_preview = st.file_uploader(
        "Upload Resume PDFs for Skill Preview",
        type=["pdf"],
        accept_multiple_files=True,
        key="skill_preview"
    )

    if uploaded_files_preview:
        temp_folder = "temp_skill_preview"
        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder)
        os.makedirs(temp_folder, exist_ok=True)

        for file in uploaded_files_preview:
            file_path = os.path.join(temp_folder, file.name)
            with open(file_path, "wb") as f:
                f.write(file.read())

            # Extract text
            raw_text = extract_text_from_pdf(file_path)
            clean_text = clean_and_lemmatize(raw_text)
            extracted_skills = extract_skills_from_text(raw_text)

            # ---------- DISPLAY ----------
            st.markdown(f"### 📄 {file.name}")
            st.write("**Detected Skills:**")

            if extracted_skills:
                cols = st.columns(5)
                for i, skill in enumerate(extracted_skills):
                    cols[i % 5].markdown(
                        f"<div style='padding:6px;background-color:#e0f2ff;"
                        f"border-radius:8px;text-align:center;margin:3px;"
                        f"font-size:14px;color:#004c99;'>💡 {skill}</div>",
                        unsafe_allow_html=True
                    )
            else:
                st.warning("⚠️ No skills detected in this resume.")

            with st.expander("🔍 View Cleaned Resume Text"):
                st.text(clean_text[:1500] + ("..." if len(clean_text) > 1500 else ""))

            st.markdown("---")

        st.success("✅ Skill extraction completed successfully!")

        # Cleanup
        shutil.rmtree(temp_folder)
    else:
        st.info("Please upload one or more resumes to preview their extracted skills.")

# -------------------------------------------------------
# TAB 2️⃣: RESUME RANKER
# -------------------------------------------------------
with tab2:
    st.subheader("📊 AI Resume Ranker with Skill Gap Analysis")
    st.write("Rank candidates using **Skill Matching + TF-IDF Similarity** for accurate results.")

    # ---------- JOB PROFILE SELECTION ----------
    job_profile_path = os.path.join("backend", "model", "job_profiles.json")
    if os.path.exists(job_profile_path):
        with open(job_profile_path) as f:
            job_profiles = json.load(f)
    else:
        job_profiles = {}

    job_options = list(job_profiles.keys())
    selected_job = st.selectbox("🧩 Select Job Profile", job_options, index=None, placeholder="Choose a job profile...")

    # Auto-fill both skills and job description when a profile is selected
    prefilled_skills_text = ""
    prefilled_description = ""

    if selected_job:
        prefilled_skills_text = ", ".join(job_profiles[selected_job]["skills"])
        prefilled_description = job_profiles[selected_job]["job_description"]


    # ---------- INPUTS ----------
    with st.expander("🎯 Enter Job Requirements", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            required_skills_input = st.text_area(
                "Enter Required Skills (comma-separated):",
                prefilled_skills_text or "Python, SQL, Excel, Data Visualization, Machine Learning",
                height=100
            )
        with col2:
            job_description_input = st.text_area(
                "Paste Job Description (optional):",
                prefilled_description or "We are looking for candidates with strong technical and analytical skills.",
                height=100
            )


    uploaded_files_rank = st.file_uploader(
        "Upload Resume PDFs for Ranking",
        type=["pdf"],
        accept_multiple_files=True,
        key="rank_upload"
    )

    # ---------- ANALYZE ----------
    if st.button("🚀 Analyze & Rank"):
        if not uploaded_files_rank:
            st.warning("⚠️ Please upload at least one resume.")
        elif not required_skills_input.strip():
            st.warning("⚠️ Please enter required skills before analyzing.")
        else:
            required_skills = [s.strip() for s in required_skills_input.split(",") if s.strip()]
            temp_folder = "temp_resumes"

            # Reset temp folder
            if os.path.exists(temp_folder):
                shutil.rmtree(temp_folder)
            os.makedirs(temp_folder, exist_ok=True)

            for file in uploaded_files_rank:
                file_path = os.path.join(temp_folder, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.read())

            # ---------- RUN HYBRID RANKER ----------
            results = rank_resumes_combined(required_skills, job_description_input, temp_folder)

            if results:
                st.subheader("📊 Resume Ranking Results")

                for res in results:
                    st.markdown(f"### 📄 {res['file_name']}")
                    st.progress(res["final_score"] / 100)
                    st.write(f"**Final Score:** {res['final_score']}%  "
                             f"(Skill: {res['skill_score']}%, TF-IDF: {res['tfidf_score']}%)")
                    st.write(f"✅ **Matched Skills:** {', '.join(res['matched_skills']) or 'None'}")
                    st.write(f"❌ **Missing Skills:** {', '.join(res['missing_skills']) or 'None'}")
                    st.markdown("---")

                # ---------- BAR CHART ----------
                df = pd.DataFrame(results)
                st.subheader("📈 Match Percentage Comparison")
                fig = px.bar(
                    df,
                    x="file_name",
                    y="final_score",
                    color="final_score",
                    color_continuous_scale="Blues",
                    text="final_score",
                    labels={"file_name": "Resume File", "final_score": "Match %"},
                )
                fig.update_traces(texttemplate='%{text}%', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)

                # ---------- CSV DOWNLOAD ----------
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name="resume_ranking_results.csv",
                    mime="text/csv",
                )

                st.success("✅ Analysis Completed Successfully!")

            else:
                st.warning("⚠️ No resumes found or unable to extract text.")

            shutil.rmtree(temp_folder)
