import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get analysis response from Google Gemini
def get_gemini_response(jd, resume_text):
    model = genai.GenerativeModel('gemini-pro')
    input_prompt = f"""
    {jd}
    Resume:
    {resume_text}

    Act as an experienced ATS (Applicant Tracking System) with a deep understanding of various technical roles and industries such as software engineering, data science, cybersecurity, DevOps, and more. Evaluate the provided resume in alignment with the given job description for the desired technical position. Strictly adhere to the specific job description, required skills, technologies, and responsibilities mentioned. If the job aligns with technical domains like web development, machine learning, cloud computing, or others, focus your analysis specifically on those areas. Considering the competitiveness of the job market, help improve the resume by:
    - Assigning a percentage match based on the job description.
    - Identifying missing technical keywords with high accuracy.
    - Anticipating potential technical interview questions with suggested keywords to use in answers, instead of providing full answers.
    - Suggesting project topics to work on based on gaps or needed expansions from the projects listed in the resume.
    - Highlighting specific experiences or accomplishments to emphasize in the resume.
    - Generating practice questions related to the projects listed in the resume to help the candidate prepare for potential project-related questions during interviews.

    Additionally, for roles in the arts, science, and commerce fields:
    - Assign a percentage match based on the job description.
    - Identify missing academic keywords with high accuracy.
    - Anticipate potential interview questions with suggested keywords to use in answers, instead of providing full answers.
    - Suggest research or project topics to work on based on gaps or needed expansions from the projects listed in the resume.
    - Highlight specific experiences or accomplishments to emphasize in the resume.
    - Generating practice questions related to the projects listed in the resume to help the candidate prepare for potential project-related questions during interviews.

    Please format your response as follows:
    {{
        "JD_Match": "Percentage",
        "Missing_Technical_Keywords": [
            "Keyword1",
            "Keyword2"
        ],
        "Missing_Academic_Keywords": [
            "Keyword1",
            "Keyword2"
        ],
        "Technical_Skills_Summary_Suggestions": "Suggestions for enhancing the technical skills section",
        "Skills_Summary_Suggestions": "Suggestions for enhancing the skills section",
        "Potential_Technical_Interview_Questions": [
            {{
                "Question": "Technical question 1",
                "Keywords": ["Keyword1", "Keyword2"]
            }},
            {{
                "Question": "Technical question 2",
                "Keywords": ["Keyword3", "Keyword4"]
            }},
            {{
                "Question": "Technical question 3",
                "Keywords": ["Keyword5", "Keyword6"]
            }},
            {{
                "Question": "Technical question 4",
                "Keywords": ["Keyword7", "Keyword8"]
            }},
            {{
                "Question": "Technical question 5",
                "Keywords": ["Keyword9", "Keyword10"]
            }}
        ],
        "Potential_Interview_Questions": [
            {{
                "Question": "Interview question 1",
                "Keywords": ["Keyword1", "Keyword2"]
            }},
            {{
                "Question": "Interview question 2",
                "Keywords": ["Keyword3", "Keyword4"]
            }},
            {{
                "Question": "Interview question 3",
                "Keywords": ["Keyword5", "Keyword6"]
            }},
            {{
                "Question": "Interview question 4",
                "Keywords": ["Keyword7", "Keyword8"]
            }},
            {{
                "Question": "Interview question 5",
                "Keywords": ["Keyword9", "Keyword10"]
            }}
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
            "Topic 1 based on existing projects to expand",
            "New Topic 2 related to job requirements"
        ],
        "Suggested_Research_Topics": [
            "Topic 1 based on existing projects to expand",
            "New Topic 2 related to job requirements"
        ],
        "Technical_Experience_Required": {{
            "Years_of_Experience": "Years of experience if mentioned in the resume",
            "No_Previous_Experience": "No previous experience if not mentioned"
        }},
        "Experience_Required": {{
            "Years_of_Experience": "Years of experience if mentioned in the resume",
            "No_Previous_Experience": "No previous experience if not mentioned"
        }},
        "Desired_Job_Match": "Percentage",
        "Highlighted_Experiences_Accomplishments": [
            "Experience 1 to emphasize",
            "Accomplishment 2 to emphasize"
        ],
        "Project_Practice_Questions": {{
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
        }}
    }}
    """

    response = model.generate_content(input_prompt)
    return response.text

# Function to extract text from uploaded PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() if page.extract_text() else ''
    return text

# Streamlit app layout
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
