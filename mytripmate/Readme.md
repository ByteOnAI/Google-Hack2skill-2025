# My Trip Mate ✈️

My Trip Mate is a powerful and intelligent tool designed to help you create personalized travel itineraries. Leveraging a sophisticated agent powered by Google's Vertex AI, it seamlessly integrates with various services to craft the perfect trip plan tailored to your preferences.

## ✨ Features

*   **Personalized Itinerary Generation:** Get custom travel plans based on your interests, duration, and destination.
*   **Intelligent Tool Orchestration:** A central agent intelligently uses a suite of tools to gather the best information.
*   **Real-time Location Data:** Utilizes Google Maps for accurate information on places, directions, and points of interest.
*   **Live Weather Forecasts:** Integrates a weather API to provide up-to-date weather conditions for your trip.
*   **Scalable Backend:** Uses Firebase for robust data storage, potentially for user profiles and saved itineraries.

## 🤖 How It Works

The core of My Trip Mate is a central agent built on **Vertex AI**. This agent acts as an orchestrator, analyzing your travel requests in natural language. Based on your query, it intelligently selects and utilizes a suite of powerful tools to gather information and build your itinerary.

For example, when you ask for a trip plan, the agent might:
1.  Use **Google Search** to find attractions, restaurants, and hotels based on your interests.
2.  Use a **Weather API** to check the forecast for your travel dates.
3.  Structure the information into a day-by-day itinerary.
4.  Use **Firebase** to save the generated plan to your user profile.

This multi-tool approach allows the agent to handle complex, multi-step requests and provide comprehensive, actionable travel plans.

## 🛠️ Tools

My Trip Mate's agent is equipped with the following tools:

*   **Vertex AI:** The brain of the operation, hosting the generative AI model that powers our intelligent agent.
*   **Google Maps API:** For all location-based queries, including finding places, calculating distances, and getting directions.
*   **Weather API:** To provide real-time weather forecasts for your destinations.
*   **Firebase:** For backend services, including user authentication, and storing user profiles and saved itineraries.

## 🚀 Getting Started

### Prerequisites

*   Python 3.9+
*   `pip` package manager
*   A Google Cloud Platform (GCP) project with the required APIs enabled (Vertex AI, Google Maps, etc.).

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/my-trip-mate.git
cd my-trip-mate
```

### 2. Set up a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root of the project and add your API keys and project configuration.

```env
# .env

# Google Cloud / Vertex AI
GCP_PROJECT_ID="your-gcp-project-id"
GCP_LOCATION="your-gcp-location" # e.g., us-central1

# Google Maps
GOOGLE_MAPS_API_KEY="your-google-maps-api-key"

# Weather API
WEATHER_API_KEY="your-weather-api-key"

# Firebase (as a JSON string or path to service account file)   
FIREBASE_SERVICE_ACCOUNT_KEY_PATH="/path/to/your/firebase-service-account.json"
```

## Usage

You can interact with the My Trip Mate agent through a command-line interface or by running the main application.

**Example Interaction:**

```bash
python main.py "Plan a 5-day trip to Tokyo for someone who loves anime and technology."
```

The agent will then process the request and output a detailed itinerary.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for bugs, feature requests, or other improvements.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.