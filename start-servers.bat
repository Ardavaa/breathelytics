@echo off
echo ================================================
echo    🫁 BREATHELYTICS SERVER STARTER 🫁
echo ================================================
echo.

cd /d "%~dp0"
echo Current directory: %CD%
echo.

if exist ".venv\Scripts\activate.bat" (
    echo [INFO] Activating .venv virtual environment...
    call .venv\Scripts\activate.bat
    echo [SUCCESS] Virtual environment activated.
) else (
    echo [WARNING] No .venv found, using system Python.
)

echo.
echo [INFO] Checking Python...
python --version
echo.

echo Please choose an option:
echo.
echo 1. Start both servers (Frontend + Backend)
echo 2. Start frontend only (port 3000)
echo 3. Start backend only (port 5000)
echo 4. Development mode (both servers with auto-reload)
echo 5. Exit

:menu
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto start_both
if "%choice%"=="2" goto start_frontend
if "%choice%"=="3" goto start_backend
if "%choice%"=="4" goto start_dev
if "%choice%"=="5" goto exit_script
echo Invalid choice. Please try again.
goto menu

:start_both
echo.
echo Starting both servers...
python cli.py --both
echo.
echo Servers have stopped. Press any key to return to menu...
pause >nul
goto menu

:start_frontend
echo.
echo Starting frontend server...
python cli.py --frontend
echo.
echo Frontend server stopped. Press any key to return to menu...
pause >nul
goto menu

:start_backend
echo.
echo Starting backend server...
python cli.py --backend
echo.
echo Backend server stopped. Press any key to return to menu...
pause >nul
goto menu

:start_dev
echo.
echo Starting development mode...
python cli.py --dev
echo.
echo Development servers stopped. Press any key to return to menu...
pause >nul
goto menu

:exit_script
echo.
echo Goodbye! 👋
echo.
pause 