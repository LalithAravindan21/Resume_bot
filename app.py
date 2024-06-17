import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(jd, resume_text):
    model = genai.GenerativeModel('gemini-pro')
   {
    "JD_Match": "Percentage",
    "Missing_Technical_Keywords": [
        "Keyword1",
        "Keyword2"
    ],
    "Missing_Academic_Keywords": [
        "Keyword1",
        "Keyword2"
    ],
    "Technical_Skills_Summary_Suggestions": "Suggestions for enhancing the technical skills section, focusing on the required skills and technologies mentioned in the JD, and highlighting any advanced or niche skills.",
    "Skills_Summary_Suggestions": "Suggestions for enhancing the skills section, ensuring all necessary skills from the JD are covered and highlighting any relevant certifications or unique skills.",
    "Potential_Technical_Interview_Questions": [
        {
            "Question": "Technical question 1",
            "Keywords": ["Keyword1", "Keyword2"]
        },
        {
            "Question": "Technical question 2",
            "Keywords": ["Keyword3", "Keyword4"]
        },
        {
            "Question": "Technical question 3",
            "Keywords": ["Keyword5", "Keyword6"]
        },
        {
            "Question": "Technical question 4",
            "Keywords": ["Keyword7", "Keyword8"]
        },
        {
            "Question": "Technical question 5",
            "Keywords": ["Keyword9", "Keyword10"]
        }
    ],
    "Potential_Interview_Questions": [
        {
            "Question": "Interview question 1",
            "Keywords": ["Keyword1", "Keyword2"]
        },
        {
            "Question": "Interview question 2",
            "Keywords": ["Keyword3", "Keyword4"]
        },
        {
            "Question": "Interview question 3",
            "Keywords": ["Keyword5", "Keyword6"]
        },
        {
            "Question": "Interview question 4",
            "Keywords": ["Keyword7", "Keyword8"]
        },
        {
            "Question": "Interview question 5",
            "Keywords": ["Keyword9", "Keyword10"]
        }
    ],
    "Technical_Projects_Required": [
        "Project mentioned in the resume",
        "Another project mentioned in the resume"
    ],
    "Projects_Required": [
        "Project mentioned in the resume",
        "Another project mentioned in the resume"
    ],
    "Suggested_Project_Topics": [
        "Topic 1 based on existing projects to expand, focusing on technologies or methodologies mentioned in the JD",
        "New Topic 2 related to job requirements, ensuring alignment with the latest industry trends and practices"
    ],
    "Suggested_Research_Topics": [
        "Topic 1 based on existing projects to expand, ensuring relevance to current scientific or academic advancements",
        "New Topic 2 related to job requirements, emphasizing innovative or underexplored areas"
    ],
    "Technical_Experience_Required": {
        "Years_of_Experience": "Years of experience if mentioned in the resume",
        "No_Previous_Experience": "No previous experience if not mentioned"
    },
    "Experience_Required": {
        "Years_of_Experience": "Years of experience if mentioned in the resume",
        "No_Previous_Experience": "No previous experience if not mentioned"
    },
    "Desired_Job_Match": "Percentage",
    "Highlighted_Experiences_Accomplishments": [
        "Experience 1 to emphasize, particularly those aligning with job responsibilities and demonstrating impact or success",
        "Accomplishment 2 to emphasize, focusing on quantifiable achievements and recognitions"
    ],
    "Project_Practice_Questions": {
        "Project_Name_1": [
            "Practice question 1 for Project_Name_1, aiming to assess understanding of key technologies and methodologies used",
            "Practice question 2 for Project_Name_1, focusing on problem-solving and project outcomes",
            "Practice question 3 for Project_Name_1, exploring challenges faced and how they were overcome",
            "Practice question 4 for Project_Name_1, inquiring about teamwork and collaboration aspects",
            "Practice question 5 for Project_Name_1, covering future improvements or extensions"
        ],
        "Project_Name_2": [
            "Practice question 1 for Project_Name_2, targeting core technical skills and their application",
            "Practice question 2 for Project_Name_2, emphasizing innovation and creativity in the project",
            "Practice question 3 for Project_Name_2, covering data analysis and decision-making processes",
            "Practice question 4 for Project_Name_2, discussing challenges faced and solutions implemented",
            "Practice question 5 for Project_Name_2, considering future improvements or extensions"
        ]
        // more projects and questions as required
    }
}


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

        st.markdown("### Detailed Analysis Report")
        # Let's assume the output is well formatted in the given order and consistently uses similar headings.
        # Below is a simple string parsing example, assuming the model's output is consistently formatted.
        analysis_parts = analysis.split('\n')
        match_percentage = next((line for line in analysis_parts if "Match Percentage" in line), "Match Percentage not available.")
        resume_summary = next((line for line in analysis_parts if "Profile Summary Suggestions" in line), "Profile summary not available.")

        st.markdown("#### Job Description and Resume Match Percentage")
        st.markdown(match_percentage)

        st.markdown("#### Resume Summary")
        st.markdown(resume_summary)

        # Display other parts
        for part in analysis_parts:
            if part.strip() and part not in [match_percentage, resume_summary]:  # Avoid repeating parts
                st.markdown(part)
    else:
        st.error("Please make sure to upload a PDF resume and enter the job description before submitting.")
