#!/bin/bash
# Breathelytics Server Starter (Unix/Linux/macOS/Git Bash)

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "\n================================================"
echo -e "   🫁 ${CYAN}BREATHELYTICS SERVER STARTER${NC} 🫁"
echo -e "================================================\n"

# Change to script directory
cd "$(dirname "$0")"
echo "Current directory: $(pwd)"
echo

# Check for and activate virtual environment
if [ -f ".venv/Scripts/activate" ]; then
    echo -e "${BLUE}[INFO]${NC} Activating .venv virtual environment (Windows)..."
    source .venv/Scripts/activate
    PYTHON_CMD="python"
elif [ -f ".venv/bin/activate" ]; then
    echo -e "${BLUE}[INFO]${NC} Activating .venv virtual environment (Unix)..."
    source .venv/bin/activate
    PYTHON_CMD="python"
elif [ -f "venv/bin/activate" ]; then
    echo -e "${BLUE}[INFO]${NC} Activating venv virtual environment..."
    source venv/bin/activate
    PYTHON_CMD="python"
else
    echo -e "${YELLOW}[WARNING]${NC} No virtual environment found, using system Python."
    # Try python3 first, then python
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}[ERROR]${NC} Python not found. Please install Python 3.10+"
        exit 1
    fi
fi

echo
echo -e "${BLUE}[INFO]${NC} Checking Python..."
$PYTHON_CMD --version
echo

echo "Please choose an option:"
echo
echo "1. Start both servers (Frontend + Backend)"
echo "2. Start frontend only (port 3000)"
echo "3. Start backend only (port 5000)"
echo "4. Development mode (both servers with auto-reload)"
echo "5. Exit"

menu() {
    read -p "Enter your choice (1-5): " choice
    
    case $choice in
        1)
            start_both
            ;;
        2)
            start_frontend
            ;;
        3)
            start_backend
            ;;
        4)
            start_dev
            ;;
        5)
            exit_script
            ;;
        *)
            echo "Invalid choice. Please try again."
            menu
            ;;
    esac
}

start_both() {
    echo
    echo "Starting both servers..."
    $PYTHON_CMD cli.py --both
    echo
    echo "Servers have stopped. Press Enter to return to menu..."
    read
    menu
}

start_frontend() {
    echo
    echo "Starting frontend server..."
    $PYTHON_CMD cli.py --frontend
    echo
    echo "Frontend server stopped. Press Enter to return to menu..."
    read
    menu
}

start_backend() {
    echo
    echo "Starting backend server..."
    $PYTHON_CMD cli.py --backend
    echo
    echo "Backend server stopped. Press Enter to return to menu..."
    read
    menu
}

start_dev() {
    echo
    echo "Starting development mode..."
    $PYTHON_CMD cli.py --dev
    echo
    echo "Development servers stopped. Press Enter to return to menu..."
    read
    menu
}

exit_script() {
    echo
    echo "Goodbye! 👋"
    echo
    exit 0
}

# Start the menu
menu 