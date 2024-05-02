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
    Please analyze the provided resume and the job description, and return a detailed report with:
    - Job Description and Resume Match Percentage
    - Technical Skills Summary Suggestions
    - Potential Technical Interview Questions with Suggested Keywords to use in answers
    - Projects Required for the Job Description
    - Experience Required for the Job Description
    - Suggested Project Topics to Work On
    - Profile Summary Suggestions
    
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
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf")

submit = st.button("Analyze")

if submit:
    if uploaded_file and jd:
        resume_text = input_pdf_text(uploaded_file)
        analysis = get_gemini_response(jd, resume_text)

        # Display the output in a cleaner way
        st.markdown("### Analysis Report")
        st.text_area("Result", value=analysis, height=300)
    else:
        st.error("Please make sure to upload a PDF resume and enter the job description before submitting.")

