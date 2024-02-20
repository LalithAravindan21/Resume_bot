import streamlit as st
import google.generativeai as genai 
import os
import PyPDF2 as Pdf 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# GEMINI PRO RESPONSE
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

# Function to extract the text from PDF
def input_pdf_text(uploaded_file):
    reader = Pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Function to calculate cosine similarity between two texts
def calculate_similarity(text1, text2):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([text1, text2])
    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return similarity_score

# Define job roles based on current demand
current_demand_job_roles = ["Data Scientist", "Cybersecurity Analyst", "Software Developer", "Digital Marketing Specialist", "Cloud Engineer", "AI/ML Engineer", "Financial Analyst", "Healthcare Administrator", "UX/UI Designer", "Project Manager"]

# Define other job roles
other_job_roles = ["Tech Support Specialist", "Customer Service Representative", "Administrative Assistant", "Sales Associate", "Teacher", "Nurse", "Graphic Designer", "Accountant", "Human Resources Specialist", "Research Assistant"]

# Combine all job roles
all_job_roles = current_demand_job_roles + other_job_roles

# Input prompt for resume evaluation
input_prompt = """
Hey, act like an experienced ATS (Applicant Tracking System) with a deep understanding of various industries such as tech, finance, and healthcare. Your task is to evaluate the provided resume in alignment with the given job description for the desired position. Considering the competitiveness of the job market, provide the best assistance for improving the resume by assigning a percentage match based on the job description and identifying missing keywords with high accuracy. Additionally, anticipate potential questions that a recruiter might ask based on the job description.

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

# Streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")

# Allow the user to select one or more job roles from the multi-select box
selected_job_roles = st.multiselect("Select Your Job Roles", all_job_roles)

jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

generate = st.button("Generate Job Description")

if generate:
    if selected_job_roles:
        selected_job_roles_str = ", ".join(selected_job_roles)  # Convert list to string
        input_prompt_with_roles = f"{selected_job_roles_str} {input_prompt}"  # Add selected job roles to the input prompt
        generated_description = get_gemini_response(input_prompt_with_roles)
        st.subheader("Generated Job Description:")
        st.write(generated_description)

        if uploaded_file is not None:
            resume_text = input_pdf_text(uploaded_file)
            nlp = spacy.load("en_core_web_sm")
            resume_doc = nlp(resume_text)
            resume_keywords = [token.text for token in resume_doc if token.pos_ in ['NOUN', 'PROPN']]
            
            job_description_doc = nlp(generated_description)
            job_description_keywords = [token.text for token in job_description_doc if token.pos_ in ['NOUN', 'PROPN']]
            
            all_keywords = list(set(resume_keywords + job_description_keywords))  # Combine keywords from both resume and job description
            generated_questions = generate_questions(all_keywords)

            st.subheader("Generated Questions:")
            for i, question in enumerate(generated_questions, start=1):
                st.write(f"{i}. {question}")

            # Calculate similarity between job description and resume
            similarity_score = calculate_similarity(generated_description, resume_text)
            st.subheader("JD vs Resume Match Meter:")
            st.write(f"The job description and resume match at {similarity_score * 100:.2f}%.")

            # Suggest skills or courses based on job role and resume
            suggested_skills = suggest_skills(selected_job_roles_str, resume_text)
            st.subheader("Suggested Skills or Courses:")
            for skill in suggested_skills:
                st.write(skill)
    else:
        st.warning("Please select at least one job role before generating the job description.")
