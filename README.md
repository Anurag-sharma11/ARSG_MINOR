Perfect bro 💪 — here’s your **final single, complete, and professional `README.md`** for your **Minor Project: AI Resume Ranker with Skill Gap Analysis**.

This README includes everything — project intro, architecture, modules, tech stack, testing tools, Streamlit UI, viva-ready explanations, and future scope.
You can directly use it for **college submission, GitHub upload, or viva presentation**.

---

# 🧠 AI Resume Ranker with Skill Gap Analysis

### 🎓 Minor Project – BCA (Data Science / Computer Applications)

---

## 📘 **Project Overview**

The **AI Resume Ranker with Skill Gap Analysis** is an intelligent web-based system designed to automate the process of resume evaluation and candidate ranking.
It leverages **Natural Language Processing (NLP)**, **Machine Learning (TF-IDF)**, and **Streamlit** for a smart and interactive recruiter experience.

This system not only ranks resumes based on skill and context but also identifies **missing skills (Skill Gaps)**, helping recruiters and candidates alike.

---

## 🧩 **Objectives**

* ✅ Automate resume screening and ranking.
* ✅ Extract both technical and soft skills from PDF resumes.
* ✅ Use NLP and ML for semantic similarity analysis.
* ✅ Highlight **skill gaps** for each candidate.
* ✅ Provide an interactive recruiter dashboard (Streamlit).

---

## 🚀 **Key Features**

### 🎯 1. Skill Extraction (NLP)

* Extracts **technical** (Python, SQL, Power BI) and **soft skills** (Teamwork, Communication Skills).
* Uses a **context-aware text preprocessing pipeline** built with **spaCy** + **regex**.
* Handles variations like:

  * `PowerBI`, `Power-BI` → `Power BI`
  * `MachineLearning` → `Machine Learning`
  * `Team Collaboration` → `Teamwork`

---

### 📊 2. Resume Ranking (Hybrid Model)

* Combines **Skill-Based Matching** and **TF-IDF Semantic Similarity**.

**Formula:**

```
Final Score = 0.6 * Skill Match + 0.4 * TF-IDF Similarity
```

**Outputs:**

* 🧠 Skill Match %
* 🧮 TF-IDF Similarity %
* 🏆 Final Weighted Score %
* ✅ Matched Skills
* ❌ Missing Skills

---

### 🧠 3. Skill Gap Analysis

For every resume:

* ✅ Lists skills **present** in the resume.
* ❌ Highlights skills **missing** compared to the job profile.
* Helps recruiters find improvement areas.

---

### 💻 4. Streamlit Web Interface

Built with **Streamlit**, providing an interactive dashboard with **two main tabs**:

#### 🧩 Tab 1 – **Skill Preview**

* Upload multiple PDF resumes.
* Extracted skills displayed as **colored tags (LinkedIn-style)**.
* Expandable clean-text preview.

#### 📈 Tab 2 – **Resume Ranker**

* Enter required job skills and job description.
* Upload multiple resumes → Rank candidates using **Hybrid Model**.
* Visual results with:

  * Progress bars per resume
  * Bar chart comparison (Plotly)
  * CSV download for recruiter use

---

### ⚙️ 5. Backend Components

| File                                  | Description                                                     |
| ------------------------------------- | --------------------------------------------------------------- |
| `backend/utils/pdf_parser.py`         | Extracts text from PDF resumes using **pdfplumber**             |
| `backend/utils/text_preprocessing.py` | Cleans text, applies lemmatization, preserves multi-word skills |
| `backend/model/skill_extractor.py`    | Detects skills using regex + synonym normalization              |
| `backend/model/resume_ranker.py`      | Ranks resumes using Skill Matching + TF-IDF Similarity          |
| `backend/model/skills_list.txt`       | Knowledge base of 200+ technical & soft skills                  |
| `backend/test_resume_skills.py`       | CLI script for fast resume skill testing                        |
| `backend/app.py`                      | Streamlit dashboard with Skill Preview & Ranker tabs            |

---

## 🧩 **System Architecture**

```
                ┌──────────────────────┐
                │   Recruiter Uploads  │
                │   Resumes (PDF)      │
                └──────────┬───────────┘
                           │
                           ▼
             ┌────────────────────────────┐
             │   PDF Parser (pdfplumber)  │
             └──────────┬─────────────────┘
                           │
                           ▼
          ┌────────────────────────────────────┐
          │   NLP Preprocessing (spaCy, Regex) │
          │  → Clean text, apply synonyms      │
          │  → Preserve skills (Power BI, ML)  │
          └──────────┬─────────────────────────┘
                           │
                           ▼
         ┌────────────────────────────────────┐
         │  Skill Extractor                   │
         │  → Match from skills_list.txt       │
         │  → Identify missing skills          │
         └──────────┬─────────────────────────┘
                           │
                           ▼
        ┌────────────────────────────────────┐
        │  Hybrid Ranker                     │
        │  → Skill Match (60%)               │
        │  → TF-IDF Semantic (40%)           │
        └──────────┬─────────────────────────┘
                           │
                           ▼
        ┌────────────────────────────────────┐
        │  Streamlit Dashboard               │
        │  → Skill Preview                   │
        │  → Resume Ranking + Visualization  │
        │  → CSV Download                    │
        └────────────────────────────────────┘
```

---

## 🧠 **Tech Stack**

| Category             | Tools / Libraries                        |
| -------------------- | ---------------------------------------- |
| **Language**         | Python 3.11                              |
| **Framework**        | Streamlit                                |
| **NLP Libraries**    | spaCy, NLTK, Regex                       |
| **Machine Learning** | scikit-learn (TF-IDF, Cosine Similarity) |
| **Data Handling**    | pandas                                   |
| **PDF Parsing**      | pdfplumber                               |
| **Visualization**    | Plotly                                   |
| **Frontend (UI)**    | Streamlit Components + HTML/CSS Styling  |

---

## 🧪 **Testing Tools**

### 🧩 CLI Resume Skill Tester

Run directly in terminal to test any PDF:

```bash
python backend/test_resume_skills.py "sample_resumes/Anurag 04-11-2025 Infosys.pdf"
```

Output Example:

```
--- Extracted Skills ---
['python', 'sql', 'power bi', 'data cleaning', 'data visualization',
 'machine learning', 'communication skills', 'teamwork', 'leadership']
```

---

### 🎯 Streamlit Web App

Run the interactive app:

```bash
streamlit run backend/app.py
```

Open in browser → [http://localhost:8501](http://localhost:8501)

---

## 📊 **Sample Output (Ranking Results)**

| Resume               | Skill Match % | TF-IDF % | Final Score | Rank |
| -------------------- | ------------- | -------- | ----------- | ---- |
| `krishan_cv.pdf`     | 80%           | 30%      | **70%**     | 🥇 1 |
| `Anurag_Infosys.pdf` | 70%           | 25%      | **60%**     | 🥈 2 |
| `Old_Resume.pdf`     | 45%           | 15%      | **40%**     | 🥉 3 |

**Bar Chart Visualization:**

* Generated automatically using **Plotly** inside Streamlit.
* Provides visual match comparison between resumes.

---

## 💡 **Real-World Applications**

* 🏢 Used by **Recruiters** to automate candidate shortlisting.
* 🧑‍🎓 Used by **Students** to identify missing skills for a desired job role.
* 🧠 Extensible to **AI-driven skill recommendation** systems.

---

## 🧾 **Future Enhancements**

| Feature                     | Description                                          |
| --------------------------- | ---------------------------------------------------- |
| 🤖 AI Skill Recommendations | Suggest missing skills with Coursera / YouTube links |
| 🗣️ Chatbot Integration     | Recruiter assistant for filtering candidates         |
| ☁️ Cloud Deployment         | Deploy via Streamlit Cloud / Render                  |
| 📈 Experience Weighting     | Factor in years of experience                        |
| 🔐 Login & Dashboard        | Separate recruiter profiles with history tracking    |

---

🧑‍💼 Author

Anurag Sharma
📧 Email: astasamp798@gmail.com

🌐 GitHub: Anurag-sharma11

🎓 BCA (Data Science) – GGSIPU
📜 AI/ML Certificate – IIT Guwahati

## 📜 **How to Run the Project**

### Step 1️⃣ – Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2️⃣ – Run Streamlit App

```bash
streamlit run backend/app.py
```

### Step 3️⃣ – Test Skill Extraction (CLI)

```bash
python backend/test_resume_skills.py "path/to/resume.pdf"
```

---

## 🧠 **Key Learnings**

* Applied **Natural Language Processing** for text cleaning & skill extraction.
* Implemented **TF-IDF vectorization** for semantic resume similarity.
* Integrated backend ML logic with **Streamlit** for a clean UI.
* Designed system capable of both **Skill Gap Analysis** and **Resume Ranking**.

---

## 📚 **Acknowledgment**

Developed under the guidance of **faculty mentors** as part of
**Minor Project – BCA (GGSIPU, Semester V)**.

Special thanks to everyone who supported this project.

---

## 🧠 **Keywords**

`NLP`, `TF-IDF`, `Resume Screening`, `Streamlit`, `Machine Learning`,
`Power BI`, `Data Cleaning`, `Python`, `Data Analyst`, `Skill Gap Analysis`

---

## 🗓️ **Project Updates / Changelog**

### 🧠 *AI Resume Ranker with Skill Gap Analysis (Minor Project)*

---

### 🗓️ **12 November 2025 — Major Update**

#### 🔹 *Feature Added: Job Profile-Based Auto Skill & Description Fill*

**Description:**

* Added a **Job Profile dropdown** for recruiters in the Streamlit UI.
* When a recruiter selects a profile (e.g., *Data Analyst*, *Web Developer*, *System Associate*),
  → the **Required Skills** and **Job Description** fields automatically update.
* Recruiter can still **edit both fields manually** before running the analysis.
* This feature improves usability and helps recruiters quickly analyze resumes for different roles.

**Files Updated:**

* `backend/app.py` → added logic for auto-skill and description population.
* `backend/model/job_profiles.json` → restructured to store both `skills` and `job_description` for each profile.

**Example Profiles:**

* Data Analyst → Python, Excel, SQL, Power BI
* Backend Developer → Flask, Node.js, MongoDB
* UI/UX Designer → Figma, Wireframing, Prototyping

---

### 🗓️ **08 November 2025 — Functional Integration**

#### 🔹 *Hybrid Resume Ranker Model*

* Integrated combined **TF-IDF similarity + Skill Matching** algorithm for better accuracy.
* Added visualization with **Plotly Bar Chart** showing resume match percentage.
* Implemented CSV export option for ranked results.

**Files Updated:**

* `backend/model/resume_ranker.py`
* `backend/app.py`
* Added bar chart visualization + CSV download in Streamlit UI.

---

### 🗓️ **05 November 2025 — Core Feature Implementation**

#### 🔹 *Initial Functional Prototype*

* Built working version of **Resume Upload & Skill Extraction** pipeline.
* Used `pdfplumber` for PDF parsing and `nltk` + regex for text cleaning.
* Implemented **Skill Preview Tab** for recruiters to test extraction accuracy.

**Files Created:**

* `backend/utils/pdf_parser.py`
* `backend/model/skill_extractor.py`
* `backend/app.py` (initial Streamlit interface)

---

### 🗓️ **02 November 2025 — Project Setup**

#### 🔹 *Initial Setup & Environment Configuration*

* Created base folder structure for ML + Streamlit integration.
* Added dependencies in `requirements.txt`.
* Verified basic PDF reading and text preprocessing flow.

---

## 🧩 **Next Planned Features**

* 🔹 Recruiter-side option to **add custom job profiles** directly via UI (auto-save to JSON).
* 🔹 Candidate-side feature for **resume feedback generation** (Phase 2 - Major Project).
* 🔹 Advanced **semantic matching model (BERT)** upgrade for contextual similarity.

---

## 💡 **Version Info**

**Current Version:** `v1.2.0`
**Last Updated:** *12 November 2025*
**Developed By:** Anurag Sharma (BCA Minor Project)


