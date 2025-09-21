import logging

from google.adk.agents.llm_agent import LlmAgent
import google.cloud.logging
from typing import Optional, List, Dict

from google.adk.tools.tool_context import ToolContext
from google.adk.tools.agent_tool import AgentTool

from tripmate_agents.callback_logging import log_query_to_model, log_model_response

from .prompt import itinerary_planner_prompt
# from tripmate_agents.tools.places import map_tool
from tripmate_agents.sub_agents.planing_agent.agent import planing_agent
from tripmate_agents.sub_agents.safety_check_agent.agent import weather_agent
from tripmate_agents.tools.config import MODEL
from tripmate_agents.tools.memory import save_to_state
from tripmate_agents.sub_agents.google_search_agent.agent import search_agent
# from tripmate_agents.shared_libraries.itinerary_model import ItinerarySaveSchema


cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

itinerary_planner = LlmAgent(
    name="itinerary_planner",
    model=MODEL,
    description="Build a list of attractions to visit in a country.",
    instruction=itinerary_planner_prompt,
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    # When instructed to do so, paste the tools parameter below this line
    sub_agents=[planing_agent],
    tools=[
        AgentTool(agent=weather_agent),
        AgentTool(agent=search_agent),
        # map_tool, 
        save_to_state,
    ],
)
