import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Generative AI with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image):
    """
    Generates a response using Gemini 1.5 Flash model.

    Args:
        input_prompt (str): The input prompt for the model.
        image (list): A list containing image data.
    Returns:
        str: The response text from the model.
    """
    try:
        # Use the updated Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([input_prompt, image[0]])
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {e}")
        raise e

def input_image_setup(uploaded_file):
    """
    Prepares the uploaded image for processing.

    Args:
        uploaded_file: The uploaded image file.

    Returns:
        list: A list containing the image parts with MIME type and data.
    """
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit app setup
st.set_page_config(page_title="Calories Advisor App")
st.header("Gemini Health App")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Input prompt for the model
input_prompt = """
You are an expert nutritionist. Analyze the food items from the image, calculate the total calories, and provide details of each item:
1. Item 1 - Number of calories
2. Item 2 - Number of calories
---
Additionally:
- Mention whether the food is healthy or not.
- Provide the percentage split of carbohydrates, fats, fibers, sugars, and essential nutrients.
"""

# Submit button
submit = st.button("Tell me about the total calories")

if submit:
    if uploaded_file is None:
        st.error("Please upload an image before submitting.")
    else:
        try:
            # Prepare the image and get the response
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data)
            st.header("Response")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
