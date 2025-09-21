from google.adk.agents.llm_agent import Agent
# from google.adk import Agent
from google.adk.tools import google_search  # The Google Search tool
import sys
sys.path.append("..")
from tripmate_agents.callback_logging import log_query_to_model, log_model_response
from . import prompt

search_agent = Agent(
    model='gemini-2.5-flash',
    name='google_search_agent',
    description='A helpful assistant for user questions.',
    instruction=prompt.search_agent_prompt,
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    tools=[google_search]
)
