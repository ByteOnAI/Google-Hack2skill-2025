"""
Simple test script for MyTripMate API
Run this after starting the API server to test the endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print(f"{'='*60}\n")


def test_health_check():
    """Test health check endpoint"""
    print("Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    return response.status_code == 200


def test_user_profile():
    """Test user profile creation"""
    print("Testing User Profile Creation...")
    
    profile_data = {
        "user_id": "test_user_001",
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "phone": "+91-9000000000",
        "country_of_residence": "India",
        "timezone": "Asia/Kolkata",
        "preferred_currency": "INR",
        "languages": ["English"]
    }
    
    response = requests.post(f"{BASE_URL}/api/user/profile", json=profile_data)
    print_response("Create Profile", response)
    
    # Get the profile back
    print("Fetching Profile...")
    response = requests.get(f"{BASE_URL}/api/user/profile/test_user_001")
    print_response("Get Profile", response)
    
    return response.status_code == 200


def test_chat_basic():
    """Test basic chat endpoint"""
    print("Testing Chat Endpoint...")
    
    chat_data = {
        "message": "Hello! I want to plan a trip.",
        "user_id": "test_user_001"
    }
    
    response = requests.post(f"{BASE_URL}/api/chat", json=chat_data)
    print_response("Chat Response", response)
    
    if response.status_code == 200:
        # Extract session ID for continued conversation
        session_id = response.json().get("session_id")
        
        # Send follow-up message
        print("Sending follow-up message...")
        follow_up = {
            "message": "I'm interested in visiting Tokyo for 5 days.",
            "user_id": "test_user_001",
            "session_id": session_id
        }
        
        response = requests.post(f"{BASE_URL}/api/chat", json=follow_up)
        print_response("Follow-up Chat Response", response)
        
        return True
    
    return False


def test_itinerary_creation():
    """Test itinerary creation endpoint"""
    print("Testing Itinerary Creation...")
    
    itinerary_data = {
        "destination": "Tokyo, Japan",
        "start_date": "2025-12-01",
        "end_date": "2025-12-05",
        "travelers": 2,
        "budget": "moderate",
        "interests": ["technology", "food", "culture"],
        "user_id": "test_user_001"
    }
    
    response = requests.post(f"{BASE_URL}/api/itinerary/create", json=itinerary_data)
    print_response("Create Itinerary", response)
    
    if response.status_code == 200:
        # Try to get the itinerary
        print("Fetching saved itinerary...")
        time.sleep(1)  # Give it a moment to save
        response = requests.get(f"{BASE_URL}/api/itinerary/test_user_001")
        print_response("Get Itinerary", response)
        
        return True
    
    return False


def test_session_management():
    """Test session management"""
    print("Testing Session Management...")
    
    # List sessions
    response = requests.get(f"{BASE_URL}/api/sessions")
    print_response("List Sessions", response)
    
    return response.status_code == 200


def main():
    """Run all tests"""
    print("""
    ╔════════════════════════════════════════════╗
    ║   MyTripMate API Test Suite                ║
    ║   Make sure the API server is running!     ║
    ╚════════════════════════════════════════════╝
    """)
    
    try:
        tests = [
            ("Health Check", test_health_check),
            ("User Profile", test_user_profile),
            ("Chat Basic", test_chat_basic),
            ("Itinerary Creation", test_itinerary_creation),
            ("Session Management", test_session_management)
        ]
        
        results = []
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ Error in {test_name}: {str(e)}")
                results.append((test_name, False))
            
            time.sleep(0.5)  # Small delay between tests
        
        # Print summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        
        for test_name, result in results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{test_name:.<40} {status}")
        
        print("="*60)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        print(f"\nTotal: {passed}/{total} tests passed")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API server!")
        print("Make sure the API server is running at http://localhost:8000")
        print("Run: python api.py")


if __name__ == "__main__":
    main()
