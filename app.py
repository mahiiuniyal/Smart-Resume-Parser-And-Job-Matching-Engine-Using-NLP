import streamlit as st
import os
import docx2txt
from pdfminer.high_level import extract_text
from sentence_transformers import SentenceTransformer, util
import spacy
import pandas as pd
import matplotlib.pyplot as plt
import shutil

# Load models
nlp = spacy.load("en_core_web_sm")
bert_model = SentenceTransformer('all-MiniLM-L6-v2')

# Skill list
SKILL_KEYWORDS = [
    'python', 'java', 'c++', 'javascript', 'sql', 'html', 'css',
    'machine learning', 'deep learning', 'tensorflow', 'keras',
    'nlp', 'cloud', 'aws', 'azure', 'gcp', 'docker', 'kubernetes',
    'git', 'linux', 'data analysis', 'pandas', 'numpy', 'matplotlib',
    'cybersecurity', 'firewall', 'vulnerability', 'penetration testing'
]

# Functions
def extract_text_from_file(file_path):
    if file_path.endswith('.pdf'):
        return extract_text(file_path)
    elif file_path.endswith('.docx'):
        return docx2txt.process(file_path)
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        raise ValueError("Unsupported file format: " + file_path)

def extract_skills(text):
    doc = nlp(text.lower())
    return list({token.text for token in doc if token.text in SKILL_KEYWORDS})

def calculate_bert_similarity(text1, text2):
    embeddings = bert_model.encode([text1, text2], convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1])
    return round(float(similarity.item()) * 100, 2)

def run_matching(resume_paths, jd_paths):
    results = []
    for resume_path in resume_paths:
        resume_text = extract_text_from_file(resume_path)
        resume_skills = extract_skills(resume_text)

        for jd_path in jd_paths:
            jd_text = extract_text_from_file(jd_path)
            jd_skills = extract_skills(jd_text)

            match_score = calculate_bert_similarity(resume_text, jd_text)
            matched_skills = set(resume_skills).intersection(jd_skills)
            skill_match_score = round(len(matched_skills) / len(jd_skills) * 100, 2) if jd_skills else 0.0

            results.append({
                "Resume": os.path.basename(resume_path),
                "Job Description": os.path.basename(jd_path),
                "Match Score (%)": match_score,
                "Skill Match Score (%)": skill_match_score,
                "Matched Skills": ', '.join(matched_skills),
                "Resume Skills": ', '.join(resume_skills),
                "JD Skills": ', '.join(jd_skills)
            })
    return pd.DataFrame(results)

# Streamlit App UI
st.set_page_config(page_title="Smart Resume Matcher", layout="wide")
st.title("🧠 Smart Resume Parser + Job Matcher")
st.markdown("Upload resumes and job descriptions to compare skills and get match scores.")

resumes = st.file_uploader("Upload Resumes (PDF/DOCX)", accept_multiple_files=True)
jds = st.file_uploader("Upload Job Descriptions (DOCX/TXT)", accept_multiple_files=True)

if st.button("Run Matching") and resumes and jds:
    with st.spinner("Processing..."):

        os.makedirs("resumes", exist_ok=True)
        os.makedirs("jds", exist_ok=True)

        resume_paths = []
        jd_paths = []

        for r in resumes:
            path = os.path.join("resumes", r.name)
            with open(path, "wb") as f: f.write(r.read())
            resume_paths.append(path)

        for j in jds:
            path = os.path.join("jds", j.name)
            with open(path, "wb") as f: f.write(j.read())
            jd_paths.append(path)

        df = run_matching(resume_paths, jd_paths)

        st.success("✅ Matching Complete!")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", data=csv, file_name="matches.csv", mime="text/csv")

        # Charts
        st.subheader("📊 Top 5 Matches by Semantic Score")
        top_bert = df.sort_values(by="Match Score (%)", ascending=False).head(5)
        fig, ax = plt.subplots()
        ax.barh(top_bert["Resume"], top_bert["Match Score (%)"], color='skyblue')
        ax.set_xlabel("Match Score (%)")
        ax.invert_yaxis()
        st.pyplot(fig)

        st.subheader("🛠️ Top 5 Matches by Skill Score")
        top_skills = df.sort_values(by="Skill Match Score (%)", ascending=False).head(5)
        fig2, ax2 = plt.subplots()
        ax2.barh(top_skills["Resume"], top_skills["Skill Match Score (%)"], color='orange')
        ax2.set_xlabel("Skill Match Score (%)")
        ax2.invert_yaxis()
        st.pyplot(fig2)

        # Clean
        shutil.rmtree("resumes")
        shutil.rmtree("jds")
