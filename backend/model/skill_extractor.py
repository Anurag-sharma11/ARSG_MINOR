import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import re
from pathlib import Path
from backend.utils.text_preprocessing import apply_synonyms, clean_and_lemmatize

# -------------------------------------------------------
# 🚀 AI Resume Ranker - Universal Skill Extractor (Production-Ready)
# -------------------------------------------------------

# Path to the skills list file
SKILLS_FILE = Path(__file__).parent / "skills_list.txt"

# Toggle debug printing
DEBUG_MODE = False


def load_skills():
    """
    Load all skill keywords from skills_list.txt.
    If missing, use a robust fallback list.
    """
    if SKILLS_FILE.exists():
        skills = [s.strip().lower() for s in SKILLS_FILE.read_text().splitlines() if s.strip()]
    else:
        # Fallback default skill set
        skills = [
            "python", "java", "c", "c++", "html", "css", "javascript", "typescript",
            "react", "node.js", "express.js", "django", "flask", "sql", "mysql",
            "mongodb", "power bi", "excel", "data analysis", "data visualization",
            "data cleaning", "machine learning", "deep learning", "nlp", "git",
            "linux", "postman", "api", "rest api", "jwt", "jest", "supertest",
            "axios", "tailwind", "redux", "vite", "fastapi", "docker", "lambda",
            "sns", "sqs", "iam", "aws", "ci cd", "terraform", "jira"
        ]
    return skills


def extract_skills_from_text(text):
    """
    Extracts skills from text using:
    - NLP cleaning
    - Synonym normalization
    - Acronym and tech keyword handling
    - Regex and fallback scanning
    """

    # Step 1️⃣: Clean + normalize
    cleaned_text = clean_and_lemmatize(text)
    normalized_text = apply_synonyms(cleaned_text)
    text_lower = normalized_text.lower()

    # Step 2️⃣: Load known skills
    skills = load_skills()
    found = set()

    # Step 3️⃣: Pre-compile regex for speed
    all_text_no_punct = re.sub(r'[^a-z0-9]', '', text_lower)

    # Step 4️⃣: Smart acronym handling — merge IAM, CI/CD, JWT, REST, etc.
    # Replace possible variants to match consistently
    text_lower = re.sub(r"\bi am\b", "iam", text_lower)
    text_lower = re.sub(r"ci[\s\-\/]?cd", "ci cd", text_lower)
    text_lower = re.sub(r"aws[\s\-]*(sns|sqs|lambda)", r"aws \1", text_lower)
    text_lower = re.sub(r"jwt[\s\-]*(auth|token)?", "jwt", text_lower)

    # Optional debug print
    if DEBUG_MODE:
        print("\n--- DEBUG CLEANED TEXT PREVIEW ---\n", text_lower[:800])

    # Step 5️⃣: Pattern matching
    for skill in skills:
        skill = skill.strip().lower()
        tokens = skill.split()

        if len(tokens) > 1:
            # For multi-word skills like "machine learning", "power bi"
            pattern = r"(?i)\b" + r"[\s\-/]*".join(map(re.escape, tokens)) + r"s?\b"
        else:
            pattern = r"(?i)\b" + re.escape(skill) + r"s?\b"

        if re.search(pattern, text_lower):
            found.add(skill)
        else:
            # Compact version for things like 'restapi', 'cicd'
            compact_skill = re.sub(r'[^a-z0-9]', '', skill)
            if compact_skill in all_text_no_punct:
                found.add(skill)

    # Step 6️⃣: Fallback detection for modern tools missed by skills list
    TECH_FALLBACK = [
    "axios", "jest", "supertest", "vite", "tailwind", "redux",
    "swagger", "fastapi", "postman", "iam", "sns", "sqs",
    "jwt", "ci cd", "docker", "kubernetes", "terraform",
    "joi", "joi validation"
    ]


    for kw in TECH_FALLBACK:
        if (kw in text_lower or kw.replace(" ", "") in all_text_no_punct):
            found.add(kw)

    # Step 7️⃣: Return sorted list
    found_sorted = sorted(found)

    if DEBUG_MODE:
        print("\n[DEBUG] Extracted Skills:", found_sorted)

    return found_sorted


# ------------------- TEST SECTION -------------------
if __name__ == "__main__":
    sample_text = """
    Built secure APIs using JWT Auth, IAM (least privilege), and AWS Lambda with SNS/SQS.
    Developed React.js app using Axios, Jest, and Supertest for backend validation.
    Configured CI/CD pipelines using GitHub Actions and Docker containers.
    """
    print("\n--- Extracted Skills ---\n")
    print(extract_skills_from_text(sample_text))
