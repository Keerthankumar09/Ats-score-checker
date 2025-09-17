# 📄 ATS Resume Score Checker

A Streamlit web application that helps job seekers evaluate their resumes against job descriptions using ATS (Applicant Tracking System) keyword matching.  

## 🚀 Features
- Upload resume in **PDF** or **DOCX** format  
- Paste or upload a **Job Description (JD)**  
- Automated **keyword extraction & cleaning** using NLP  
- Calculates **ATS Score (%)** based on keyword overlap  
- Highlights **Matched** and **Missing** keywords  
- Simple and interactive **Streamlit UI**

## 🛠️ Tech Stack
- **Python**
- **Streamlit**
- **NLTK** (Stopwords, Text Processing)
- **PyPDF2** & **python-docx** (Resume parsing)
- **Collections.Counter** for keyword scoring


## ⚡ Installation
'''bash'''
git clone https://github.com/YourUsername/ats-score-checker.git
cd ats-score-checker
pip install -r requirements.txt

Run the App
streamlit run app.py



