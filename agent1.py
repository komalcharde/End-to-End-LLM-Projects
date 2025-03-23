from crewai import Agent
from tools import yt_tool
from crewai import OpenAIGPT

llm = OpenAIGPT(model_name="gpt-4-0125-preview")
from dotenv import load_dotenv
load_dotenv()
import os
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"]="gpt-4-0125-preview"
blog_researcher=Agent(
  role='Blog Researcher from Youtube Videos',
  goal='get the relevet content for the topic{topic} from yt channel',
  verbose=True,
  memory=True,
  backstory=(
      "Expert in uderstanding videos in AI Data Science, machine learning and GEN AI and providing suggession"
  ),
  tools=[],
  llm=llm,
  allow_delegation=True
)


blog_writer=Agent(
   
  role='Writer',
  goal='Narrate compelling tech stories about the video {topic} from yt channel',
  verbose=True,
  memory=True,
  backstory=(
      "With a flair for simplifying complex topics, you credit"
      "engaging narratives that cpacitive and educate, bringging new"
      "discoveries to light ina am accessible manner"
  ),
  tools=[],
  llm=llm,
  allow_delegation=False

)