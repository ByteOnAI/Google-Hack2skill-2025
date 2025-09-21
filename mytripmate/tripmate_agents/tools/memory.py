from datetime import datetime
import json
import os
import re
from typing import Dict, Any, List

from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions.state import State
from google.adk.tools import ToolContext

# from travel_concierge.shared_libraries import constants

user_profile_path = os.getenv(
    "user_profile_path", "tripmate_agents/profiles/user_0001.json"
)

SYSTEM_TIME = "_time"
ITIN_INITIALIZED = "_itin_initialized"

USER_ID = "user_id"


import json
from typing import Any

def _safe_parse_json_str(maybe_json: Any) -> Any:
    """If value is a JSON-encoded string, parse to dict; otherwise return as-is."""
    if isinstance(maybe_json, str):
        s = maybe_json.strip()
        # Quick sanity: looks like JSON object/array
        if (s.startswith("{") and s.endswith("}")) or (s.startswith("[") and s.endswith("]")):
            try:
                return json.loads(s)
            except Exception:
                return maybe_json  # leave as-is if it fails
    return maybe_json

def _next_itin_id(existing: List[Dict[str, Any]]) -> str:
    """Find max itin_XXXX in existing list and return next one."""
    max_num = 0
    pat = re.compile(r"^itin_(\d{4})$")
    for item in existing:
        itid = item.get("iten_id") or item.get("itinerary_id")
        if isinstance(itid, str):
            m = pat.match(itid)
            if m:
                try:
                    n = int(m.group(1))
                    max_num = max(max_num, n)
                except Exception:
                    pass
    return f"itin_{(max_num + 1):04d}"

def save_to_file(callback_context: "CallbackContext") -> dict:
    """
    Append the current itinerary/trip plan snapshot to a per-user JSON file.
    - File content is ALWAYS a JSON array.
    - Each element has: _time, _itin_initialized, iten_id, itinerary, trip_plan, user_id
    - 'user_profile' is NOT saved.
    - itinerary/trip_plan are stored as parsed JSON objects when possible (pretty, unescaped).
    """
    state = callback_context.state

    # Resolve user_id from state (prefer explicit 'user_id', else from 'user_profile.user_id')
    user_id = state.get("user_id")
    if not user_id and "user_profile" in state and isinstance(state["user_profile"], dict):
        user_id = state["user_profile"].get("user_id")

    if not user_id:
        return {"status": "error", "error": "missing user_id; cannot determine filename"}

    # Prepare output directory and file path
    out_dir = "tripmate_agents/itinerary"
    os.makedirs(out_dir, exist_ok=True)
    file_path = os.path.join(out_dir, f"{user_id}.json")

    # Load existing list (or start new)
    existing: List[Dict[str, Any]] = []
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                existing = data
            elif isinstance(data, dict):
                # If previous version wrote a dict, wrap it to preserve history
                existing = [data]
            else:
                existing = []
        except Exception:
            # Corrupt or unreadable -> start fresh list
            existing = []

    # Build the new record
    itinerary_raw = state.get("itinerary")
    trip_plan_raw = state.get("trip_plan")

    record = {
        "_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        "_itin_initialized": bool(state.get(ITIN_INITIALIZED, True)),
        "iten_id": _next_itin_id(existing),
        "itinerary": _safe_parse_json_str(itinerary_raw),
        "trip_plan": _safe_parse_json_str(trip_plan_raw),
        "user_id": user_id,
    }

    # Append and write (pretty/beautified, unescaped, no user_profile)
    existing.append(record)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
    except Exception as exc:
        return {"status": "error", "error": f"failed to write file: {exc}"}

    return None

def save_to_state(key: str, value: str, tool_context: ToolContext):
    """
    Save information pieces into state, one key-value pair at a time.
    """
    mem_dict = tool_context.state
    mem_dict[key] = value
    return {"status": f'Stored "{key}": "{value}"'}



def _set_user_states(source: Dict[str, Any], target: State | dict[str, Any]):
    """
    Setting the initial session state given a JSON object of states.

    Args:
        source: A JSON object of states.
        target: The session state object to insert into.
    """
    if SYSTEM_TIME not in target:
        target[SYSTEM_TIME] = str(datetime.now())

    if ITIN_INITIALIZED not in target:
        target[ITIN_INITIALIZED] = True

        target.update(source)

def load_user(callback_context: CallbackContext):
    """
    Sets up the initial state.
    Set this as a callback as before_agent_call of the root_agent.
    This gets called before the system instruction is contructed.

    Args:
        callback_context: The callback context.
    """    
    data = {}
    with open(user_profile_path, "r") as file:
        data = json.load(file)
        print(f"\nLoading Initial State: {data}\n")

    _set_user_states(data, callback_context.state)