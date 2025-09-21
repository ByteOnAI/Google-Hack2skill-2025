"""Safety agent and sub-agents, handling the safety measures of the trip."""

from google.adk.agents.llm_agent import Agent
from google.adk.tools.agent_tool import AgentTool
from tripmate_agents.tools.config import GOOGLE_MAPS_API_KEY, MODEL
from tripmate_agents.callback_logging import log_query_to_model, log_model_response
from tripmate_agents.sub_agents.google_search_agent.agent import search_agent
from . import prompt


weather_agent = Agent(
    name="weather_agent",
    model=MODEL, # Can be a string for Gemini or a LiteLlm object
    description="Provides weather information for specific cities.",
    instruction=prompt.weather_agent_prompt,
    tools=[
        AgentTool(agent=search_agent),
        ], # Pass the function directly
)

