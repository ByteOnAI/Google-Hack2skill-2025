"""Booking agent and sub-agents, handling the confirmation and payment of bookable events."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig
from .prompt import booking_orchestrator_prompt
from tripmate_agents.tools.bookings import (
    apply_coupon, apply_payment_offer, collect_payment, confirm_pin,
    book_flight, book_train, book_bus, book_hotel, generate_booking_confirmation
)
from tripmate_agents.tools.memory import save_to_file
from tripmate_agents.tools.config import MODEL

json_cfg = GenerateContentConfig(response_mime_type="application/json")

booking_orchestrator = Agent(
    model=MODEL,
    name="booking_orchestrator",
    description="Converts the finalized plan into EMT-style bookings (mocked).",
    instruction=booking_orchestrator_prompt,
    # Tools wired as callable functions
    tools=[
        apply_coupon,
        apply_payment_offer,
        collect_payment,
        confirm_pin,
        book_flight,
        book_train,
        book_bus,
        book_hotel,
        generate_booking_confirmation
    ],
    # You can keep text output for chat + store JSON to state
    generate_content_config=GenerateContentConfig(temperature=0.1, top_p=0.5),
    after_agent_callback=save_to_file,  # persists appended record with booking_confirmation in state
)
