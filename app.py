import streamlit as st
import google.generativeai as genai 
import os
import PyPDF2 as Pdf 

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#GEMINI PRO RESPONSE
def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

#to extract the text from pdf
def input_pdf_text(uploaded_file):
    reader=Pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text


input_prompt="""
Hey, act like a skilled or very experienced ATS (Application Tracking System) with a deep understanding of the tech field, software engineering, data science, data analysis, and big data engineering. Your task is to evaluate the resume provided. You must consider that the job market is very competitive and provide the best assistance for improving the resumes. Assign a percentage matching based on the JD and identify the missing keywords with high accuracy.
Resume: {text}

Please provide the response in one single string with the structure:
{{"JD Match": "%", "Missing Keywords": [], "Profile Summary": ""}}
"""

## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt)
        st.subheader(response)
