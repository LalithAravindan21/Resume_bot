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
    Please analyze the provided resume and the job description, and return a JSON structured response with details including match percentage, skills summary, interview questions with hints, required projects, experience needed, and suggested project topics.
    
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

submit = st.button("Submit")

if submit:
    if uploaded_file and jd:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(jd, text)

        try:
            parsed_response = json.loads(response)
            
            st.subheader("Job Description Match")
            st.write("JD Match Percentage:", parsed_response.get("JD_Match_Percentage", "No data available"))

            st.subheader("Technical Skills Summary Suggestions")
            st.write(parsed_response.get("Technical_Skills_Summary_Suggestions", "No suggestions available"))

            st.subheader("Potential Technical Interview Questions")
            for question in parsed_response.get("Potential_Technical_Interview_Questions", []):
                st.write("**Question:**", question["Question"])
                st.write("**Hints to use:**", ', '.join(question["Hints"]))

            st.subheader("Technical Projects Required For This Job Description")
            projects_required = parsed_response.get("Technical_Projects_Required", [])
            if projects_required:
                for project in projects_required:
                    st.write(project)
            else:
                st.write("No specific projects required.")

            st.subheader("Technical Experience Required")
            st.write(parsed_response.get("Technical_Experience_Required", "No specific experience details available"))

            st.subheader("Suggested Project Topics to Work On")
            suggested_projects = parsed_response.get("Suggested_Project_Topics", [])
            if suggested_projects:
                for project in suggested_projects:
                    st.write(project)
            else:
                st.write("No suggested project topics available.")

        except json.JSONDecodeError:
            st.error("Failed to decode JSON from model response. Please check the model output format.")
    else:
        st.error("Please make sure to upload a PDF resume and enter the job description before submitting.")
