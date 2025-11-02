# MyTripMate API Documentation

## Overview

This API provides endpoints to interact with the MyTripMate AI agent for trip planning, itinerary generation, and travel assistance. The API is built with FastAPI and supports RESTful interactions.

## Base URL

```
http://localhost:8000
```

## Getting Started

### 1. Installation

Install the required dependencies:

```bash
cd mytripmate
pip install -r requirements.txt
```

### 2. Configuration

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` with your API keys and configuration:

```env
GOOGLE_PROJECT_ID=your-gcp-project-id
GOOGLE_LOCATION=us-central1
MODEL=gemini-2.0-flash-exp
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
API_PORT=8000
```

### 3. Start the API Server

```bash
python api.py
```

Or using uvicorn directly:

```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### 4. Interactive Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## API Endpoints

### Health Check

#### `GET /`
Check if the API is running

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-02T22:30:00.000Z",
  "version": "1.0.0"
}
```

#### `GET /health`
Health check endpoint (same as root)

---

### Chat Endpoints

#### `POST /api/chat`
Send a message to the AI agent and get a response

**Request Body:**
```json
{
  "message": "Plan a 5-day trip to Tokyo",
  "user_id": "user_001",
  "session_id": null,
  "user_profile": {
    "user_id": "user_001",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "country_of_residence": "India",
    "timezone": "Asia/Kolkata",
    "preferred_currency": "INR",
    "languages": ["English", "Hindi"]
  }
}
```

**Response:**
```json
{
  "response": "Hi John — I'd be happy to help plan your 5-day trip to Tokyo! To create the best itinerary...",
  "session_id": "user_001_20251102223000",
  "user_id": "user_001",
  "timestamp": "2025-11-02T22:30:00.000Z",
  "metadata": {
    "has_itinerary": false,
    "session_messages": 1
  }
}
```

**Fields:**
- `message` (required): User's message to the agent
- `user_id` (required): Unique user identifier
- `session_id` (optional): Session ID to continue an existing conversation
- `user_profile` (optional): User profile information (if not provided, will load from file or use default)

**Conversation Example:**

First message (starting a new session):
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want to plan a trip to Paris",
    "user_id": "user_001"
  }'
```

Continue conversation (using session_id from previous response):
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want to go for 7 days in December",
    "user_id": "user_001",
    "session_id": "user_001_20251102223000"
  }'
```

---

### Itinerary Endpoints

#### `POST /api/itinerary/create`
Create a detailed itinerary with structured parameters

**Request Body:**
```json
{
  "destination": "Tokyo, Japan",
  "start_date": "2025-12-01",
  "end_date": "2025-12-07",
  "travelers": 2,
  "budget": "moderate",
  "interests": ["technology", "food", "culture"],
  "user_id": "user_001",
  "user_profile": {
    "user_id": "user_001",
    "first_name": "John",
    "preferred_currency": "INR"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Itinerary created successfully",
  "response": "Here's your detailed 7-day itinerary for Tokyo...",
  "itinerary": {
    "_time": "2025-11-02 22:30:00.123456",
    "iten_id": "itin_0001",
    "itinerary": {
      "destination": "Tokyo, Japan",
      "days": [...]
    },
    "user_id": "user_001"
  },
  "user_id": "user_001",
  "timestamp": "2025-11-02T22:30:00.000Z"
}
```

**Fields:**
- `destination` (required): Destination city/country
- `start_date` (required): Trip start date (YYYY-MM-DD format)
- `end_date` (required): Trip end date (YYYY-MM-DD format)
- `travelers` (optional): Number of travelers (default: 1)
- `budget` (optional): Budget range (e.g., "low", "moderate", "luxury")
- `interests` (optional): List of user interests
- `user_id` (required): User identifier
- `user_profile` (optional): User profile

#### `GET /api/itinerary/{user_id}`
Get the most recent saved itinerary for a user

**Response:**
```json
{
  "success": true,
  "itinerary": {
    "_time": "2025-11-02 22:30:00.123456",
    "iten_id": "itin_0001",
    "itinerary": {...},
    "trip_plan": {...},
    "user_id": "user_001"
  },
  "user_id": "user_001"
}
```

**404 Response (no itinerary found):**
```json
{
  "success": false,
  "message": "No itinerary found for this user"
}
```

---

### User Profile Endpoints

#### `POST /api/user/profile`
Create or update a user profile

**Request Body:**
```json
{
  "user_id": "user_001",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "+91-9000000000",
  "country_of_residence": "India",
  "timezone": "Asia/Kolkata",
  "preferred_currency": "INR",
  "languages": ["English", "Hindi"]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Profile saved successfully",
  "user_id": "user_001"
}
```

#### `GET /api/user/profile/{user_id}`
Get user profile

**Response:**
```json
{
  "success": true,
  "profile": {
    "user_id": "user_001",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "country_of_residence": "India",
    "timezone": "Asia/Kolkata",
    "preferred_currency": "INR",
    "languages": ["English", "Hindi"]
  },
  "user_id": "user_001"
}
```

---

### Session Management

#### `DELETE /api/session/{session_id}`
Delete a chat session

**Response:**
```json
{
  "success": true,
  "message": "Session deleted successfully"
}
```

#### `GET /api/sessions`
List all active sessions (for debugging)

**Response:**
```json
{
  "active_sessions": [
    "user_001_20251102223000",
    "user_002_20251102224500"
  ],
  "count": 2
}
```

---

## Frontend Integration Examples

### JavaScript/React Example

```javascript
// Chat with the agent
async function chatWithAgent(message, userId, sessionId = null) {
  const response = await fetch('http://localhost:8000/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: message,
      user_id: userId,
      session_id: sessionId,
    }),
  });
  
  const data = await response.json();
  return data;
}

// Create itinerary
async function createItinerary(itineraryData) {
  const response = await fetch('http://localhost:8000/api/itinerary/create', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(itineraryData),
  });
  
  const data = await response.json();
  return data;
}

// Usage
const chatResponse = await chatWithAgent(
  "Plan a trip to Tokyo",
  "user_001"
);
console.log(chatResponse.response);

// Continue conversation
const followUp = await chatWithAgent(
  "I want to go for 5 days",
  "user_001",
  chatResponse.session_id
);
```

### Python Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Chat with agent
def chat_with_agent(message, user_id, session_id=None):
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json={
            "message": message,
            "user_id": user_id,
            "session_id": session_id
        }
    )
    return response.json()

# Create itinerary
def create_itinerary(data):
    response = requests.post(
        f"{BASE_URL}/api/itinerary/create",
        json=data
    )
    return response.json()

# Usage
chat_response = chat_with_agent("Plan a trip to Tokyo", "user_001")
print(chat_response["response"])

# Create structured itinerary
itinerary = create_itinerary({
    "destination": "Tokyo, Japan",
    "start_date": "2025-12-01",
    "end_date": "2025-12-07",
    "travelers": 2,
    "user_id": "user_001"
})
print(itinerary)
```

---

## CORS Configuration

The API is configured to allow all origins by default for development. For production, update the CORS settings in `api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],  # Specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200`: Success
- `404`: Resource not found
- `500`: Internal server error

Error response format:
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Data Storage

- **User Profiles**: Stored in `tripmate_agents/profiles/{user_id}.json`
- **Itineraries**: Stored in `tripmate_agents/itinerary/{user_id}.json`
- **Sessions**: Stored in-memory (lost on server restart)

For production, consider using:
- Redis for session storage
- PostgreSQL/MongoDB for persistent data
- Cloud storage for itineraries and profiles

---

## Testing the API

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Plan a trip to Paris", "user_id": "test_user"}'

# Create itinerary
curl -X POST http://localhost:8000/api/itinerary/create \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Paris, France",
    "start_date": "2025-12-15",
    "end_date": "2025-12-20",
    "travelers": 2,
    "user_id": "test_user"
  }'

# Get itinerary
curl http://localhost:8000/api/itinerary/test_user
```

### Using the Interactive Docs

Visit `http://localhost:8000/docs` for an interactive Swagger UI where you can test all endpoints directly from your browser.

---

## Deployment Considerations

### Production Deployment

1. **Set proper CORS origins**
2. **Use environment variables** for all sensitive data
3. **Implement rate limiting** to prevent abuse
4. **Add authentication** (JWT, OAuth, etc.)
5. **Use a production WSGI server** (Gunicorn, uWSGI)
6. **Implement proper logging** and monitoring
7. **Use persistent storage** for sessions (Redis)
8. **Add caching** for frequently requested data

### Example Production Command

```bash
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## Support

For issues or questions:
1. Check the logs in the terminal where the API is running
2. Visit the interactive docs at `/docs`
3. Ensure all required environment variables are set

---

## Version

Current API Version: **1.0.0**
