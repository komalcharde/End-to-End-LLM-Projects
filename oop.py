import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
prompt="""you are Youtube video summairizer.You will be taking the transcript text and summerizing the entire video and providing the important summary in points within 250 word.
Please get the summary here:"""
def extract_transcript_deatils(youtube_video_url):
     try:
          video_id=youtube_video_url.split("=")[1]
          print(video_id)
          transcript_text=YouTubeTranscriptApi.get_transcript(video_id)
          transcript =" "
          for i in transcript_text:
              transcript+=""+i["text"]
              return transcript

     except Exception as e:
          raise e
def generate_gemini_content(transcript_text,prompt):
     model=genai.GenerativeModel("gemini-1.5-pro")
     response=model.generate_content(prompt+transcript_text)
     return response.text
st.title("Youtube Transcript to Detailed Notes Connerter")

youtube_link=st.text_input("ENter youtube video link:")
if youtube_link:
     video_id=youtube_link.split("=")[1]
     print(video_id)
     st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)
if st.button("Get Detailed Notes"):
     transcript_text=extract_transcript_deatils(youtube_link)
     if transcript_text:
          summary=generate_gemini_content(transcript_text,prompt)
          st.markdown("##Deatiled Notes:")
          st.write(summary)
