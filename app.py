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


input_prompt = """
Hello! I'm here to assist you as an experienced ATS (Application Tracking System) specializing in the tech industry. To provide you with the best feedback, please specify the position you're interested in:

Desired Position: {desired_position}

Now, please share your resume, and I'll evaluate it based on the provided job description and your desired position. Considering the competitiveness of the job market, I'll assess the resume's alignment with the job requirements, assign a percentage match, identify any missing keywords, and provide a profile summary highlighting your relevant experiences and skills.

Resume: {text}

Please provide the response in a professional format:

JD Match: %
Missing Keywords: 
Profile Summary: 
Anticipated Questions:
- 
- 
- 

Additionally, I'll analyze your past projects and experiences mentioned in the resume to assess how well they align with the desired position.
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
