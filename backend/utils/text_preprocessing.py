import spacy
from nltk.corpus import stopwords
import re
import nltk
# --- Ensure NLTK data downloads in cloud environments ---
nltk.download('stopwords')
nltk.download('punkt')

# ---------------- NLP MODEL SETUP ----------------
# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Load English stopwords (for text cleanup)
STOPWORDS = set(stopwords.words("english"))

# -------------------------------------------------------
# ✅ AI Resume Ranker - Text Preprocessing Utility
# Minor Project Final Version (Smart Context-Aware Version)
# -------------------------------------------------------

def apply_synonyms(text):
    """
    Smart, context-aware normalization.
    Handles flexible skill naming like:
    - PowerBI Reports, Dashboards → Power BI
    - Data Cleaning & Handling → Data Cleaning
    - ReactJS, Node JS → React, Node.js
    - Communication and Team Collaboration → Communication Skills, Teamwork
    """

    replacements = {
        # -------- DATABASES --------
        r"\b(mysql|postgresql|ms\s*sql|sql\s*(server|database)?)\b": "sql",

        # -------- WEB / FRONTEND --------
        # Preserve specific JS frameworks before generic JS replacement
        r"\b(reactjs|react\.js|react\s*app|react\s*framework)\b": "react",
        r"\b(nodejs|node\.js|node\s*app|node\s*js)\b": "node.js",
        r"\b(expressjs|express\.js|express\s*js)\b": "express.js",
        r"\b(nextjs|next\.js|next\s*js)\b": "next.js",

        # Now safely handle standalone 'js' at the end of words
        # Standalone 'JS' replacement (avoid touching Node.js / ReactJS / ExpressJS)
        #r"(?<!node)(?<!react)(?<!express)(?<!next)\b(js)\b": "javascript",



        # -------- DATA SKILLS --------
        r"\b(power[\s\-]*bi(\s*(dashboard|dashboards|report|reports|tool|tools|workspace)?)?)\b": "power bi",
        r"\b(data\s*(cleaning|handling|wrangling|preprocessing|management|munging|transformation))\b": "data cleaning",
        r"\b(data\s*(visualization|viz|dashboards|charts|plots|reporting|analysis))\b": "data visualization",
        r"\b(dashboard|dashboards)\b": "data visualization",
        r"\b(data\s*(analytics|analysis|insights|mining))\b": "data analysis",
        r"\b(eda|exploratory\s*data\s*analysis)\b": "data analysis",
        r"\b(excel\s*(sheet|tool|file|workbook|reports)?)\b": "excel",

        # -------- ML / AI --------
        r"\b(ml|machine\s*learning(\s*(model|project|algorithm)?)?)\b": "machine learning",
        r"\b(dl|deep\s*learning)\b": "deep learning",
        r"\b(ai|artificial\s*intelligence)\b": "artificial intelligence",

        # -------- SOFT SKILLS --------
        r"\b(team\s*(collaboration|coordination|player|work))\b": "teamwork",
        r"\b(collaboration|coordination|cooperation)\b": "teamwork",
        r"\b(communication(\s*skills)?|presentation|documentation|interpersonal\s*skills)\b": "communication skills",
        r"\b(problem\s*solving|analytical\s*thinking|critical\s*thinking)\b": "problem solving",
        r"\b(leadership|management\s*skills|team\s*lead)\b": "leadership",

        # -------- TOOLS / ENVIRONMENTS --------
        r"\b(vs\s*code|visual\s*studio\s*code)\b": "vs code",
        r"\b(intellij|intellij\s*idea)\b": "intellij idea",
        r"\b(jupyter\s*notebook|colab|google\s*colab)\b": "jupyter notebook",
        r"\b(vscode)\b": "vs code"
    }

    text = text.lower()

    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)

    text = re.sub(r"\s{2,}", " ", text).strip()
    return text


def clean_and_lemmatize(text):
    print("\n--- DEBUG CLEANED TEXT (from text_preprocessing) ---\n")
    print(text[:800])

    """
    Final Stable Version ✅
    Cleans text, applies synonyms, preserves multi-word technical phrases,
    and lemmatizes words without splitting letters.
    """

    # 1️⃣ Normalize synonyms first
    text = apply_synonyms(text)
    
    # --- Protect important acronyms and tech tokens before spaCy modifies them ---
    ACRONYMS = [
        "AWS", "SNS", "SQS", "IAM", "CI", "CD", "API", "JWT",
        "REST", "SQL", "HTML", "CSS", "HTTP", "TCP", "UDP"
    ]

    # Convert any of these acronyms into lowercase protected tokens
    for acr in ACRONYMS:
        pattern = r"\b" + acr + r"\b"
        text = re.sub(pattern, acr.lower(), text, flags=re.IGNORECASE)


    # 2️⃣ Protect multi-word skill phrases
    key_phrases = [
        "power bi", "data cleaning", "data visualization", "data analysis",
        "machine learning", "deep learning", "communication skills", "teamwork",
        "problem solving", "artificial intelligence", "visual studio code",
        "intellij idea", "jupyter notebook"
    ]
    for phrase in key_phrases:
        protected = phrase.replace(" ", "_")
        text = re.sub(phrase, protected, text, flags=re.IGNORECASE)
    # --- Preserve JS frameworks before cleaning ---
    text = re.sub(r"\b(node[\s\-\.]*js)\b", "node_js", text, flags=re.I)
    text = re.sub(r"\b(react[\s\-\.]*js)\b", "react_js", text, flags=re.I)
    text = re.sub(r"\b(express[\s\-\.]*js)\b", "express_js", text, flags=re.I)
    text = re.sub(r"\b(next[\s\-\.]*js)\b", "next_js", text, flags=re.I)



    # 3️⃣ Basic cleanup — keep letters, numbers, underscores, and spaces
    text = re.sub(r"[^A-Za-z0-9_\s]", " ", text)
    text = re.sub(r"\s{2,}", " ", text).strip()

    
    # 4️⃣ Lemmatize with spaCy (simple mode)
    doc = nlp(text)
    tokens = []

    # 🧠 Always preserve tech-specific tokens before lemmatization
    TECH_KEYWORDS = {
        "jest", "supertest", "axios", "vite", "tailwind", "redux",
        "swagger", "postman", "eslint", "mocha", "chai", "docker",
        "lambda", "sns", "sqs", "iam", "joi"
    }

    for token in doc:
        tok = token.text.lower()
        if "_" in tok:
            tokens.append(tok)
        elif tok in TECH_KEYWORDS:
            tokens.append(tok)  # ✅ preserve as-is
        elif tok not in STOPWORDS and token.is_alpha:
            tokens.append(token.lemma_.lower())


    # 5️⃣ Restore multi-word phrases
    clean_text = " ".join(tokens).replace("_", " ")

    # 6️⃣ Final normalization (handle residual merges)
    clean_text = re.sub(r"([a-z])([A-Z])", r"\1 \2", clean_text)
    clean_text = re.sub(r"\s{2,}", " ", clean_text).strip()
    
    clean_text = clean_text.replace("node_js", "node.js")
    clean_text = clean_text.replace("react_js", "react.js")
    clean_text = clean_text.replace("express_js", "express.js")
    clean_text = clean_text.replace("next_js", "next.js")


        # ---- Final spacing patch for glued skill endings ----
    # add space after known skill endings that merge with next word (like 'power bicreation')
    clean_text = re.sub(r"(power bi)(?=[a-z])", r"\1 ", clean_text)
    clean_text = re.sub(r"(machine learning)(?=[a-z])", r"\1 ", clean_text)
    clean_text = re.sub(r"(data visualization)(?=[a-z])", r"\1 ", clean_text)
    clean_text = re.sub(r"(sql)(?=[a-z])", r"\1 ", clean_text)
    clean_text = re.sub(r"(data cleaning)(?=[a-z])", r"\1 ", clean_text)

    # remove any double spaces
    clean_text = re.sub(r"\s{2,}", " ", clean_text).strip()
    
        # ---- Final Smart Spacing Patch ----
    # Add missing space if a key skill phrase is glued to the next word
    fix_phrases = [
        "power bi", "data cleaning", "data visualization",
        "machine learning", "sql", "data analysis"
    ]
    for phrase in fix_phrases:
        clean_text = re.sub(rf"({phrase})(?=[a-z])", r"\1 ", clean_text)

    clean_text = re.sub(r"\s{2,}", " ", clean_text).strip()
    
    # 🧠 DEBUG: Show the cleaned text preview before returning
    print("\n[DEBUG] Final Cleaned Text Snippet:\n", clean_text[:500])
    
    return clean_text


# ------------------- TEST SECTION -------------------
if __name__ == "__main__":
    sample_text = """
    Developed PowerBI Reports and dashboards using MySQL database.
    Worked on ReactJS app and NodeJS backend for data visualization.
    Strong in Data Cleaning, Wrangling and Machine Learning model deployment.
    Excellent Team Collaboration, Leadership and Documentation.
    """
    print("\n--- Original Text ---\n", sample_text)
    print("\n--- Cleaned & Normalized ---\n", clean_and_lemmatize(sample_text))
