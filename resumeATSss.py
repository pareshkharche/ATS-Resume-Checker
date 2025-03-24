import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PyPDF2 import PdfReader

# Load environment variables and configure API
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get Gemini output (DO NOT MODIFY)
def get_gemini_output(pdf_text, prompt):
    response = model.generate_content([pdf_text, prompt])
    return response.text

# Function to read PDF (DO NOT MODIFY)
def read_pdf(uploaded_file):
    if uploaded_file is not None:
        pdf_reader = PdfReader(uploaded_file)
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
        return pdf_text
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit UI
st.set_page_config(page_title="ResumeATS Pro", layout="wide")

# Tailwind CSS and Custom Styling
st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        .custom-container {
            @apply bg-indigo-50 p-8 rounded-lg shadow-md;
        }
        .custom-button {
            @apply bg-teal-600 hover:bg-teal-700 text-white font-bold py-2 px-4 rounded-full;
        }
        .custom-input {
            @apply border border-gray-300 rounded-md p-2 w-full;
        }
        .custom-radio {
            @apply mr-4;
        }
        .custom-file-uploader {
            @apply border-2 border-dashed border-teal-600 rounded-md p-8 text-center cursor-pointer;
        }
        .custom-sidebar {
            @apply bg-indigo-100 p-4;
        }
        .custom-slider > div > div > div > div {
            background-color: #9CA3AF;
        }
        .custom-slider > div > div > div > div[data-baseweb="slider-thumb"]{
            background-color: #4B5563;
            border:none;
        }
        .custom-slider > div > div > div > div[data-baseweb="slider-thumb"]:focus{
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5);
        }
    </style>
""", unsafe_allow_html=True)

st.title("ResumeATS Pro")
st.subheader("Optimize Your Resume for ATS and Land Your Dream Job")

with st.container():
    st.markdown('<div class="custom-container">', unsafe_allow_html=True)
    upload_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"], label_visibility="visible")

    job_description = st.text_area("Enter the job description (optional)", key="job_desc", height=150, placeholder="Paste job description here", label_visibility="visible")

    analysis_option = st.radio("Choose analysis type:", ["Quick Scan", "Detailed Analysis", "ATS Optimization"], key="analysis_type")

    if st.button("Analyze Resume", key="analyze_button", type="primary", use_container_width=True):
        if upload_file is not None:
            pdf_text = read_pdf(upload_file)
            if analysis_option == "Quick Scan":
                prompt = f"""You are ResumeChecker, an expert in resume analysis. Provide a quick scan of the following resume: 1. Identify the most suitable profession for this resume. 2. List 3 key strengths of the resume. 3. Suggest 2 quick improvements. 4. Give an overall ATS score out of 100. Resume text: {pdf_text} Job description (if provided): {job_description}"""
            elif analysis_option == "Detailed Analysis":
                prompt = f"""You are ResumeChecker, an expert in resume analysis. Provide a detailed analysis of the following resume: 1. Identify the most suitable profession for this resume. 2. List 5 strengths of the resume. 3. Suggest 3-5 areas for improvement with specific recommendations. 4. Rate the following aspects out of 10: Impact, Brevity, Style, Structure, Skills. 5. Provide a brief review of each major section (e.g., Summary, Experience, Education). 6. Give an overall ATS score out of 100 with a breakdown of the scoring. Resume text: {pdf_text} Job description (if provided): {job_description}"""
            else:
                prompt = f"""You are ResumeChecker, an expert in ATS optimization. Analyze the following resume and provide optimization suggestions: 1. Identify keywords from the job description that should be included in the resume. 2. Suggest reformatting or restructuring to improve ATS readability. 3. Recommend changes to improve keyword density without keyword stuffing. 4. Provide 3-5 bullet points on how to tailor this resume for the specific job description. 5. Give an ATS compatibility score out of 100 and explain how to improve it. Resume text: {pdf_text} Job description: {job_description}"""
            response = get_gemini_output(pdf_text, prompt)
            st.subheader("Analysis Results")
            st.write(response)
            st.subheader("Have questions about your resume?")
            user_question = st.text_input("Ask me anything about your resume or the analysis:", key="user_question")
            if user_question:
                chat_prompt = f"""Based on the resume and analysis above, answer the following question: {user_question} Resume text: {pdf_text} Previous analysis: {response}"""
                chat_response = get_gemini_output(pdf_text, chat_prompt)
                st.write(chat_response)
        else:
            st.error("Please upload a resume to analyze.")
    st.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="custom-sidebar">', unsafe_allow_html=True)
st.sidebar.title("Resources")
st.sidebar.markdown("""
- [Resume Writing Tips](https://cdn-careerservices.fas.harvard.edu/wp-content/uploads/sites/161/2023/08/College-resume-and-cover-letter-4.pdf)
- [ATS Optimization Guide](https://career.io/career-advice/create-an-optimized-ats-resume)
- [Interview Preparation](https://hbr.org/2021/11/10-common-job-interview-questions-and-how-to-answer-them)
""")
st.sidebar.title("Feedback")
st.sidebar.text_area("Help us improve! Leave your feedback:", key="feedback_area")
st.sidebar.button("Submit Feedback", key="submit_feedback", type="primary", use_container_width=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)