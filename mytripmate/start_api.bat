@echo off
echo Starting MyTripMate API Server...
echo.

REM Check if virtual environment exists
if not exist ".venv\" (
    echo Creating virtual environment...
    python -m venv .venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
echo.

REM Install dependencies
echo Installing/updating dependencies...
pip install -r requirements.txt
echo.

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and configure it.
    echo.
    pause
    exit /b 1
)

REM Start the API server
echo Starting API server on port 8000...
echo API will be available at: http://localhost:8000
echo Swagger docs at: http://localhost:8000/docs
echo.
python api.py

pause
