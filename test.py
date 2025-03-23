from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Check API Key
if not api_key:
    st.error("API Key is missing. Please check your .env file.")
else:
    genai.configure(api_key=api_key)

# Initialize Gemini Vision Model
try:
    model = genai.GenerativeModel("gemini-1.5-pro")
except Exception as e:
    st.error(f"Failed to load Gemini model: {e}")

# Function to get the response from the Gemini model
def get_gemini_response(image_data, prompt):
    try:
        if not image_data:
            raise ValueError("Image data is empty")
        response = model.generate_content([prompt, image_data])  # Ensure correct input format
        return response.text
    except Exception as e:
        st.error(f"An error occurred while generating content: {e}")
        return None

# Function to process the uploaded image
def input_image_details(uploaded_file):
    try:
        if uploaded_file is not None:
            image = Image.open(uploaded_file)  # Open the image
            return image  # Return as PIL Image (if API supports it)
        else:
            raise FileNotFoundError("No file uploaded")
    except Exception as e:
        st.error(f"An error occurred while processing the uploaded file: {e}")
        return None

# Streamlit UI
st.set_page_config(page_title="Multilanguage Invoice Extractor")
st.header("📄 Gemini Invoice Processing")

# User Input
user_input = st.text_area("Ask something about the invoice:", key="input")
uploaded_file = st.file_uploader("📂 Upload an invoice image...", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="🖼 Uploaded Invoice", use_column_width=True)

# Default instruction for AI
input_prompt = """
You are an expert in understanding invoices. 
We will upload an image as an invoice, and you will have to answer any questions based on the uploaded invoice image.
"""

# Submit Button
if st.button("🔍 Analyze Invoice"):
    if uploaded_file is not None and user_input:
        try:
            image_data = input_image_details(uploaded_file)  # Process Image
            full_prompt = input_prompt + f"\nUser Query: {user_input}"  # Combine User Input
            response = get_gemini_response(image_data, full_prompt)  # Get AI Response
            if response:
                st.subheader("💡 Response:")
                st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("⚠️ Please upload an image and enter a question!")
