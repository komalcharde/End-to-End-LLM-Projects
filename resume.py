from dotenv import load_dotenv
import streamlit as st
import os
import fitz  # PyMuPDF for PDF handling
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Gemini AI API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Google API Key is missing! Please set it in your .env file.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# Function to extract text from the uploaded PDF file
def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from the uploaded PDF file.

    Args:
        uploaded_file: The uploaded PDF file.

    Returns:
        Extracted text from the PDF (or error message).
    """
    if uploaded_file is not None:
        try:
            # Read the file as bytes
            pdf_bytes = uploaded_file.getvalue()
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")  # Open PDF from bytes

            # Extract text from all pages
            pdf_text = "\n".join([page.get_text("text") for page in pdf_document]).strip()

            # Debugging: Print extracted text
            print("Extracted PDF Text:\n", pdf_text[:500])  # Print first 500 characters for debugging

            # Check if PDF text is empty (possible scanned PDF)
            if not pdf_text:
                return "⚠️ No selectable text found! Try using a PDF with real text (not images)."

            return pdf_text

        except Exception as e:
            st.error(f"❌ Error processing PDF: {e}")
            return None
    else:
        return None

# Function to get a response from Google Gemini AI
def get_gemini_response(input_text, pdf_text, prompt):
    """
    Generates a response from the Gemini AI model.

    Args:
        input_text: Job description provided by the user.
        pdf_text: Extracted text from the uploaded resume PDF.
        prompt: Instruction for AI processing.

    Returns:
        The AI-generated response.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')  # Use the latest available Gemini model
    try:
        response = model.generate_content([input_text, pdf_text, prompt])
        return response.text
    except Exception as e:
        st.error(f"❌ Error generating response: {e}")
        return f"An error occurred while generating the response: {e}"

# Streamlit UI
st.set_page_config(page_title="ATS Resume Expert")
st.header("📄 ATS Tracking System - Resume Analyzer")

# User input: Job description
input_text = st.text_area("🔍 Enter the job description:", key="input")

# Upload resume as a PDF
uploaded_file = st.file_uploader("📤 Upload your resume (PDF format)", type=["pdf"])

if uploaded_file:
    st.success("✅ PDF uploaded successfully!")

# Button selections
submit1 = st.button("📊 Analyze Resume")
submit2 = st.button("📈 Improve Skills")
submit3 = st.button("🔑 Missing Keywords")

# AI Prompts
input_prompt1 = """
You are an experienced HR professional specializing in technical hiring.
Your task is to analyze the given resume against the job description.
Provide a professional evaluation, highlight strengths, and identify areas of improvement.
"""

input_prompt2 = """
You are an HR manager with expertise in technical hiring.
Review the resume and suggest areas where the candidate can improve their skills to better match the job description.
"""

input_prompt3 = """
You are an AI-powered ATS (Applicant Tracking System) specialist.
Analyze the resume and compare it to the job description.
Provide a percentage match, list missing keywords, and suggest final improvements.
"""

# Button Actions
if submit1 or submit2 or submit3:
    if not uploaded_file:
        st.error("⚠️ Please upload a resume first!")
    else:
        pdf_text = extract_text_from_pdf(uploaded_file)

        if not pdf_text:
            st.error("❌ Could not extract text from the PDF. Please check the file and try again.")
        elif "⚠️ No selectable text found" in pdf_text:
            st.warning(pdf_text)  # Show warning if scanned PDF detected
        else:
            if submit1:
                response = get_gemini_response(input_text, pdf_text, input_prompt1)
                st.subheader("📊 Resume Analysis:")
                st.write(response)

            elif submit2:
                response = get_gemini_response(input_text, pdf_text, input_prompt2)
                st.subheader("📈 Skill Improvement Suggestions:")
                st.write(response)

            elif submit3:
                response = get_gemini_response(input_text, pdf_text, input_prompt3)
                st.subheader("🔑 Missing Keywords & Analysis:")
                st.write(response)
