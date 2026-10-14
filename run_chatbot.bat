@echo off
title Campus & Placement AI FAQ Chatbot
echo ========================================================
echo  Starting Campus & Placement AI FAQ Chatbot (Streamlit)
echo ========================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in your system PATH.
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

:: Check if virtual environment exists, if not create one
if not exist "venv" (
    echo [1/3] Creating virtual environment 'venv'...
    python -m venv venv
)

:: Activate virtual environment
echo [2/3] Activating virtual environment...
call venv\Scripts\activate.bat

:: Install dependencies
echo [3/3] Checking dependencies...
pip install -r requirements.txt --quiet

echo.
echo ========================================================
echo  Launching Streamlit Web App...
echo  (Press Ctrl+C in this terminal window to stop the app)
echo ========================================================
echo.
streamlit run app.py

pause
