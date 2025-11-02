# 📋 MyTripMate API Setup Checklist

Use this checklist to get your API up and running!

---

## ✅ Setup Steps

### □ Step 1: Environment Configuration

- [ ] Copy `.env.example` to `.env`
  ```bash
  copy .env.example .env
  ```

- [ ] Edit `.env` with your credentials:
  - [ ] `GOOGLE_PROJECT_ID` - Your GCP project ID
  - [ ] `GOOGLE_MAPS_API_KEY` - Google Maps API key
  - [ ] `MODEL` - AI model (default: gemini-2.0-flash-exp)
  - [ ] `API_PORT` - Port number (default: 8000)

### □ Step 2: Dependencies

- [ ] Install required packages
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Verify installations:
  - [ ] `fastapi` installed
  - [ ] `uvicorn` installed
  - [ ] `google-adk` installed
  - [ ] `pydantic` installed

### □ Step 3: Start the API

Choose one method:

- [ ] **Method A**: Double-click `start_api.bat` (Windows)

- [ ] **Method B**: Run in terminal
  ```bash
  python api.py
  ```

- [ ] **Method C**: Use uvicorn directly
  ```bash
  uvicorn api:app --reload --port 8000
  ```

### □ Step 4: Verify API is Running

- [ ] Open browser to http://localhost:8000
  - Should see: `{"status":"healthy",...}`

- [ ] Check interactive docs:
  - [ ] Swagger UI: http://localhost:8000/docs
  - [ ] ReDoc: http://localhost:8000/redoc

### □ Step 5: Test the API

- [ ] Run test suite:
  ```bash
  python test_api.py
  ```

- [ ] Or test manually with curl:
  ```bash
  curl http://localhost:8000/health
  ```

---

## 🔍 Quick Tests

### Test 1: Health Check
```bash
curl http://localhost:8000/health
```
✅ **Expected**: `{"status":"healthy",...}`

### Test 2: Chat Endpoint
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"Hello\",\"user_id\":\"test\"}"
```
✅ **Expected**: JSON response with agent's greeting

### Test 3: Interactive Docs
- [ ] Visit http://localhost:8000/docs
- [ ] Try the `/api/chat` endpoint
- [ ] See response in browser

---

## 🌐 Frontend Integration Checklist

### □ Basic Integration

- [ ] Can make HTTP requests to API from frontend
- [ ] CORS is working (no CORS errors in console)
- [ ] Can parse JSON responses

### □ Chat Feature

- [ ] Send message to `/api/chat`
- [ ] Display agent response
- [ ] Save `session_id` from response
- [ ] Use `session_id` for follow-up messages

### □ Itinerary Feature

- [ ] Send data to `/api/itinerary/create`
- [ ] Display generated itinerary
- [ ] Fetch itinerary with `/api/itinerary/{user_id}`

### □ User Profile

- [ ] Create profile with `/api/user/profile` (POST)
- [ ] Fetch profile with `/api/user/profile/{user_id}` (GET)
- [ ] Use profile in chat requests

---

## 📁 Files Reference

| File | Purpose |
|------|---------|
| `api.py` | Main API server code |
| `.env` | Your configuration (create from .env.example) |
| `requirements.txt` | Python dependencies |
| `start_api.bat` | Quick start script (Windows) |
| `test_api.py` | Test suite |
| `API_DOCUMENTATION.md` | Complete API docs |
| `QUICKSTART.md` | Quick start guide |
| `API_INTEGRATION_SUMMARY.md` | Integration overview |

---

## 🆘 Troubleshooting

### Problem: Port already in use
**Solution**: Change port in `.env`:
```env
API_PORT=8001
```

### Problem: Module not found
**Solution**: Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

### Problem: CORS errors in frontend
**Solution**: Check `api.py` CORS configuration:
```python
allow_origins=["*"]  # For development
# OR for production:
allow_origins=["https://your-frontend.com"]
```

### Problem: Agent not responding
**Solution**: 
1. Check `.env` configuration
2. Verify Google Cloud credentials
3. Check API terminal logs for errors

### Problem: Cannot connect from frontend
**Solution**:
1. Verify API is running: `curl http://localhost:8000/health`
2. Check frontend is using correct URL
3. Ensure no firewall blocking

---

## ✨ Success Indicators

You'll know everything is working when:

- [x] ✅ `python api.py` starts without errors
- [x] ✅ http://localhost:8000/health returns `{"status":"healthy"}`
- [x] ✅ http://localhost:8000/docs shows Swagger UI
- [x] ✅ `python test_api.py` passes all tests
- [x] ✅ Frontend can make requests without CORS errors
- [x] ✅ Chat messages get intelligent responses
- [x] ✅ Itineraries are generated successfully

---

## 📞 Quick Command Reference

```bash
# Start API
python api.py

# Test API
python test_api.py

# Install dependencies
pip install -r requirements.txt

# Check health
curl http://localhost:8000/health

# Test chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"Plan a trip\",\"user_id\":\"test\"}"
```

---

## 🎯 Next Steps After Setup

1. **Read Documentation**
   - [ ] Review `API_DOCUMENTATION.md`
   - [ ] Check `QUICKSTART.md` examples

2. **Customize**
   - [ ] Edit agent prompts in `tripmate_agents/prompt.py`
   - [ ] Adjust CORS settings for production

3. **Integrate Frontend**
   - [ ] Follow examples in `QUICKSTART.md`
   - [ ] Test all endpoints from your app

4. **Deploy**
   - [ ] Follow deployment guidelines
   - [ ] Set up production environment variables
   - [ ] Configure production CORS

---

## 🎉 Ready to Go!

Once all checkboxes above are complete, you're ready to integrate the API with your frontend!

**Need help?** Check the documentation files or the API logs.

Happy coding! 🚀
