import streamlit as st
import google.generativeai as genai 
import os
import PyPDF2 as Pdf 
import json
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
input_prompt: |
    Hey, act like an experienced ATS (Applicant Tracking System) with a deep understanding of various technical roles and industries such as software engineering, data science, cybersecurity, DevOps, and more. Your task is to evaluate the provided resume in alignment with the given job description for the desired technical position without being overly creative. Strictly adhere to the specific job description, required skills, technologies, and responsibilities mentioned. If the job aligns with areas like web development, machine learning, cloud computing, or any other technical domain, focus your analysis solely on those relevant aspects. Considering the competitiveness of the job market, provide the best assistance for improving the resume by assigning a percentage match based on the job description and identifying missing technical keywords with high accuracy. Additionally, anticipate potential technical questions that a recruiter might ask based on the job description.

    Please provide the response in the following format:

    {
        "JD_Match": "Percentage",
        "Missing_Technical_Keywords": [
            "Keyword1",
            "Keyword2"
        ],
        "Technical_Skills_Summary_Suggestions": "Suggestions for enhancing the technical skills section",
        "Potential_Technical_Interview_Questions": [
            {
                "Question": "Random technical question 1",
                "Answer": "Answer 1"
            },
            {
                "Question": "Random technical question 2",
                "Answer": "Answer 2"
            },
            {
                "Question": "Random technical question 3",
                "Answer": "Answer 3"
            },
            {
                "Question": "Random technical question 4",
                "Answer": "Answer 4"
            },
            {
                "Question": "Random technical question 5",
                "Answer": "Answer 5"
            }
        ],
        "Technical_Projects_Required": [
            "Project mentioned in the resume",
            "Another project mentioned in the resume"
        ],
        "Technical_Experience_Required": {
            "Years_of_Experience": "Years of experience if mentioned in the resume",
            "No_Previous_Experience": "No previous experience if not mentioned"
        },
        "Desired_Job_Match": "Percentage"
    }
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
        
        # Parsing JSON response
        parsed_response = json.loads(response)
        
        st.subheader("Job Description Match")
        st.write("JD Match:", parsed_response["JD_Match"])

        st.subheader("Missing Technical Keywords")
        for keyword in parsed_response["Missing_Technical_Keywords"]:
            st.write(keyword)

        st.subheader("Technical Skills Summary Suggestions")
        st.write(parsed_response["Technical_Skills_Summary_Suggestions"])

        st.subheader("Potential Technical Interview Questions")
        for question in parsed_response["Potential_Technical_Interview_Questions"]:
            st.write("**Question:**", question["Question"])
            st.write("**Answer:**", question["Answer"])

        st.subheader("Technical Projects Required For This Job Description")
        for project in parsed_response["Technical_Projects_Required"]:
            st.write(project)

        st.subheader("Technical Experience Required")
        st.write("Years of Experience:", parsed_response["Technical_Experience_Required"]["Years_of_Experience"])
        st.write("No Previous Experience:", parsed_response["Technical_Experience_Required"]["No_Previous_Experience"])

        st.subheader("Desired Job Match")
        st.write("Desired Job Match:", parsed_response["Desired_Job_Match"])
