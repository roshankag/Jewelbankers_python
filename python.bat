@echo off
REM Set environment variables
set GENAI_API_KEY=AIzaSyCivb2rBfdp-xP-nU7xCszkpOo5JdJM-24
set GOOGLE_APPLICATION_CREDENTIALS_NEW=C:\Users\deepa\Downloads\orbital-stream-426213-r2-6040f858ab8b.json

REM Activate the virtual environment if needed
REM call path\to\your\venv\Scripts\activate.bat

REM Set the Python environment variable to use the new Google credentials
set GOOGLE_APPLICATION_CREDENTIALS=%GOOGLE_APPLICATION_CREDENTIALS_NEW%

REM Install the wheel file
pip install dist\main-0.1-py3-none-any.whl

REM Run the FastAPI application
uvicorn main:app --host 0.0.0.0 --port 8000

REM Pause to keep the window open
pause
