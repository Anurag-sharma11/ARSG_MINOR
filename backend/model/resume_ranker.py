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
    """
    Rank resumes using a hybrid approach:
      - Skill-based score: fraction of required skills found in resume
      - TF-IDF cosine similarity: semantic similarity between job description and resume text
    Final score = skill_weight * skill_score + ml_weight * tfidf_score
    :param required_skills: list of required skill strings (e.g. ["python","sql"])
    :param job_description: string describing job (used for TF-IDF)
    :param resume_folder: path containing PDF resumes
    :param skill_weight: float between 0 and 1
    :param ml_weight: float between 0 and 1 (skill_weight + ml_weight should ideally = 1)
    :return: list of dicts sorted by final_score descending
    """

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

    # ---------------- Skill-based processing ----------------
    required_skills_norm = [s.strip().lower() for s in required_skills if s and s.strip()]

    for resume_file in resumes:
        resume_path = os.path.join(resume_folder, resume_file)
        # Extract and preprocess resume text
        raw_text = extract_text_from_pdf(resume_path)
        resume_clean = clean_and_lemmatize(raw_text)

        # Extract skills found in resume text
        found_skills = extract_skills_from_text(resume_clean)

        # compute matched / missing lists
        found_lower = [s.lower() for s in found_skills]
        matched = [s for s in required_skills_norm if s in found_lower]
        missing = [s for s in required_skills_norm if s not in found_lower]

        # skill score as percentage 0-100
        skill_score = round((len(matched) / len(required_skills_norm)) * 100, 2) if required_skills_norm else 0.0

        results.append({
            "file_name": resume_file,
            "resume_text": resume_clean,
            "skill_score": skill_score,
            "matched_skills": matched,
            "missing_skills": missing
        })

    # ---------------- TF-IDF (semantic) processing ----------------
    # If job_description is empty, use required_skills joined as the job text
    job_text = job_description.strip() if (job_description and job_description.strip()) else " ".join(required_skills_norm)
    job_clean = clean_and_lemmatize(job_text)

    docs = [job_clean] + [r["resume_text"] for r in results]

    # Vectorize (lightweight)
    try:
        vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
        tfidf_matrix = vectorizer.fit_transform(docs)
        job_vec = tfidf_matrix[0]
        resume_vecs = tfidf_matrix[1:]
        tfidf_scores = cosine_similarity(job_vec, resume_vecs).flatten() * 100  # scale 0-100
    except Exception:
        # if TF-IDF fails for any reason, give zero ML contribution
        tfidf_scores = np.zeros(len(results))

    # ---------------- Combine into final score ----------------
    for idx, r in enumerate(results):
        ml_score = round(float(tfidf_scores[idx]), 2) if len(tfidf_scores) > idx else 0.0
        final_score = round((skill_weight * r["skill_score"] + ml_weight * ml_score), 2)
        r["tfidf_score"] = ml_score
        r["final_score"] = final_score

    # Sort by final_score descending
    results.sort(key=lambda x: x["final_score"], reverse=True)

    # Cleanup: remove resume_text to avoid large payloads
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
