@echo off
:: Breathelytics Server Starter (Windows)
:: Simple batch file to start frontend and backend servers

echo.
echo ================================================
echo    🫁 BREATHELYTICS SERVER STARTER 🫁
echo ================================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.10+ and add it to PATH.
    pause
    exit /b 1
)

:: Check if CLI exists
if not exist "cli.py" (
    echo [ERROR] cli.py not found. Make sure you're in the project root directory.
    pause
    exit /b 1
)

:: Menu options
echo Please choose an option:
echo.
echo 1. Start both servers (Frontend + Backend)
echo 2. Start frontend only (port 3000)
echo 3. Start backend only (port 5000)
echo 4. Development mode (both servers with auto-reload)
echo 5. Show help
echo 6. Exit
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" (
    echo Starting both servers...
    python cli.py --both
) else if "%choice%"=="2" (
    echo Starting frontend server...
    python cli.py --frontend
) else if "%choice%"=="3" (
    echo Starting backend server...
    python cli.py --backend
) else if "%choice%"=="4" (
    echo Starting development mode...
    python cli.py --dev
) else if "%choice%"=="5" (
    python cli.py --help
    pause
) else if "%choice%"=="6" (
    echo Goodbye!
    exit /b 0
) else (
    echo Invalid choice. Please try again.
    pause
    goto :eof
)

pause 