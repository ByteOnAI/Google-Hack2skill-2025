import os
# import sys
import logging

# sys.path.append("../..")
from ...callback_logging import log_query_to_model, log_model_response
from dotenv import load_dotenv
import google.cloud.logging
from google.adk import Agent
from typing import Optional, List, Dict

from google.adk.tools.tool_context import ToolContext

from .prompt import travel_brainstormer_agent_prompt


load_dotenv()

cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

travel_brainstormer = Agent(
    name="travel_brainstormer",
    model=os.getenv("MODEL"),
    description="Assist the user in choosing a travel destination country.",
    instruction=travel_brainstormer_agent_prompt,
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
)
