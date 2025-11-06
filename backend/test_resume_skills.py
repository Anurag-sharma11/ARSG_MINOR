import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.utils.pdf_parser import extract_text_from_pdf
from backend.utils.text_preprocessing import clean_and_lemmatize
from backend.model.skill_extractor import extract_skills_from_text

# -------------------------------------------------------
# 🧠 Quick Resume Skill Tester
# Run:  python backend/test_resume_skills.py <path_to_resume.pdf>
# Example: python backend/test_resume_skills.py "sample_resumes/Anurag.pdf"
# -------------------------------------------------------

def test_resume(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"\n❌ File not found: {pdf_path}\n")
        return

    print(f"\n📄 Testing Resume: {os.path.basename(pdf_path)}\n")

    # Step 1️⃣ Extract text from PDF
    text = extract_text_from_pdf(pdf_path)

    print("\n--- Extracted Raw Text (first 600 chars) ---\n")
    print(text[:600], "\n")

    # Step 2️⃣ Clean + normalize text
    clean_text = clean_and_lemmatize(text)

    print("\n--- Cleaned & Normalized Text (first 600 chars) ---\n")
    print(clean_text[:600], "\n")

    # Step 3️⃣ Extract skills
    skills = extract_skills_from_text(text)

    print("\n--- Extracted Skills ---\n")
    print(skills, "\n")

    print("✅ Test completed successfully!\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n⚠️ Usage: python backend/test_resume_skills.py <path_to_resume.pdf>\n")
    else:
        pdf_path = sys.argv[1]
        test_resume(pdf_path)
