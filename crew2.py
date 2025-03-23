from crewai import Crew, Process
from task2 import research_task, write_task  # ✅ Ensure task2.py exists and is correct
from agents2 import researcher, writer  # ✅ Ensure agents2.py exists

# Forming the tech-focused crew with some enhanced configurations
crew = Crew(
  agents=[researcher, writer],
  tasks=[research_task, write_task],
  process=Process.sequential,  # Optional: Sequential task execution is default
  memory=True,
  cache=True,
  max_rpm=20,
  share_crew=True
)

# Starting the task execution process with enhanced feedback
result = crew.kickoff(inputs={'topic': 'AI in blogging'})
print(result)
