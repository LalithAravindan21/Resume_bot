import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import json
import re
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def parse_to_json(model_output):
    # Regex searches to find data in the model's output text
    match_percentage = re.search(r'Match Percentage:\s*(\d+%|\w+)', model_output)
    skills_summary = re.search(r'Technical Skills Summary Suggestions:\s*(.*)', model_output)
    interview_questions = re.findall(r'Question:\s*(.*?); Keywords:\s*(.*?)\n', model_output)
    projects_required = re.search(r'Projects Required:\s*(.*)', model_output)
    experience_required = re.search(r'Experience Required:\s*(.*)', model_output)
    suggested_projects = re.search(r'Suggested Projects:\s*(.*)', model_output)
    profile_summary = re.search(r'Profile Summary:\s*(.*)', model_output)

    data = {
        "matchPercentage": match_percentage.group(1) if match_percentage else "No data available",
        "skillsSummary": skills_summary.group(1) if skills_summary else "No data available",
        "interviewQuestions": [{"question": q, "keywords": k} for q, k in interview_questions] if interview_questions else [],
        "projectsRequired": projects_required.group(1) if projects_required else "No data available",
        "experienceRequired": experience_required.group(1) if experience_required else "No data available",
        "suggestedProjects": suggested_projects.group(1).split(", ") if suggested_projects else [],
        "profileSummary": profile_summary.group(1) if profile_summary else "No data available"
    }
    return data

def get_gemini_response(jd, resume_text):
    model = genai.GenerativeModel('gemini-pro')
    input_prompt = f"""
    Analyze the provided resume and the job description:
    Please return the analysis in the following structured text format:
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
        st.write(f"**Job Description and Resume Match Percentage:** {analysis_json['matchPercentage']}")
        st.write(f"**Technical Skills Summary:** {analysis_json['skillsSummary']}")
        st.write("**Potential Technical Interview Questions:**")
        for question in analysis_json['interviewQuestions']:
            st.write(f"- **Question:** {question['question']}")
            st.write(f"  **Keywords:** {question['keywords']}")
        st.write(f"**Projects Required for the Job Description:** {analysis_json['projectsRequired']}")
        st.write(f"**Experience Required for the Job Description:** {analysis_json['experienceRequired']}")
        st.write("**Suggested Project Topics to Work On:**")
        for project in analysis_json['suggestedProjects']:
            st.write(f"- {project}")
        st.write(f"**Profile Summary Suggestions:** {analysis_json['profileSummary']}")
    else:
        st.error("Please make sure to upload a PDF resume and enter the job description before submitting.")
