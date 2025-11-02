"""
FastAPI REST API for MyTripMate AI Agent
Provides endpoints to interact with the trip planning agent from frontend applications.
"""

import os
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field
import uvicorn

from dotenv import load_dotenv
from google.adk.sessions import InMemoryChatSession

# Import the root agent
from tripmate_agents.agent import root_agent

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="MyTripMate API",
    description="AI-powered trip planning and travel assistance API",
    version="1.0.0"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory session storage (consider Redis for production)
sessions: Dict[str, InMemoryChatSession] = {}


# ==================== Pydantic Models ====================

class UserProfile(BaseModel):
    """User profile information"""
    user_id: str = Field(..., description="Unique user identifier")
    first_name: str = Field(..., description="User's first name")
    last_name: Optional[str] = Field(None, description="User's last name")
    email: Optional[str] = Field(None, description="User's email")
    phone: Optional[str] = Field(None, description="User's phone number")
    country_of_residence: str = Field(default="India", description="User's country")
    timezone: str = Field(default="Asia/Kolkata", description="User's timezone")
    preferred_currency: str = Field(default="INR", description="Preferred currency")
    languages: List[str] = Field(default=["English"], description="Preferred languages")


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., description="User's message to the agent")
    user_id: str = Field(..., description="User ID for session management")
    session_id: Optional[str] = Field(None, description="Session ID to continue conversation")
    user_profile: Optional[UserProfile] = Field(None, description="User profile (optional)")


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str = Field(..., description="Agent's response")
    session_id: str = Field(..., description="Session ID for continuing conversation")
    user_id: str = Field(..., description="User ID")
    timestamp: str = Field(..., description="Response timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ItineraryRequest(BaseModel):
    """Request model for creating itinerary"""
    destination: str = Field(..., description="Destination city/country")
    start_date: str = Field(..., description="Trip start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="Trip end date (YYYY-MM-DD)")
    travelers: int = Field(default=1, description="Number of travelers")
    budget: Optional[str] = Field(None, description="Budget range")
    interests: Optional[List[str]] = Field(None, description="User interests")
    user_id: str = Field(..., description="User ID")
    user_profile: Optional[UserProfile] = Field(None, description="User profile")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    version: str


# ==================== Helper Functions ====================

def get_or_create_session(session_id: Optional[str], user_id: str) -> tuple[InMemoryChatSession, str]:
    """Get existing session or create new one"""
    if session_id and session_id in sessions:
        return sessions[session_id], session_id
    
    # Create new session
    new_session_id = f"{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    new_session = InMemoryChatSession()
    sessions[new_session_id] = new_session
    
    logger.info(f"Created new session: {new_session_id}")
    return new_session, new_session_id


def load_user_profile(user_id: str, custom_profile: Optional[UserProfile] = None) -> Dict[str, Any]:
    """Load user profile from file or use provided profile"""
    
    if custom_profile:
        # Use provided profile
        return {
            "user_profile": custom_profile.model_dump()
        }
    
    # Try to load from file
    profile_path = Path(f"tripmate_agents/profiles/{user_id}.json")
    
    if profile_path.exists():
        try:
            with open(profile_path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading profile for {user_id}: {e}")
    
    # Default profile
    return {
        "user_profile": {
            "user_id": user_id,
            "first_name": "User",
            "last_name": "",
            "email": "",
            "phone": "",
            "country_of_residence": "India",
            "timezone": "Asia/Kolkata",
            "preferred_currency": "INR",
            "languages": ["English"]
        }
    }


def save_user_profile(user_id: str, profile_data: Dict[str, Any]):
    """Save user profile to file"""
    profiles_dir = Path("tripmate_agents/profiles")
    profiles_dir.mkdir(parents=True, exist_ok=True)
    
    profile_path = profiles_dir / f"{user_id}.json"
    
    try:
        with open(profile_path, "w") as f:
            json.dump(profile_data, f, indent=2)
        logger.info(f"Saved profile for user: {user_id}")
    except Exception as e:
        logger.error(f"Error saving profile for {user_id}: {e}")


def get_itinerary_for_user(user_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve saved itinerary for a user"""
    itinerary_path = Path(f"tripmate_agents/itinerary/{user_id}.json")
    
    if itinerary_path.exists():
        try:
            with open(itinerary_path, "r") as f:
                data = json.load(f)
                # Return the most recent itinerary if it's a list
                if isinstance(data, list) and len(data) > 0:
                    return data[-1]
                return data
        except Exception as e:
            logger.error(f"Error loading itinerary for {user_id}: {e}")
    
    return None


# ==================== API Endpoints ====================

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - Health check"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint for conversing with the AI agent
    
    Example request:
    {
        "message": "Plan a 5-day trip to Tokyo",
        "user_id": "user_001",
        "session_id": null,
        "user_profile": {...}
    }
    """
    try:
        # Get or create session
        session, session_id = get_or_create_session(request.session_id, request.user_id)
        
        # Load user profile
        profile_data = load_user_profile(request.user_id, request.user_profile)
        
        # Update session state with user profile and current time
        session.state.update(profile_data)
        session.state["_time"] = datetime.now().isoformat()
        session.state["user_id"] = request.user_id
        
        logger.info(f"Processing chat for user {request.user_id}: {request.message}")
        
        # Send message to agent
        response = root_agent.run(
            message=request.message,
            session=session
        )
        
        # Extract response text
        response_text = ""
        if hasattr(response, 'content'):
            if isinstance(response.content, str):
                response_text = response.content
            elif isinstance(response.content, list):
                response_text = "\n".join([str(c) for c in response.content])
        else:
            response_text = str(response)
        
        # Get any saved itinerary
        itinerary = get_itinerary_for_user(request.user_id)
        
        return ChatResponse(
            response=response_text,
            session_id=session_id,
            user_id=request.user_id,
            timestamp=datetime.now().isoformat(),
            metadata={
                "has_itinerary": itinerary is not None,
                "session_messages": len(session.history) if hasattr(session, 'history') else 0
            }
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.post("/api/itinerary/create")
async def create_itinerary(request: ItineraryRequest):
    """
    Create a detailed itinerary based on structured parameters
    
    Example request:
    {
        "destination": "Tokyo, Japan",
        "start_date": "2025-12-01",
        "end_date": "2025-12-07",
        "travelers": 2,
        "budget": "moderate",
        "interests": ["technology", "food", "culture"],
        "user_id": "user_001"
    }
    """
    try:
        # Create session
        session = InMemoryChatSession()
        
        # Load user profile
        profile_data = load_user_profile(request.user_id, request.user_profile)
        
        # Setup session state
        session.state.update(profile_data)
        session.state["_time"] = datetime.now().isoformat()
        session.state["user_id"] = request.user_id
        
        # Construct message for itinerary creation
        interests_str = ", ".join(request.interests) if request.interests else "general sightseeing"
        budget_str = f" with a {request.budget} budget" if request.budget else ""
        
        message = (
            f"Create a detailed itinerary for {request.travelers} person(s) "
            f"traveling to {request.destination} from {request.start_date} to {request.end_date}. "
            f"The traveler(s) are interested in {interests_str}{budget_str}."
        )
        
        logger.info(f"Creating itinerary for user {request.user_id}: {message}")
        
        # Send to agent
        response = root_agent.run(
            message=message,
            session=session
        )
        
        # Extract response
        response_text = ""
        if hasattr(response, 'content'):
            if isinstance(response.content, str):
                response_text = response.content
            elif isinstance(response.content, list):
                response_text = "\n".join([str(c) for c in response.content])
        else:
            response_text = str(response)
        
        # Try to get the saved itinerary
        itinerary_data = get_itinerary_for_user(request.user_id)
        
        return JSONResponse(content={
            "success": True,
            "message": "Itinerary created successfully",
            "response": response_text,
            "itinerary": itinerary_data,
            "user_id": request.user_id,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error creating itinerary: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error creating itinerary: {str(e)}")


@app.get("/api/itinerary/{user_id}")
async def get_itinerary(user_id: str):
    """Get saved itinerary for a user"""
    try:
        itinerary = get_itinerary_for_user(user_id)
        
        if itinerary:
            return JSONResponse(content={
                "success": True,
                "itinerary": itinerary,
                "user_id": user_id
            })
        else:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "message": "No itinerary found for this user"
                }
            )
    except Exception as e:
        logger.error(f"Error retrieving itinerary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/user/profile")
async def create_or_update_profile(profile: UserProfile):
    """Create or update user profile"""
    try:
        profile_data = {
            "user_profile": profile.model_dump()
        }
        save_user_profile(profile.user_id, profile_data)
        
        return JSONResponse(content={
            "success": True,
            "message": "Profile saved successfully",
            "user_id": profile.user_id
        })
    except Exception as e:
        logger.error(f"Error saving profile: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/user/profile/{user_id}")
async def get_profile(user_id: str):
    """Get user profile"""
    try:
        profile_data = load_user_profile(user_id)
        
        return JSONResponse(content={
            "success": True,
            "profile": profile_data.get("user_profile"),
            "user_id": user_id
        })
    except Exception as e:
        logger.error(f"Error retrieving profile: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a chat session"""
    if session_id in sessions:
        del sessions[session_id]
        return JSONResponse(content={
            "success": True,
            "message": "Session deleted successfully"
        })
    else:
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": "Session not found"
            }
        )


@app.get("/api/sessions")
async def list_sessions():
    """List all active sessions (for debugging)"""
    return JSONResponse(content={
        "active_sessions": list(sessions.keys()),
        "count": len(sessions)
    })


# ==================== Server Entry Point ====================

if __name__ == "__main__":
    port = int(os.getenv("API_PORT", "8000"))
    host = os.getenv("API_HOST", "0.0.0.0")
    
    logger.info(f"Starting MyTripMate API server on {host}:{port}")
    
    uvicorn.run(
        "api:app",
        host=host,
        port=port,
        reload=True,  # Enable auto-reload during development
        log_level="info"
    )
