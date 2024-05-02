import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import re
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def parse_to_json(model_output):
    # Flexible regex searches to handle variations in the model's output
    match_percentage = re.search(r'Match Percentage:\s*(\S+)', model_output)
    skills_summary = re.search(r'Technical Skills Summary Suggestions:\s*(.*?)(?=\n|$)', model_output, re.DOTALL)
    interview_questions = re.findall(r'Question:\s*(.*?); Keywords:\s*(.*?)(?=\n|$)', model_output)
    projects_required = re.search(r'Projects Required:\s*(.*?)(?=\n|$)', model_output, re.DOTALL)
    experience_required = re.search(r'Experience Required:\s*(.*?)(?=\n|$)', model_output, re.DOTALL)
    suggested_projects = re.search(r'Suggested Projects:\s*(.*?)(?=\n|$)', model_output, re.DOTALL)
    profile_summary = re.search(r'Profile Summary:\s*(.*?)(?=\n|$)', model_output, re.DOTALL)

    data = {
        "matchPercentage": match_percentage.group(1) if match_percentage else "No data available",
        "skillsSummary": skills_summary.group(1).strip() if skills_summary else "No data available",
        "interviewQuestions": [{"question": q.strip(), "keywords": k.strip()} for q, k in interview_questions],
        "projectsRequired": projects_required.group(1).strip() if projects_required else "No data available",
        "experienceRequired": experience_required.group(1).strip() if experience_required else "No data available",
        "suggestedProjects": suggested_projects.group(1).split(", ") if suggested_projects else [],
        "profileSummary": profile_summary.group(1).strip() if profile_summary else "No data available"
    }
    return data

def get_gemini_response(jd, resume_text):
    model = genai.GenerativeModel('gemini-pro')
    input_prompt = f"""
    Analyze the provided resume and the job description:
    Please return the analysis in a structured text format:
    Match Percentage: [Percentage]
    Technical Skills Summary Suggestions: [Suggestions]
    Questions and Keywords: [List questions with keywords]
    Projects Required: [Required projects]
    Experience Required: [Experience details]
    Suggested Projects: [Project suggestions]
    Profile Summary: [Summary]

    ---Job Description---
    {jd}

    ---Resume Text---
    {resume_text}
    """
    response = model.generate_content(input_prompt)
    print("Debug Model Output:", response.text)  # This line helps to debug the output format
    return parse_to_json(response.text)

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
        analysis_json = get_gemini_response(jd, resume_text)

        st.subheader("Analysis Report")
        st.json(analysis_json)  # Display the JSON formatted output
    else:
        st.error("Please make sure to upload a PDF resume and enter the job description before submitting.")
