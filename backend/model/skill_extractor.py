import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import re
from pathlib import Path
from backend.utils.text_preprocessing import apply_synonyms, clean_and_lemmatize

# -------------------------------------------------------
# ✅ AI Resume Ranker - Skill Extractor Module
# Final Debugged Version (Full Integration)
# -------------------------------------------------------

# Path to the skills list file
SKILLS_FILE = Path(__file__).parent / "skills_list.txt"

def load_skills():
    """
    Load all skill keywords from skills_list.txt.
    If the file is missing, load a fallback list of common skills.
    """
    if SKILLS_FILE.exists():
        skills = [s.strip().lower() for s in SKILLS_FILE.read_text().splitlines() if s.strip()]
    else:
        # Fallback list
        skills = [
            "python", "java", "c", "c++", "html", "css", "javascript",
            "react", "node.js", "django", "flask", "sql", "mysql", "mongodb",
            "power bi", "excel", "data analysis", "data visualization", "data cleaning",
            "machine learning", "deep learning", "nlp", "git", "linux",
            "communication skills", "teamwork", "problem solving",
            "pandas", "numpy", "postman", "api", "rest api", "leadership"
        ]
    return skills


def extract_skills_from_text(text):
    """
    Extracts known skills from text:
    - Applies advanced synonym normalization
    - Cleans, lemmatizes, and regex-matches skills
    - Handles variations like PowerBI, Data Handling, ReactJS, etc.
    """

    # Step 1️⃣: Clean and lemmatize first
    text = clean_and_lemmatize(text)

    # Step 2️⃣: Apply synonym normalization AFTER cleaning
    text = apply_synonyms(text)

    # Step 3️⃣: Fix potential glued phrases (powerbi → power bi, etc.)
    for p in ["power bi", "machine learning", "data visualization", "sql", "data cleaning"]:
        text = re.sub(rf"({p})(?=[a-z])", r"\1 ", text)


    # Step 4️⃣: Load known skills
    skills = load_skills()
    found = set()

    
    # Step 5️⃣: Flexible pattern matching
    print("\n--- DEBUG TEXT PREVIEW ---\n")
    print(text[:800])  # 👈 optional: shows what text extractor sees, remove later if not needed

    for skill in skills:
        # create flexible pattern: allows spaces, newlines, or hyphens between words
        tokens = skill.strip().split()
        if len(tokens) > 1:
            # multi-word skill (like 'power bi', 'machine learning')
            pattern = r"(?i)\b" + r"[\s\-]*".join(map(re.escape, tokens)) + r"s?\b"
        else:
            # single word skill
            pattern = r"(?i)\b" + re.escape(skill) + r"s?\b"

        if re.search(pattern, text):
            found.add(skill)
        else:
            # Flexible matching for glued or punctuated variations
            compact_skill = re.sub(r'[^a-z0-9]', '', skill.lower())
            text_no_punct = re.sub(r'[^a-z0-9]', '', text.lower())
            if compact_skill in text_no_punct:
                found.add(skill)


    # Step 6️⃣: Return sorted unique skill list
    return sorted(found)


# ------------------- TEST SECTION -------------------
if __name__ == "__main__":
    sample_text = """
    Experienced in PowerBI dashboard creation, Data Cleaning & Data Handling.
    Developed ReactJS app with NodeJS backend.
    Strong background in Machine Learning, Data Visualization, and SQL database management.
    Excellent teamwork, leadership, and communication.
    """
    print("\n--- Extracted Skills ---\n")
    print(extract_skills_from_text(sample_text))
