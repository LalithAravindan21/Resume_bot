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
Hey, act like an experienced ATS (Applicant Tracking System) with a deep understanding of various industries such as tech, finance, and healthcare. Your task is to evaluate the provided resume in alignment with the given job description for the desired position without being more creative and being align with the specefic job description and technology mentioned.If all the responsibilities is according to the web dev , machine learning or any other technology just stick to the topic and provide the results. Considering the competitiveness of the job market, provide the best assistance for improving the resume by assigning a percentage match based on the job description and identifying missing keywords with high accuracy. Additionally, anticipate potential questions that a recruiter might ask based on the job description.

Please provide the response in the following format:

JD Match: Percentage
Missing Keywords: 
- Keyword1
- Keyword2
Profile Summary Suggestions: 
- Suggestions for profile summary enhancements
Potential Interview Questions: 
1. {{Random question 1}}
   - Answer 1
2. {{Random question 2}}
   - Answer 2
3. {{Random question 3}}
   - Answer 3
4. {{Random question 4}}
   - Answer 4
5. {{Random question 5}}
   - Answer 5

Projects Required For This Job Description: 
1. Project mentioned in the resume
2. Another project mentioned in the resume
Experience Required according to the Job Description: 
- Years of experience if mentioned in the resume
- No previous experience if not mentioned
Desired Job Match: Percentage
"""
# Below this line, you would handle the generation of random questions programmatically in your application before sending the prompt for evaluation.

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
