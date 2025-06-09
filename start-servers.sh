#!/bin/bash
# Breathelytics Server Starter (Unix/Linux/macOS)
# Simple shell script to start frontend and backend servers

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "\n================================================"
echo -e "   🫁 ${CYAN}BREATHELYTICS SERVER STARTER${NC} 🫁"
echo -e "================================================\n"

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Python not found. Please install Python 3.10+ and add it to PATH."
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

# Check for and activate virtual environment
if [ -f ".venv/Scripts/activate" ]; then
    echo -e "${BLUE}[INFO]${NC} Activating virtual environment (.venv)..."
    source .venv/Scripts/activate
    PYTHON_CMD="python.exe"  # Use python.exe in Windows venv
elif [ -f ".venv/bin/activate" ]; then
    echo -e "${BLUE}[INFO]${NC} Activating virtual environment (.venv)..."
    source .venv/bin/activate
    PYTHON_CMD="python"
elif [ -d "venv" ] && [ -f "venv/bin/activate" ]; then
    echo -e "${BLUE}[INFO]${NC} Activating virtual environment (venv)..."
    source venv/bin/activate
    PYTHON_CMD="python"
else
    echo -e "${YELLOW}[WARNING]${NC} No virtual environment found. Using system Python."
fi

# Check if CLI exists
if [ ! -f "cli.py" ]; then
    echo -e "${RED}[ERROR]${NC} cli.py not found. Make sure you're in the project root directory."
    exit 1
fi

# Menu function
show_menu() {
    echo "Please choose an option:"
    echo ""
    echo -e "${GREEN}1.${NC} Start both servers (Frontend + Backend)"
    echo -e "${GREEN}2.${NC} Start frontend only (port 3000)"
    echo -e "${GREEN}3.${NC} Start backend only (port 5000)"
    echo -e "${GREEN}4.${NC} Development mode (both servers with auto-reload)"
    echo -e "${GREEN}5.${NC} Show help"
    echo -e "${GREEN}6.${NC} Exit"
    echo ""
}

# Main loop
while true; do
    show_menu
    read -p "Enter your choice (1-6): " choice
    
    case $choice in
        1)
            echo -e "${BLUE}Starting both servers...${NC}"
            $PYTHON_CMD cli.py --both
            break
            ;;
        2)
            echo -e "${BLUE}Starting frontend server...${NC}"
            $PYTHON_CMD cli.py --frontend
            break
            ;;
        3)
            echo -e "${BLUE}Starting backend server...${NC}"
            $PYTHON_CMD cli.py --backend
            break
            ;;
        4)
            echo -e "${BLUE}Starting development mode...${NC}"
            $PYTHON_CMD cli.py --dev
            break
            ;;
        5)
            $PYTHON_CMD cli.py --help
            echo ""
            read -p "Press Enter to continue..."
            ;;
        6)
            echo -e "${YELLOW}Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice. Please try again.${NC}"
            echo ""
            ;;
    esac
done 