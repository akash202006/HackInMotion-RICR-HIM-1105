@echo off
REM SMART AI FORECASTING - Quick Start Script
REM This script helps set up and run the entire stack

setlocal enabledelayedexpansion

echo.
echo ========================================
echo SMART AI FORECASTING - Quick Start
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "frontend" (
    echo ERROR: Please run this script from the project root directory
    echo Expected to find: frontend/, backend/, database/ folders
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.9+
    pause
    exit /b 1
)
echo ✓ Python found

echo.
echo [2/4] Setting up backend...
cd backend

if not exist ".env" (
    echo ERROR: .env file not found in backend/
    echo Please copy .env.example to .env and add your Supabase credentials
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -q -r requirements.txt
echo ✓ Dependencies installed

cd ..

echo.
echo [3/4] Backend is ready!
echo To start backend, open a new terminal and run:
echo   cd backend
echo   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
echo.
echo [4/4] Frontend is ready!
echo To start frontend, open another new terminal and run:
echo   cd frontend
echo   python -m http.server 8000
echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Open your browser:
echo   Frontend: http://localhost:8000
echo   Backend Docs: http://localhost:8001/docs
echo   Database: Visit Supabase dashboard
echo.
echo Next steps:
echo 1. Run database setup (see database/README.md)
echo 2. Start backend and frontend in separate terminals
echo 3. Visit http://localhost:8000 and create an account
echo.
pause
