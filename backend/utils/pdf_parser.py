import pdfplumber
import re

# -------------------------------------------------------
# ✅ AI Resume Ranker - PDF Text Extraction Utility
# Minor Project Final Version
# -------------------------------------------------------

def extract_text_from_pdf(path):
    """
    Extracts and cleans text from a PDF file using pdfplumber.
    Handles line breaks, bullet points, and unwanted characters.
    Returns a clean text string ready for NLP processing.
    """

    full_text = []

    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                full_text.append(text)
    except Exception as e:
        print(f"[ERROR] Failed to read PDF: {path}\nReason: {e}")
        return ""

    # Join all pages
    text = "\n".join(full_text)

    # ---------- CLEANUP STEPS ----------
    # Remove bullets and special symbols
    text = re.sub(r"[•■●▪◆]", " ", text)

    # Replace newlines with spaces
    text = text.replace("\n", " ")

    # Remove multiple spaces
    text = re.sub(r"\s{2,}", " ", text)

    # Remove unwanted non-ASCII or control characters
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    # Keep letters, digits, and important punctuation
    text = re.sub(r"[^A-Za-z0-9\.\,\-\+\#\s]", " ", text)

    # Normalize spacing again
    text = re.sub(r"\s{2,}", " ", text).strip()
    print("\n--- DEBUG PDF TEXT PREVIEW (LAST CLEANED VERSION) ---\n")
    print(text[:1500])

    return text


# ------------------- TEST SECTION -------------------
if __name__ == "__main__":
    sample_pdf = "sample_resumes/Anurag 04-11-2025 Infosys.pdf"
    print("\n--- Extracted PDF Text (Preview) ---\n")
    text = extract_text_from_pdf(sample_pdf)
    print(text[:2000])  # Show first 1000 chars only
