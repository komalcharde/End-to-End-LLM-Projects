from dotenv import load_dotenv
import os
from crewai_tools import SerperDevTool

# Load environment variables
load_dotenv()

# Verify the API key is loaded (optional debug)
if not os.getenv("SERPER_API_KEY"):
    raise ValueError("SERPER_API_KEY not found! Check your .env file.")

# Initialize the SerperDevTool with the API key
tool = SerperDevTool()
