import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(jd, resume_text):
    model = genai.GenerativeModel('gemini-pro')
    input_prompt = f"""
    Analyze the provided resume and the job description and return a JSON structured response with details including:
    - matchPercentage: Job Description and Resume Match Percentage
    - missingKeywords: Missing Keywords and Skills
    - skillsSummary: Technical Skills Summary Suggestions
    - interviewQuestions: Potential Technical Interview Questions with suggested keywords to use in answers
    - projectsRequired: Projects Required for the Job Description
    - experienceRequired: Experience Required for the Job Description
    - suggestedProjects: Suggested Project Topics to Work On
    - profileSummary: Profile Summary Suggestions

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

        try:
            # Parse the JSON output
            analysis_json = json.loads(analysis)

            # Display JSON data in a professional manner
            st.subheader("Analysis Report")
            st.write("### Job Description and Resume Match Percentage")
            st.write(analysis_json.get('matchPercentage', 'No data available'))

            st.write("### Missing Keywords and Skills")
            st.write(analysis_json.get('missingKeywords', 'No data available'))

            st.write("### Technical Skills Summary Suggestions")
            st.write(analysis_json.get('skillsSummary', 'No data available'))

            st.write("### Potential Technical Interview Questions")
            questions = analysis_json.get('interviewQuestions', [])
            for question in questions:
                st.write(f"**Question:** {question['question']}")
                st.write(f"**Suggested Keywords:** {', '.join(question['keywords'])}")

            st.write("### Projects Required for the Job Description")
            st.write(analysis_json.get('projectsRequired', 'No data available'))

            st.write("### Experience Required for the Job Description")
            st.write(analysis_json.get('experienceRequired', 'No data available'))

            st.write("### Suggested Project Topics to Work On")
            suggested_projects = analysis_json.get('suggestedProjects', [])
            for project in suggested_projects:
                st.write(project)

            st.write("### Profile Summary Suggestions")
            st.write(analysis_json.get('profileSummary', 'No data available'))

        except json.JSONDecodeError:
            st.error("Failed to decode JSON from model response. Please check the model output format.")
    else:
        st.error("Please make sure to upload a PDF resume and enter the job description before submitting.")
