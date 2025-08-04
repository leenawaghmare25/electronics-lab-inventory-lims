@echo off
REM Electronics Lab Inventory - LIMS Setup Script for Windows
REM This script sets up the development environment

echo ============================================================
echo Electronics Lab Inventory - LIMS Setup
echo ============================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo ✅ Python is installed

REM Run the Python setup script
python setup.py

echo.
echo ============================================================
echo Setup completed! 
echo ============================================================
echo.
echo To start development:
echo 1. Activate virtual environment: venv\Scripts\activate
echo 2. Go to backend folder: cd backend  
echo 3. Run the server: python app.py
echo.
pause