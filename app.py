import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Google API for the generative model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(jd, resume_text):
    model = genai.GenerativeModel('gemini-pro')
    input_prompt = f"""
    As an advanced ATS, your role is to analyze a resume provided below and assess it against a detailed job description for a technical position. Focus on the job's specific requirements including skills, technologies, responsibilities, and industry relevance. Generate a response in JSON format that provides a comprehensive evaluation aligned with the job description provided.

    ---Job Description---
    {jd}

    ---Resume Text---
    {resume_text}

    Your output should include:
    - A match percentage with the job description.
    - Missing technical keywords not found in the resume.
    - Suggestions for improving the technical skills section.
    - Potential technical interview questions with key terms for hints.
    - A list of projects mentioned in the resume.
    - Suggested new project topics relevant to the job.
    - Detailed technical experience requirements including necessary years of experience.
    - Desired job match percentage.
    """
    response = model.generate_content(input_prompt)
    print("Model Response:", response.text)  # Debugging line to check model output
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() if page.extract_text() else ''
    return text

# Streamlit user interface
st.title("Smart ATS")
st.text("Improve Your Resume with ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the pdf file.")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None and jd:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(jd, text)

        try:
            # Attempt to parse the JSON response
            parsed_response = json.loads(response)

            # If parsing is successful, use parsed_response to update the UI components
            st.subheader("Job Description Match")
            st.write("JD Match:", parsed_response.get("JD_Match", "No data"))

            st.subheader("Missing Technical Keywords")
            missing_keywords = parsed_response.get("Missing_Technical_Keywords", [])
            if missing_keywords:
                for keyword in missing_keywords:
                    st.write(keyword)
            else:
                st.write("No missing keywords identified.")

            # Continue adding sections following the same pattern
            # Ensure all keys match those expected in the JSON structure

        except json.JSONDecodeError:
            st.error("Failed to decode JSON from model response. Please check the model output format.")
            print("Failed JSON:", response)  # Log the problematic JSON for debugging
    else:
        st.error("Please make sure to upload a PDF resume and enter the job description before submitting.")
