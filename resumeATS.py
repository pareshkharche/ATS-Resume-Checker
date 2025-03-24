import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PyPDF2 import PdfReader

# Load environment variables and configure API
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get Gemini output
def get_gemini_output(pdf_text, prompt):
    response = model.generate_content([pdf_text, prompt])
    return response.text

# Function to read PDF
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
            @apply bg-gradient-to-br from-gray-100 to-gray-200 p-8 rounded-3xl shadow-2xl transition-transform duration-300 hover:scale-103;
        }
        .custom-button {
            @apply bg-gradient-to-r from-blue-400 to-purple-500 hover:from-blue-500 hover:to-purple-600 text-gray-800 font-semibold py-3 px-8 rounded-full transition-colors duration-300 transform hover:scale-105;
        }
        .custom-input {
            @apply border border-gray-300 rounded-2xl p-4 w-full focus:ring-2 focus:ring-purple-300 focus:outline-none transition-shadow duration-300 hover:shadow-lg;
        }
        .custom-radio {
            @apply mr-6 cursor-pointer;
        }
        .custom-file-uploader {
            @apply border-2 border-dashed border-blue-400 rounded-2xl p-12 text-center cursor-pointer hover:border-purple-500 transition-colors duration-300 transform hover:scale-103;
        }
        .custom-sidebar {
            @apply bg-gradient-to-b from-gray-200 to-gray-100 p-8 rounded-2xl shadow-lg;
        }
        .custom-subheader{
            @apply text-xl font-semibold mb-4 text-gray-700;
        }
        .custom-sidebar a{
            @apply transition-colors duration-300 hover:text-blue-600;
        }
        .custom-sidebar h2, .custom-sidebar h3{
            @apply text-gray-800;
        }
        .custom-sidebar textarea{
            @apply border border-gray-300 rounded-2xl p-3 w-full focus:ring-2 focus:ring-purple-300 focus:outline-none transition-shadow duration-300 hover:shadow-md;
        }
        .custom-text{
            @apply text-gray-700;
        }
    </style>
""", unsafe_allow_html=True)

st.title("ResumeATS Pro")
st.subheader("Craft Your Future, One Resume at a Time")

with st.container():
    st.markdown('<div class="custom-container">', unsafe_allow_html=True)
    upload_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"], label_visibility="visible")

    job_description = st.text_area("Enter the job description (optional)", key="job_desc", height=150, placeholder="Paste job description here", label_visibility="visible")

    analysis_option = st.radio("Choose analysis type:", ["Quick Scan", "Detailed Analysis", "ATS Optimization"], key="analysis_type")

    if st.button("Analyze Resume", key="analyze_button", type="primary", use_container_width=True):
        if upload_file is not None:
            pdf_text = read_pdf(upload_file)
            if analysis_option == "Quick Scan":
                prompt = f"""You are ResumeChecker, an expert in resume analysis. Provide a quick scan of the following resume: 1. Identify the most suitable profession for this resume. 2. List 3 key strengths. 3. Suggest 2 quick improvements. 4. Give an overall ATS score out of 100. Resume: {pdf_text} Job description (if any): {job_description}"""
            elif analysis_option == "Detailed Analysis":
                prompt = f"""You are ResumeChecker, an expert in resume analysis. Provide a detailed analysis of the following resume: 1. Identify the most suitable profession. 2. List 5 strengths. 3. Suggest 3-5 improvements. 4. Rate: Impact, Brevity, Style, Structure, Skills (out of 10). 5. Review sections. 6. Give ATS score/100. Resume: {pdf_text} Job description (if any): {job_description}"""
            else:
                prompt = f"""You are ResumeChecker, an expert in ATS optimization. Analyze the resume: 1. Identify keywords from the job description. 2. Suggest reformatting. 3. Recommend keyword density changes. 4. Provide 3-5 points to tailor the resume. 5. Give ATS score/100. Resume: {pdf_text} Job description: {job_description}"""
            response = get_gemini_output(pdf_text, prompt)
            st.markdown('<p class="custom-subheader">Analysis Results</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="custom-text">{response}</p>', unsafe_allow_html=True)
            st.markdown('<p class="custom-subheader">Have questions about your resume?</p>', unsafe_allow_html=True)
            user_question = st.text_input("Ask me anything about your resume or the analysis:", key="user_question")
            if user_question:
                chat_prompt = f"""Based on the resume and analysis above, answer the question: {user_question} Resume: {pdf_text} Previous analysis: {response}"""
                chat_response = get_gemini_output(pdf_text, chat_prompt)
                st.markdown(f'<p class="custom-text">{chat_response}</p>', unsafe_allow_html=True)
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