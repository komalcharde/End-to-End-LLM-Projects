import streamlit as st
import sqlite3
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Generative AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Google API Key is missing! Please set it in your .env file.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# Function to get SQL query from Gemini AI
def get_gemini_response(question, prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")  # Updated model
        response = model.generate_content(f"{prompt}\n{question}")

        if response.text:
            sql_query = response.text.strip()
            sql_query = sql_query.split("\n")[-1]  # Take last line (assuming SQL is at the end)
            return sql_query
        else:
            return None
    except Exception as e:
        st.error(f"Error generating Gemini response: {e}")
        return None

# Function to execute SQL query on the database
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        # Debugging: Print SQL before execution
        print("Executing SQL Query:", sql)

        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()

        if not rows:
            return ["⚠️ No matching records found! Check your input."]
        return rows

    except sqlite3.Error as e:
        return [f"❌ SQL Error: {e}"]

# Define Gemini prompt for SQL generation
prompt = """You are an AI assistant trained to convert natural language questions into SQL queries.
The database is named STUDENT and contains the following columns: NAME, CLASS, SECTION, MARKS.

### Example Queries:
1. **Question:** How many students are in the database?
   **SQL:** SELECT COUNT(*) FROM STUDENT;

2. **Question:** List students in the 'Data Science' class.
   **SQL:** SELECT * FROM STUDENT WHERE CLASS='Data Science' COLLATE NOCASE;

Provide only the SQL query in your response.
"""

# Streamlit UI setup
st.set_page_config(page_title="Gemini SQL Query Generator")
st.header("Gemini AI - SQL Query Generator")

# User input
question = st.text_input("Enter your question:", key="input")

# Generate button
if st.button("Generate SQL and Query Database"):
    if not question:
        st.warning("Please enter a question!")
    else:
        # Generate SQL query
        sql_query = get_gemini_response(question, prompt)

        if sql_query:
            st.subheader("Generated SQL Query:")
            st.code(sql_query, language="sql")
            print("Generated SQL Query:", sql_query)  # Debugging

            # Execute SQL query in the SQLite database
            query_results = read_sql_query(sql_query, "student.db")

            if query_results:
                st.subheader("Query Results:")
                for row in query_results:
                    st.write(row)
            else:
                st.warning("No data returned from the database.")
