"""Planning agent. A pre-booking agent covering the planning part of the trip."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig
from . import prompt
from tripmate_agents.tools.config import MODEL
from tripmate_agents.sub_agents.google_search_agent.agent import search_agent
from tripmate_agents.tools.memory import save_to_state, save_to_file
from tripmate_agents.sub_agents.booking_agent.agent import booking_orchestrator


json_response_config = GenerateContentConfig(
    response_mime_type="application/json"
)


hotel_room_selection_agent = Agent(
    model=MODEL,
    name="hotel_room_selection_agent",
    description="Help users with the room choices for a hotel",
    instruction=prompt.HOTEL_ROOM_SELECTION_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    generate_content_config=json_response_config,
    # tools = [AgentTool(agent=search_agent)]
)

hotel_search_agent = Agent(
    model=MODEL,
    name="hotel_search_agent",
    description="Help users find hotel around a specific geographic area",
    instruction=prompt.HOTEL_SEARCH_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    generate_content_config=json_response_config,
    # tools = [AgentTool(agent=search_agent)]
)

flight_seat_selection_agent = Agent(
    model=MODEL,
    name="flight_seat_selection_agent",
    description="Help users with the seat choices",
    instruction=prompt.FLIGHT_SEAT_SELECTION_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    generate_content_config=json_response_config,
)

flight_search_agent = Agent(
    model=MODEL,
    name="flight_search_agent",
    description="Help users find best flight deals",
    instruction=prompt.FLIGHT_SEARCH_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    generate_content_config=json_response_config,
    # tools = [AgentTool(agent=search_agent)]
)

train_search_agent = Agent(
    model=MODEL,
    name="train_search_agent",
    description="Help users find the best train options within budget and timing constraints",
    instruction=prompt.TRAIN_SEARCH_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    generate_content_config=json_response_config,
    # tools = [AgentTool(agent=search_agent)]
)

train_seat_selection_agent = Agent(
    model=MODEL,
    name="train_seat_selection_agent",
    description="Help users choose train class/berth and seats based on preference",
    instruction=prompt.TRAIN_SEAT_SELECTION_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    generate_content_config=json_response_config,
)

bus_search_agent = Agent(
    model=MODEL,
    name="bus_search_agent",
    description="Help users find the best intercity bus options within budget and timing constraints",
    instruction=prompt.BUS_SEARCH_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    generate_content_config=json_response_config,
    # tools = [AgentTool(agent=search_agent)]
)

bus_seat_selection_agent = Agent(
    model=MODEL,
    name="bus_seat_selection_agent",
    description="Help users pick bus seat/berth and AC/non-AC based on preference",
    instruction=prompt.BUS_SEAT_SELECTION_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    generate_content_config=json_response_config,
)

ship_search_agent = Agent(
    model=MODEL,
    name="ship_search_agent",
    description="Help users find ship/ferry routes when a water connection is available, respecting budget & schedule",
    instruction=prompt.SHIP_SEARCH_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    generate_content_config=json_response_config,
)

ship_cabin_selection_agent = Agent(
    model=MODEL,
    name="ship_cabin_selection_agent",
    description="Help users pick ship/ferry cabin/class",
    instruction=prompt.SHIP_CABIN_SELECTION_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    generate_content_config=json_response_config,
)

# --- Orchestrator: Planning Agent ---
planing_agent = Agent(
    model=MODEL,
    name="planning_agent",
    description=(
        "Helps users with travel planning, completing a full itinerary for their vacation. "
        "Supports flights, trains, buses, and ships. Finds best deals, filters by budget, "
        "confirms preferred mode, gathers seat/cabin choices, then hotel, and produces a final itinerary."
    ),
    instruction=prompt.PLANNING_AGENT_INSTR,
    tools=[
        # Transport discovery (all modes)
        AgentTool(agent=flight_search_agent),
        AgentTool(agent=train_search_agent),
        AgentTool(agent=bus_search_agent),
        AgentTool(agent=ship_search_agent),

        # Seat/cabin selection per mode
        AgentTool(agent=flight_seat_selection_agent),
        AgentTool(agent=train_seat_selection_agent),
        AgentTool(agent=bus_seat_selection_agent),
        AgentTool(agent=ship_cabin_selection_agent),

        # Stay 
        AgentTool(agent=hotel_search_agent),
        AgentTool(agent=hotel_room_selection_agent),

        AgentTool(agent=search_agent),
        
        # Memory tool
        save_to_state,
    ],
    sub_agents=[booking_orchestrator],
    generate_content_config=GenerateContentConfig(temperature=0.1, top_p=0.5),
    after_agent_callback=save_to_file,
)