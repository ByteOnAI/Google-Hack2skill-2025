from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
MODEL = os.environ.get("MODEL")
GOOGLE_GENAI_USE_VERTEXAI = os.environ.get("GOOGLE_GENAI_USE_VERTEXAI")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID")
GOOGLE_LOCATION = os.environ.get("GOOGLE_LOCATION")
GOOGLE_REGION = os.environ.get("GOOGLE_REGION")
