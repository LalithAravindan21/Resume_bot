import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(jd, resume_text):
    model = genai.GenerativeModel('gemini-pro')
    input_prompt = f"""
    Analyze the provided resume and the job description. Provide a detailed report with:
    1. Job Description and Resume Match Percentage.
    2. Missing Keywords and Skills.
    3. Technical Skills Summary Suggestions.
    4. Potential Technical Interview Questions with suggested keywords to use in answers.
    5. Projects Required for the Job Description.
    6. Experience Required for the Job Description.
    7. Suggested Project Topics to Work On, including any revisions or expansions on projects mentioned in the resume.
    8. Profile Summary Suggestions.

    ---Job Description---
    {jd}
    
    ---Resume Text---
    {resume_text}
    """
    response = model.generate_content(input_prompt)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() if page.extract_text() else ''
    return text

st.title("Smart ATS - Enhance Your Resume")
jd = st.text_area("Paste the Job Description", height=150)
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf")

submit = st.button("Analyze")

if submit:
    if uploaded_file and jd:
        resume_text = input_pdf_text(uploaded_file)
        analysis = get_gemini_response(jd, resume_text)

        st.markdown("### Analysis Report")
        analysis_parts = analysis.split('\n')
        for part in analysis_parts:
            if part.strip():  # Check if the line is not just whitespace
                st.markdown(part)  # Use markdown to render each line
    else:
        st.error("Please make sure to upload a PDF resume and enter the job description before submitting.")
