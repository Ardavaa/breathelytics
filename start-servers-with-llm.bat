@echo off
echo =====================================================
echo    Starting Breathelytics Servers with LLM Support
echo =====================================================

REM Set Gemini API Key
set GEMINI_API_KEY=AIzaSyAEhKUQKI9iQe2KOl_pP62TK1nV3PyTBrs
set ENABLE_LLM=True

REM Kill any existing servers
echo Stopping existing servers...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul

REM Start Backend Server in background
echo Starting Backend Server with LLM...
cd src\breathelytics-backend
start /b python app.py > backend.log 2>&1

REM Wait for backend to start
timeout /t 5 /nobreak >nul

REM Start Frontend Server in background
echo Starting Frontend Server...
cd ..\breathelytics-frontend
start /b python -m http.server 8080 > frontend.log 2>&1

REM Wait a moment for servers to initialize
timeout /t 2 /nobreak >nul

echo.
echo =====================================================
echo   Servers started successfully in background!
echo   Backend: http://localhost:5000 (with LLM support)
echo   Frontend: http://localhost:8080
echo =====================================================
echo.
echo Servers are running in the background.
echo Check backend.log and frontend.log for server output.
echo To stop servers, run: taskkill /f /im python.exe
echo.
echo Press any key to exit this window...
pause >nul 