import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.model.skill_extractor import extract_skills_from_text
from backend.utils.pdf_parser import extract_text_from_pdf
from backend.utils.text_preprocessing import clean_and_lemmatize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# -------------------------
# Hybrid Resume Ranker
# (Skill-based + TF-IDF)
# -------------------------

def rank_resumes_combined(required_skills, job_description, resume_folder,
                          skill_weight=0.6, ml_weight=0.4):
    # safety: ensure weights sum to 1
    total = skill_weight + ml_weight
    if total == 0:
        skill_weight, ml_weight = 0.6, 0.4
    else:
        skill_weight = skill_weight / total
        ml_weight = ml_weight / total

    results = []
    resumes = [f for f in os.listdir(resume_folder) if f.lower().endswith(".pdf")]

    if not resumes:
        return []

    # Normalize required skills
    required_skills_norm = [s.strip().lower() for s in required_skills if s and s.strip()]

    # Tech fallback keywords to auto-detect if extractor misses them
    TECH_FALLBACK = {"jest", "supertest", "axios", "vite", "tailwind", "redux", "fastapi", "swagger", "postman"}

    for resume_file in resumes:
        resume_path = os.path.join(resume_folder, resume_file)

        # 1) Extract raw text from PDF
        raw_text = extract_text_from_pdf(resume_path) or ""
        # debug raw
        print("\n[DEBUG] RAW_TEXT preview (first 400 chars):\n", raw_text[:400])

        # 2) Clean and lemmatize
        resume_clean = clean_and_lemmatize(raw_text) or ""
        print("\n[DEBUG] CLEANED_TEXT preview (first 400 chars):\n", resume_clean[:400])

        # 3) Extract skills found using your skill extractor
        found_skills = extract_skills_from_text(resume_clean) or []
        found_lower = [s.lower() for s in found_skills]
        print("\n[DEBUG] FOUND_SKILLS from extractor:", found_skills)

        # 4) Fallback: auto-detect tech keywords directly from raw_text and cleaned text
        #    (handles cases where skill list missing or preprocessing dropped tokens)
        raw_lower = raw_text.lower()
        clean_lower = resume_clean.lower()

        fallback_added = []
        for kw in TECH_FALLBACK:
            if kw not in found_lower and (kw in raw_lower or kw in clean_lower):
                found_lower.append(kw)
                fallback_added.append(kw)

        if fallback_added:
            print("[DEBUG] Fallback auto-added keywords:", fallback_added)

        # 5) Matched / missing against required list
        matched = [s for s in required_skills_norm if s in found_lower]
        missing = [s for s in required_skills_norm if s not in found_lower]

        skill_score = round((len(matched) / len(required_skills_norm)) * 100, 2) if required_skills_norm else 0.0

        results.append({
            "file_name": resume_file,
            "resume_text": resume_clean,
            "skill_score": skill_score,
            "matched_skills": matched,
            "missing_skills": missing
        })

    # ---------------- TF-IDF (semantic) processing ----------------
    job_text = job_description.strip() if (job_description and job_description.strip()) else " ".join(required_skills_norm)
    job_clean = clean_and_lemmatize(job_text)

    docs = [job_clean] + [r["resume_text"] for r in results]

    try:
        vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
        tfidf_matrix = vectorizer.fit_transform(docs)
        job_vec = tfidf_matrix[0]
        resume_vecs = tfidf_matrix[1:]
        tfidf_scores = cosine_similarity(job_vec, resume_vecs).flatten() * 100
    except Exception as e:
        print("[DEBUG] TF-IDF error:", e)
        tfidf_scores = np.zeros(len(results))

    # Combine
    for idx, r in enumerate(results):
        ml_score = round(float(tfidf_scores[idx]), 2) if len(tfidf_scores) > idx else 0.0
        final_score = round((skill_weight * r["skill_score"] + ml_weight * ml_score), 2)
        r["tfidf_score"] = ml_score
        r["final_score"] = final_score

    results.sort(key=lambda x: x["final_score"], reverse=True)

    # Cleanup
    for r in results:
        if "resume_text" in r:
            del r["resume_text"]

    return results



# ---------------- TEST / DEMO ----------------
if __name__ == "__main__":
    # Example required skills and job description you can edit for testing
    required_skills = ["Python", "SQL", "Power BI", "Excel", "Data Analysis", "Machine Learning"]
    job_description = (
        "We are looking for a Data Analyst with strong skills in Python, SQL, Power BI and Excel. "
        "Should be familiar with data cleaning, visualization and basic machine learning."
    )
    folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../sample_resumes"))

    ranked = rank_resumes_combined(required_skills, job_description, folder)

    print("\n--- Hybrid Resume Ranking (Skill + TF-IDF) ---\n")
    for res in ranked:
        print(f"{res['file_name']} -> Final: {res['final_score']}%  |  Skill: {res['skill_score']}%  |  TF-IDF: {res['tfidf_score']}%")
        print(f"✅ Matched: {res['matched_skills']}")
        print(f"❌ Missing: {res['missing_skills']}\n")
