professional — no “bro” tone, no hype lines, no ChatGPT-style phrases.
Content, structure, and depth will remain perfect for BCA minor project, viva, and GitHub.

Below is the final refined README.md ⬇️
You can directly copy–paste it.

🧠 AI Resume Ranker with Skill Gap Analysis
🎓 Minor Project – BCA (Data Science / Computer Applications)
📘 Project Overview

The AI Resume Ranker with Skill Gap Analysis is a web-based intelligent system designed to automate resume screening and candidate evaluation.
The project uses Natural Language Processing (NLP) and Machine Learning techniques to analyze resumes, rank candidates based on job requirements, and identify missing skills.

The system assists recruiters in shortlisting candidates efficiently and helps students understand skill gaps for specific job roles.

🎯 Objectives

Automate resume screening and ranking.

Extract technical and soft skills from PDF resumes.

Apply NLP-based semantic similarity analysis.

Identify missing skills compared to job requirements.

Provide an interactive and user-friendly dashboard.

🚀 Key Features
1️⃣ Skill Extraction using NLP

Extracts technical skills (Python, SQL, Power BI) and soft skills (Communication, Teamwork).

Uses spaCy, regex, and text normalization.

Handles multiple variations of the same skill:

PowerBI, Power-BI → Power BI

MachineLearning → Machine Learning

Team Collaboration → Teamwork

2️⃣ Resume Ranking using Hybrid Model

The system ranks resumes using a combination of:

Skill Match Percentage

TF-IDF Semantic Similarity

Final Score Formula:

Final Score = 0.6 × Skill Match + 0.4 × TF-IDF Similarity


Generated Outputs:

Skill Match Percentage

TF-IDF Similarity Score

Final Weighted Score

Matched Skills

Missing Skills

3️⃣ Skill Gap Analysis

Compares extracted resume skills with required job skills.

Identifies missing skills for each candidate.

Helps recruiters and candidates understand improvement areas.

4️⃣ Streamlit Web Interface

The application is developed using Streamlit and provides two main sections:

🔹 Skill Preview Tab

Upload multiple PDF resumes.

Displays extracted skills as visual tags.

Shows cleaned resume text for verification.

🔹 Resume Ranker Tab

Input job description and required skills.

Upload resumes for ranking.

Displays results using progress bars and bar charts.

Allows CSV export of ranking results.

5️⃣ Backend Modules
File	Description
backend/utils/pdf_parser.py	Extracts text from PDF resumes using pdfplumber
backend/utils/text_preprocessing.py	Cleans and preprocesses resume text
backend/model/skill_extractor.py	Extracts skills using regex and normalization
backend/model/resume_ranker.py	Implements hybrid ranking logic
backend/model/skills_list.txt	Repository of technical and soft skills
backend/test_resume_skills.py	Command-line skill extraction tester
backend/app.py	Streamlit-based user interface
🧩 System Architecture
Recruiter Uploads Resumes (PDF)
            ↓
PDF Text Extraction (pdfplumber)
            ↓
Text Preprocessing (spaCy, Regex)
            ↓
Skill Extraction & Normalization
            ↓
Skill Gap Identification
            ↓
Hybrid Resume Ranking (Skill Match + TF-IDF)
            ↓
Streamlit Dashboard & Visualization

🧠 Technology Stack
Category	Tools
Programming Language	Python 3.11
Framework	Streamlit
NLP	spaCy, NLTK, Regex
Machine Learning	scikit-learn (TF-IDF, Cosine Similarity)
Data Processing	pandas
PDF Processing	pdfplumber
Visualization	Plotly
🧪 Testing & Execution
🔹 Resume Skill Testing (CLI)
python backend/test_resume_skills.py "path/to/resume.pdf"


Sample Output:

['python', 'sql', 'power bi', 'machine learning',
 'data visualization', 'communication skills']

🔹 Streamlit Application
streamlit run backend/app.py


Access the application at:
http://localhost:8501

📊 Sample Ranking Output
Resume	Skill Match	TF-IDF	Final Score	Rank
krishan_cv.pdf	80%	30%	70%	1
Anurag_Infosys.pdf	70%	25%	60%	2
Old_Resume.pdf	45%	15%	40%	3
🌍 Applications

Automated resume shortlisting for recruiters.

Skill gap identification for students and job seekers.

Can be extended for large-scale recruitment systems.

🔮 Future Enhancements

AI-based skill recommendation system.

Chatbot-assisted resume screening.

Cloud deployment.

Experience-based weighting.

Recruiter login and history tracking.

🧑‍💼 Author

Anurag Sharma
BCA (Data Science) – GGSIPU
Email: astasamp798@gmail.com

GitHub: Anurag-sharma11

📌 How to Run the Project
Step 1: Install Dependencies
pip install -r requirements.txt

Step 2: Run Application
streamlit run backend/app.py

Step 3: Test Skill Extraction
python backend/test_resume_skills.py "resume.pdf"

📚 Key Learnings

Practical application of NLP for text analysis.

Use of TF-IDF for semantic similarity.

Integration of machine learning logic with web interfaces.

End-to-end system design for real-world applications.

📖 Acknowledgment

This project was developed as part of the Minor Project requirement for BCA (Semester V) under the guidance of faculty members at GGSIPU.

🔑 Keywords

NLP, Resume Screening, TF-IDF, Streamlit, Machine Learning, Skill Gap Analysis, Data Science

📌 Version Information

Version: v1.2.0

Last Updated: November 2025

Project Type: BCA Minor Project