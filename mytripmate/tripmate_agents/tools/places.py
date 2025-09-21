# tripmate_agents/tools/places.py
"""
Simplified Google Places tool for the itinerary_planner agent.

Provides:
- A single map_tool(key: str, tool_context: ToolContext) function that:
  - Looks at tool_context.state[key]["places"] (list of POI dicts).
  - For each POI, queries Google Places FindPlaceFromText with "place_name, address"
  - Fills place_id, map_url, lat, lng (as strings) on each POI when available.
  - Returns {"places": updated_list}
"""

import os
import logging
from typing import Dict, Any, List

import requests
from google.adk.tools.tool_context import ToolContext  # matches the import style used elsewhere
from .config import GOOGLE_PLACES_API_KEY
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


PLACES_FIND_URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
GOOGLE_PHOTO_BASE = "https://maps.googleapis.com/maps/api/place/photo"


def _find_place(query: str, api_key: str, timeout: int = 5) -> Dict[str, Any]:
    """Call Find Place From Text and return the first candidate dict or an error dict."""
    params = {
        "input": query,
        "inputtype": "textquery",
        # minimal fields needed: place_id, formatted_address, name, geometry
        "fields": "place_id,formatted_address,name,geometry",
        "key": api_key,
    }

    try:
        resp = requests.get(PLACES_FIND_URL, params=params, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        logger.warning("Places API request failed for query=%s: %s", query, e)
        return {"error": str(e)}

    candidates = data.get("candidates") or []
    if not candidates:
        return {"error": "no candidates"}
    return candidates[0]


def _build_map_url(place_id: str) -> str:
    return f"https://www.google.com/maps/place/?q=place_id:{place_id}"


def map_tool(key: str, tool_context: ToolContext) -> Dict[str, List[Dict[str, Any]]]:
    """
    Tool to enrich POIs stored under tool_context.state[key]["places"] with verified place
    metadata (place_id, map_url, lat, lng).

    Expected POI shape (incoming): list of dicts where each dict has at least:
      - "place_name" (or "name") and/or "address"
    After execution each POI will have (if found):
      - "place_id": str or None
      - "map_url": str or None
      - "lat": str or None
      - "lng": str or None

    Returns:
        {"places": updated_places_list}
    """
    try:
        api_key = GOOGLE_PLACES_API_KEY
    except ValueError as e:
        logger.error("Google Places API key missing: %s", e)
        # Nothing to do — return empty or existing places unchanged
        existing = tool_context.state.get(key, {}).get("places", [])
        return {"places": existing}

    # Ensure state structure exists
    if key not in tool_context.state:
        tool_context.state[key] = {}
    if "places" not in tool_context.state[key] or not isinstance(tool_context.state[key]["places"], list):
        tool_context.state[key]["places"] = []

    places: List[Dict[str, Any]] = tool_context.state[key]["places"]

    for idx, poi in enumerate(places):
        # Construct a sensible text query: prefer explicit place_name then fallback to 'name'
        name = poi.get("place_name") or poi.get("name") or ""
        address = poi.get("address") or poi.get("formatted_address") or ""
        if not name and not address:
            logger.info("POI at index %d missing name/address — skipping", idx)
            # leave poi unchanged
            continue

        query = ", ".join([part.strip() for part in (name, address) if part.strip()])
        if not query:
            logger.info("Empty composed query for POI index %d — skipping", idx)
            continue

        result = _find_place(query, api_key)
        if "error" in result:
            logger.info("No match for query '%s' (poi idx %d): %s", query, idx, result.get("error"))
            # Explicitly set None values so downstream code can check them
            poi.setdefault("place_id", None)
            poi.setdefault("map_url", None)
            poi.setdefault("lat", None)
            poi.setdefault("lng", None)
            continue

        # Pull values safely
        place_id = result.get("place_id")
        formatted_address = result.get("formatted_address")
        geometry = result.get("geometry", {})
        location = geometry.get("location", {}) or {}
        lat = location.get("lat")
        lng = location.get("lng")

        # Normalize/format coordinates as strings if present
        poi["place_id"] = place_id or None
        poi["map_url"] = _build_map_url(place_id) if place_id else None
        poi["lat"] = str(lat) if lat is not None else None
        poi["lng"] = str(lng) if lng is not None else None

        # Optionally update human-friendly fields if available
        if formatted_address and not poi.get("address"):
            poi["address"] = formatted_address
        if result.get("name") and not poi.get("place_name"):
            poi["place_name"] = result.get("name")

        logger.info("Updated POI idx %d: place_id=%s lat=%s lng=%s", idx, place_id, poi["lat"], poi["lng"])

    # Return the updated POIs — the Agent will receive this as the tool result.
    return {"places": places}
