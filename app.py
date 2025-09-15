import re
import string
from collections import Counter

import docx
import PyPDF2
import nltk
import streamlit as st
from nltk.corpus import stopwords

# Download stopwords (first time only)
nltk.download("stopwords", quiet=True)
STOPWORDS = set(stopwords.words("english"))


# ---------------------------
# Utils: Extract Text
# ---------------------------
def extract_text_from_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])


def extract_resume_text(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    else:
        return ""


# ---------------------------
# Text Cleaning
# ---------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"\d+", "", text)  # remove numbers
    text = text.translate(str.maketrans("", "", string.punctuation))  # remove punctuation
    tokens = text.split()
    tokens = [w for w in tokens if w not in STOPWORDS and len(w) > 2]
    return tokens


# ---------------------------
# ATS Scoring
# ---------------------------
def calculate_score(resume_tokens, jd_tokens):
    resume_counts = Counter(resume_tokens)
    jd_counts = Counter(jd_tokens)

    matched = [word for word in jd_counts if word in resume_counts]
    missing = [word for word in jd_counts if word not in resume_counts]

    score = (len(matched) / len(jd_counts)) * 100 if jd_counts else 0
    return round(score, 2), matched, missing


# ---------------------------
# Streamlit App
# ---------------------------
def main():
    st.set_page_config(page_title="ATS Resume Score Checker", page_icon="📄", layout="wide")

    # Title Section
    st.markdown(
        """
        <div style="text-align: center; padding: 20px;">
            <h1 style="color:#2C3E50;">📄 ATS Resume Score Checker</h1>
            <p style="font-size:18px; color:#34495E;">
                Upload your resume and paste a job description to check your ATS match score.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Upload + JD input
    col1, col2 = st.columns([1, 2])
    with col1:
        uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
    with col2:
        jd_text = st.text_area("Paste Job Description here:", height=180)

    if uploaded_file and jd_text:
        if st.button("🚀 Check ATS Score", use_container_width=True):
            with st.spinner("Analyzing resume..."):
                resume_text = extract_resume_text(uploaded_file)
                resume_tokens = clean_text(resume_text)
                jd_tokens = clean_text(jd_text)

                score, matched, missing = calculate_score(resume_tokens, jd_tokens)

                # Show Score
                st.markdown("---")
                st.subheader("📊 ATS Match Score")
                st.progress(int(score))
                st.markdown(f"<h2 style='color:#27AE60;'>{score}%</h2>", unsafe_allow_html=True)

                # Show Keywords
                st.markdown("---")
                col1, col2 = st.columns(2)

                with col1:
                    st.success("✅ Matched Keywords")
                    if matched:
                        st.write(", ".join(matched))
                    else:
                        st.write("None")

                with col2:
                    st.error("❌ Missing Keywords")
                    if missing:
                        st.write(", ".join(missing))
                    else:
                        st.write("None")


if __name__ == "__main__":
    main()
