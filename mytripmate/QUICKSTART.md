# MyTripMate API - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

```bash
cd mytripmate
pip install -r requirements.txt
```

### Step 2: Configure Environment

1. Copy the example environment file:
```bash
copy .env.example .env
```

2. Edit `.env` and add your API keys:
```env
GOOGLE_PROJECT_ID=your-project-id
GOOGLE_MAPS_API_KEY=your-maps-api-key
MODEL=gemini-2.0-flash-exp
API_PORT=8000
```

### Step 3: Start the API Server

**Option A: Using the batch file (Windows)**
```bash
start_api.bat
```

**Option B: Using Python directly**
```bash
python api.py
```

**Option C: Using uvicorn**
```bash
uvicorn api:app --reload --port 8000
```

The API will start at `http://localhost:8000`

### Step 4: Test the API

Open a new terminal and run:
```bash
python test_api.py
```

Or visit the interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📡 Connect Your Frontend

### React/Next.js Example

Create an API client:

```javascript
// lib/api.js
const API_BASE_URL = 'http://localhost:8000';

export async function sendMessage(message, userId, sessionId = null) {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, user_id: userId, session_id: sessionId })
  });
  return response.json();
}

export async function createItinerary(data) {
  const response = await fetch(`${API_BASE_URL}/api/itinerary/create`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return response.json();
}

export async function getItinerary(userId) {
  const response = await fetch(`${API_BASE_URL}/api/itinerary/${userId}`);
  return response.json();
}
```

Use in your components:

```javascript
// components/ChatBox.jsx
import { useState } from 'react';
import { sendMessage } from '@/lib/api';

export default function ChatBox({ userId }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState(null);

  const handleSend = async () => {
    if (!input.trim()) return;

    // Add user message to UI
    setMessages([...messages, { role: 'user', content: input }]);

    // Send to API
    const response = await sendMessage(input, userId, sessionId);
    
    // Update session ID
    setSessionId(response.session_id);

    // Add agent response to UI
    setMessages(prev => [
      ...prev,
      { role: 'agent', content: response.response }
    ]);

    setInput('');
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
      </div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        placeholder="Ask about your trip..."
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}
```

### Vue.js Example

```javascript
// composables/useTrip.js
import { ref } from 'vue';

export function useTrip() {
  const API_BASE_URL = 'http://localhost:8000';
  const sessionId = ref(null);

  async function chat(message, userId) {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        user_id: userId,
        session_id: sessionId.value
      })
    });

    const data = await response.json();
    sessionId.value = data.session_id;
    return data;
  }

  async function createItinerary(itineraryData) {
    const response = await fetch(`${API_BASE_URL}/api/itinerary/create`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(itineraryData)
    });
    return response.json();
  }

  return { chat, createItinerary, sessionId };
}
```

### Angular Example

```typescript
// services/trip.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class TripService {
  private apiUrl = 'http://localhost:8000';
  private sessionId: string | null = null;

  constructor(private http: HttpClient) {}

  chat(message: string, userId: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/api/chat`, {
      message,
      user_id: userId,
      session_id: this.sessionId
    });
  }

  createItinerary(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/api/itinerary/create`, data);
  }

  getItinerary(userId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/api/itinerary/${userId}`);
  }
}
```

---

## 🎯 Common Use Cases

### 1. Simple Chat Interface

```javascript
// Start a conversation
const response1 = await sendMessage(
  "I want to plan a trip",
  "user_123"
);
console.log(response1.response);
// "Hi User — I'd be happy to help! Do you already know your destination..."

// Continue conversation
const response2 = await sendMessage(
  "Yes, I want to go to Paris",
  "user_123",
  response1.session_id
);
console.log(response2.response);
```

### 2. Direct Itinerary Creation

```javascript
const itinerary = await createItinerary({
  destination: "Paris, France",
  start_date: "2025-12-15",
  end_date: "2025-12-20",
  travelers: 2,
  budget: "moderate",
  interests: ["art", "food", "history"],
  user_id: "user_123"
});

console.log(itinerary.itinerary);
```

### 3. User Profile Management

```javascript
// Save user profile
await fetch('http://localhost:8000/api/user/profile', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_id: "user_123",
    first_name: "John",
    preferred_currency: "USD",
    timezone: "America/New_York",
    languages: ["English"]
  })
});

// Get profile
const profile = await fetch('http://localhost:8000/api/user/profile/user_123')
  .then(r => r.json());
```

---

## 🔧 Troubleshooting

### API Won't Start

1. **Check if port 8000 is already in use:**
   ```bash
   netstat -ano | findstr :8000
   ```

2. **Change the port in .env:**
   ```env
   API_PORT=8001
   ```

### Connection Refused from Frontend

1. **Enable CORS for your frontend domain** in `api.py`:
   ```python
   allow_origins=["http://localhost:3000"]  # Your frontend URL
   ```

2. **Check if API is running:**
   ```bash
   curl http://localhost:8000/health
   ```

### Agent Not Responding

1. **Check your .env configuration**
2. **Verify Google Cloud credentials**
3. **Check API logs in the terminal**

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 📚 Next Steps

1. **Read the full documentation**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
2. **Explore the interactive docs**: http://localhost:8000/docs
3. **Run the test suite**: `python test_api.py`
4. **Customize the agent**: Edit prompts in `tripmate_agents/prompt.py`

---

## 🌟 Key Endpoints Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/chat` | POST | Chat with agent |
| `/api/itinerary/create` | POST | Create itinerary |
| `/api/itinerary/{user_id}` | GET | Get saved itinerary |
| `/api/user/profile` | POST | Save user profile |
| `/api/user/profile/{user_id}` | GET | Get user profile |
| `/api/sessions` | GET | List active sessions |

---

## 💡 Tips

- **Sessions persist** until server restart (use Redis for production)
- **User profiles** are saved to `tripmate_agents/profiles/`
- **Itineraries** are saved to `tripmate_agents/itinerary/`
- **Use session_id** to maintain conversation context
- **Customize the agent** by editing prompt files

---

## 🤝 Need Help?

- Check the logs when running the API
- Use the interactive docs at `/docs`
- Run `python test_api.py` to diagnose issues
- Verify all environment variables are set correctly

Happy coding! 🚀
