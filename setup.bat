@echo off
REM CredTech Dashboard - Windows Setup Script

echo ================================
echo CredTech Dashboard Setup
echo ================================
echo.

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

python --version
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo ^^!^^! Please update .env with your FRED API key ^^!^^!
)

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo To start the dashboard, run:
echo   python app.py
echo.
echo Then open: http://localhost:5000
echo.
pause
