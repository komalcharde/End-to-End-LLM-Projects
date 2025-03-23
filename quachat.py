from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API Key is missing. Check your .env file.")
else:
    genai.configure(api_key=api_key)

# Load AI Model (Check if Available)
try:
    model = genai.GenerativeModel("gemini-1.5-pro")  # Change if needed
    chat = model.start_chat(history=[])
except Exception as e:
    st.error(f"Error loading model: {e}")

# Function to Get AI Response
def get_gemini_response(question):
    try:
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        return f"Error: {e}"

# Streamlit Web UI
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

# Initialize Chat History
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# User Input
input_text = st.text_input("Input:", key="input")
submit = st.button("Ask the question")

if submit and input_text:
    response = get_gemini_response(input_text)
    st.session_state["chat_history"].append(("You", input_text))
    
    st.subheader("The Response is")
    
    if isinstance(response, str):  # Handle API errors
        st.write(response)
    else:
        for chunk in response:
            st.write(chunk.text)
            st.session_state["chat_history"].append(("Bot", chunk.text))

# Display Chat History
st.subheader("Chat History")
for role, text in st.session_state["chat_history"]:
    st.write(f"**{role}:** {text}")
