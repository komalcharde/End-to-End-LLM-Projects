from dotenv import load_dotenv
import streamlit as st
import os
from PyPDF2 import PdfReader
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    """
    Gets a response from the Gemini model.

    Args:
        input: The input string containing the prompt and data.

    Returns:
        The response from the Gemini model.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(input)
        return response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        return f"An error occurred while generating the response: {e}"

def input_pdf_text(uploaded_file):
    """
    Extracts text from a PDF file.

    Args:
        uploaded_file: The uploaded PDF file.

    Returns:
        The extracted text from the PDF.
    """
    if uploaded_file is not None:
        try:
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return None
    return None

# Streamlit UI
st.title("Smart ATS")
st.text("Optimize Your Resume for ATS Compatibility")

jd = st.text_area("Paste the Job Description", placeholder="Enter the job description here...")
uploaded_file = st.file_uploader("Upload Your Resume (PDF format only)", type="pdf", help="Please upload a valid PDF file.")
submit = st.button("Submit")

if submit:
    if jd.strip() == "":
        st.warning("Please provide a job description.")
    elif uploaded_file is None:
        st.warning("Please upload a PDF file.")
    else:
        # Process the resume and job description
        text = input_pdf_text(uploaded_file)
        if text:
            input_prompt = f"""
            Hey Act like a skilled or very experienced ATS (Application Tracking System)
            with a deep understanding of the tech field, software engineering, data science, data analyst, and big data engineer. Your task is to evaluate
            the resume based on the given job description. You must consider the job market is very competitive and you should provide
            the best assistance for improving the resumes. Assign the percentages Matching based
            on 2D and
            the missing keywords with high accuracy.
            resume:{text}
            description:{jd}
            I want response in one single string having the structure
            {{"JD Match":"%","MissingKeyword":[],"Profile Summary":""}}
            """
            try:
                response = get_gemini_response(input_prompt)
                st.subheader("Evaluation Result")
                st.text(response)
            except Exception as e:
                st.error(f"An error occurred while processing your request: {e}")
        else:
            st.error("Could not extract text from the uploaded PDF. Please ensure the file is not encrypted or corrupted.")
