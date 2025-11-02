"""Demonstration of MY-TRIP-MATE AI Agent using ADK"""

import os
import logging

from dotenv import load_dotenv
import google.cloud.logging
from google.adk import Agent
from google.genai import types
from typing import Optional, List, Dict

from google.adk.tools.tool_context import ToolContext

from tripmate_agents import prompt

# from tripmate_agents.sub_agents.booking.agent import booking_agent
from tripmate_agents.sub_agents.in_trip.agent import in_trip_agent
# from tripmate_agents.sub_agents.inspiration.agent import inspiration_agent
# from tripmate_agents.sub_agents.planning.agent import planning_agent
from tripmate_agents.sub_agents.post_trip.agent import post_trip_agent
from tripmate_agents.sub_agents.pre_trip.agent import pre_trip_agent
from .sub_agents.brainstormer_agent.agent import travel_brainstormer
from .sub_agents.itinerary_agent.agent import itinerary_planner


from tripmate_agents.tools.memory import load_user, save_to_file
from tripmate_agents.tools.config import MODEL


cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()
print("MODEL: ", MODEL)

my_trip_mate_agent = Agent(
    model=MODEL,
    name="my_trip_mate_agent",
    description="Start a user on a Trip Planning.",
    instruction=prompt.my_trip_mate_agent_prompt,
    generate_content_config=types.GenerateContentConfig(temperature=0.2,),
    sub_agents=[
        travel_brainstormer,
        itinerary_planner,
        pre_trip_agent,
        in_trip_agent,
        post_trip_agent,
    ],
    before_agent_callback=load_user,
    # after_agent_callback=save_to_file,
)
root_agent = my_trip_mate_agent

if __name__ == "__main__":
    root_agent.run()
