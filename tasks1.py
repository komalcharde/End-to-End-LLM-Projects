from crewai import Task
from tools import yt_tool
from agents import blog_researcher,blog_writer
research_task=Task(
    description=(
        "Identity the video {topic}"
        "Get detailed information about the video from the channel"
    ),
    expected_output='A comprehensive 3 paragraphs long report based on the {topic} of video of video content',
    tools=[yt_tool],
    agent=blog_researcher,

)
write_task=Task(
    description=(
        "get the info from the youtube channel on the topic {topic}"
    ),
    expected_output='Summarize the info from the youtube chnnel video on the topic{topic} and create the content on the blog',
    tools=[yt_tool],
    agent=blog_writer,
    async_execution=False,
    output_file='new-blog-post.md'
)