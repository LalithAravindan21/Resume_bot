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
    ---Job Description---
    {jd}
    
    ---Resume Text---
    {resume_text}
    
    Please return a comprehensive evaluation in JSON format.
    """
    response = model.generate_content(input_prompt)
    print("Model response for debugging:", response.text)  # Debugging output
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() if page.extract_text() else ''
    return text

st.title("Smart ATS")
st.text("Improve Your Resume with ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file and jd:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(jd, text)

        if response.startswith('{'):
            try:
                parsed_response = json.loads(response)
                st.json(parsed_response)  # Display the JSON in a preformatted block
            except json.JSONDecodeError:
                st.error("Failed to decode JSON from model response.")
                st.text_area("Raw response", response)  # Display raw response for troubleshooting
        else:
            st.error("Unexpected format from model response, check the debug logs.")
            st.text_area("Raw response", response)
    else:
        st.error("Please make sure to upload a PDF resume and enter the job description before submitting.")
