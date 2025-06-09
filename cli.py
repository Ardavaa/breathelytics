#!/usr/bin/env python3
"""
Breathelytics CLI - Start frontend and backend servers easily

Usage:
    python cli.py --frontend             # Start only frontend server
    python cli.py --backend              # Start only backend server  
    python cli.py --both                 # Start both servers
    python cli.py --dev                  # Development mode (both with auto-reload)
    python cli.py --help                 # Show help
"""

import os
import sys
import argparse
import subprocess
import signal
import time
import threading
from pathlib import Path
from typing import Optional, List, Dict, Any


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m' 
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class ServerManager:
    """Manages frontend and backend server processes."""
    
    def __init__(self):
        self.frontend_process: Optional[subprocess.Popen] = None
        self.backend_process: Optional[subprocess.Popen] = None
        self.running = True
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum: int, frame) -> None:
        """Handle shutdown signals gracefully."""
        print(f"\n{Colors.WARNING}Received signal {signum}, shutting down servers...{Colors.ENDC}")
        self.stop_all_servers()
        sys.exit(0)
    
    def _print_status(self, message: str, status: str = "INFO") -> None:
        """Print colored status message."""
        color_map = {
            "INFO": Colors.OKBLUE,
            "SUCCESS": Colors.OKGREEN, 
            "WARNING": Colors.WARNING,
            "ERROR": Colors.FAIL,
            "HEADER": Colors.HEADER
        }
        color = color_map.get(status, Colors.ENDC)
        print(f"{color}[{status}]{Colors.ENDC} {message}")
    
    def check_dependencies(self) -> bool:
        """Check if required dependencies are available."""
        self._print_status("Checking dependencies...", "INFO")
        
        # Check Python version
        if sys.version_info < (3, 10):
            self._print_status(f"Python 3.10+ required, found {sys.version}", "ERROR")
            return False
        
        # Check if virtual environment is activated (recommended)
        venv_detected = (
            hasattr(sys, 'real_prefix') or  # virtualenv
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or  # venv
            os.environ.get('VIRTUAL_ENV') is not None or  # Environment variable
            '.venv' in sys.executable  # Windows .venv in path
        )
        if not venv_detected:
            self._print_status("Virtual environment not detected. Consider using venv/conda.", "WARNING")
        
        # Check if backend dependencies exist
        try:
            import flask
            self._print_status("✓ Flask found", "SUCCESS")
        except ImportError:
            self._print_status("Flask not found. Run: pip install -r requirements.txt", "ERROR")
            return False
        
        # Check if frontend directory exists
        frontend_path = Path("src/breathelytics-frontend")
        if not frontend_path.exists():
            self._print_status("Frontend directory not found", "ERROR")
            return False
        
        # Check if backend directory exists  
        backend_path = Path("src/breathelytics-backend")
        if not backend_path.exists():
            self._print_status("Backend directory not found", "ERROR")
            return False
        
        self._print_status("✓ All dependencies checked", "SUCCESS")
        return True
    
    def start_frontend_server(self, port: int = 3000, dev_mode: bool = False) -> bool:
        """Start the frontend server."""
        try:
            frontend_dir = Path("src/breathelytics-frontend")
            if not frontend_dir.exists():
                self._print_status("Frontend directory not found", "ERROR")
                return False
            
            self._print_status(f"Starting frontend server on port {port}...", "INFO")
            
            if dev_mode:
                # For development, we could use live-server if installed
                # But we'll use Python's built-in server with watch capability
                cmd = [sys.executable, "-m", "http.server", str(port)]
            else:
                cmd = [sys.executable, "-m", "http.server", str(port)]
            
            self.frontend_process = subprocess.Popen(
                cmd,
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Give server time to start
            time.sleep(1)
            
            if self.frontend_process.poll() is None:
                self._print_status(f"✓ Frontend server started at http://localhost:{port}", "SUCCESS")
                return True
            else:
                self._print_status("Failed to start frontend server", "ERROR")
                return False
                
        except Exception as e:
            self._print_status(f"Error starting frontend server: {str(e)}", "ERROR")
            return False
    
    def start_backend_server(self, port: int = 5000, dev_mode: bool = False, production_mode: bool = False, verbose: bool = False) -> bool:
        """Start the backend server."""
        try:
            backend_dir = Path("src/breathelytics-backend")
            if not backend_dir.exists():
                self._print_status("Backend directory not found", "ERROR")
                return False
            
            self._print_status(f"Starting backend server on port {port}...", "INFO")
            
            # Set environment variables
            env = os.environ.copy()
            env['FLASK_APP'] = 'run.py'
            env['PYTHONPATH'] = str(backend_dir)
            
            # Configure environment based on mode
            if production_mode:
                env['FLASK_ENV'] = 'production'
                env['FLASK_DEBUG'] = 'False'
                # Don't set SECRET_KEY - let it fail if not provided
                if 'SECRET_KEY' not in env:
                    self._print_status("Production mode requires SECRET_KEY environment variable", "ERROR")
                    return False
            else:
                env['FLASK_ENV'] = 'development'
                env['FLASK_DEBUG'] = 'True' if dev_mode else 'False'
                # Set a default SECRET_KEY for development
                if 'SECRET_KEY' not in env:
                    env['SECRET_KEY'] = 'breathelytics-dev-key-2024'
            
            if dev_mode:
                cmd = [sys.executable, "run.py"]
            else:
                cmd = [sys.executable, "run.py"]
            
            # For verbose mode or dev mode, show real-time output
            # Otherwise capture output for cleaner UI
            if verbose or dev_mode:
                self._print_status("Starting backend with real-time output...", "INFO")
                self.backend_process = subprocess.Popen(
                    cmd,
                    cwd=backend_dir,
                    env=env
                )
            else:
                # Create log files for captured output
                log_dir = backend_dir / 'logs'
                log_dir.mkdir(exist_ok=True)
                
                with open(log_dir / 'backend_stdout.log', 'w') as stdout_log, \
                     open(log_dir / 'backend_stderr.log', 'w') as stderr_log:
                    
                    self.backend_process = subprocess.Popen(
                        cmd,
                        cwd=backend_dir,
                        stdout=stdout_log,
                        stderr=stderr_log,
                        env=env
                    )
                
                self._print_status(f"Backend logs: {log_dir}/backend_stdout.log, {log_dir}/backend_stderr.log", "INFO")
            
            # Give server more time to start (backend takes longer)
            time.sleep(3)
            
            # Test if backend is actually responding
            try:
                import urllib.request
                import urllib.error
                
                test_url = f"http://localhost:{port}/api/health"
                request = urllib.request.Request(test_url)
                with urllib.request.urlopen(request, timeout=5) as response:
                    if response.getcode() == 200:
                        self._print_status(f"✓ Backend server started at http://localhost:{port}", "SUCCESS")
                        return True
                    else:
                        self._print_status(f"Backend server not responding (HTTP {response.getcode()})", "ERROR")
                        return False
                        
            except urllib.error.URLError as e:
                self._print_status(f"Backend server not responding: {str(e)}", "ERROR")
                
                # If not verbose, show last few lines of error log
                if not verbose and not dev_mode:
                    try:
                        stderr_log_path = backend_dir / 'logs' / 'backend_stderr.log'
                        if stderr_log_path.exists():
                            with open(stderr_log_path, 'r') as f:
                                lines = f.readlines()
                                if lines:
                                    self._print_status("Last error log entries:", "ERROR")
                                    for line in lines[-5:]:  # Show last 5 lines
                                        print(f"  {line.strip()}")
                    except Exception:
                        pass
                        
                return False
                
        except Exception as e:
            self._print_status(f"Error starting backend server: {str(e)}", "ERROR")
            return False
    
    def stop_all_servers(self) -> None:
        """Stop all running servers."""
        self.running = False
        
        if self.frontend_process and self.frontend_process.poll() is None:
            self._print_status("Stopping frontend server...", "INFO")
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
                self._print_status("✓ Frontend server stopped", "SUCCESS")
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
                self._print_status("✗ Frontend server forcefully killed", "WARNING")
        
        if self.backend_process and self.backend_process.poll() is None:
            self._print_status("Stopping backend server...", "INFO") 
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
                self._print_status("✓ Backend server stopped", "SUCCESS")
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
                self._print_status("✗ Backend server forcefully killed", "WARNING")
    
    def monitor_servers(self) -> None:
        """Monitor server processes and restart if they crash."""
        while self.running:
            try:
                # Check frontend process
                if self.frontend_process and self.frontend_process.poll() is not None:
                    self._print_status("Frontend server stopped unexpectedly", "ERROR")
                    self.running = False
                    break
                
                # Check backend process  
                if self.backend_process and self.backend_process.poll() is not None:
                    self._print_status("Backend server stopped unexpectedly", "ERROR")
                    self.running = False
                    break
                
                time.sleep(1)
                
            except KeyboardInterrupt:
                break
        
        self.stop_all_servers()


def print_banner() -> None:
    """Print CLI banner."""
    banner = f"""
{Colors.HEADER}══════════════════════════════════════════════════════════════════
                    🫁 BREATHELYTICS CLI 🫁                       
              AI-Powered Respiratory Disease Detection               
══════════════════════════════════════════════════════════════════{Colors.ENDC}

{Colors.OKCYAN}Start your frontend and backend servers with ease!{Colors.ENDC}
"""
    print(banner)


def print_help() -> None:
    """Print help information."""
    help_text = f"""
{Colors.BOLD}USAGE:{Colors.ENDC}
    python cli.py [OPTIONS]

{Colors.BOLD}OPTIONS:{Colors.ENDC}
    {Colors.OKGREEN}--frontend{Colors.ENDC}        Start only frontend server (port 3000)
    {Colors.OKGREEN}--backend{Colors.ENDC}         Start only backend server (port 5000)
    {Colors.OKGREEN}--both{Colors.ENDC}            Start both frontend and backend servers
    {Colors.OKGREEN}--dev{Colors.ENDC}             Development mode (both servers with auto-reload)
    {Colors.OKGREEN}--production{Colors.ENDC}      Production mode (requires SECRET_KEY)
    {Colors.OKGREEN}--frontend-port{Colors.ENDC}   Specify frontend port (default: 3000)
    {Colors.OKGREEN}--backend-port{Colors.ENDC}    Specify backend port (default: 5000)
    {Colors.OKGREEN}--verbose{Colors.ENDC}         Show real-time backend output
    {Colors.OKGREEN}--help{Colors.ENDC}            Show this help message

{Colors.BOLD}EXAMPLES:{Colors.ENDC}
    python cli.py --both                           # Start both servers
    python cli.py --dev                            # Development mode  
    python cli.py --frontend --frontend-port 8080  # Frontend on port 8080
    python cli.py --backend --backend-port 5001    # Backend on port 5001

{Colors.BOLD}NOTES:{Colors.ENDC}
    • Frontend will be available at http://localhost:3000 (or specified port)
    • Backend API will be available at http://localhost:5000 (or specified port)
    • Use Ctrl+C to stop all servers gracefully
    • Make sure you have activated your virtual environment
"""
    print(help_text)


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Breathelytics CLI - Start frontend and backend servers",
        add_help=False  # Custom help
    )
    
    parser.add_argument('--frontend', action='store_true', help='Start frontend server')
    parser.add_argument('--backend', action='store_true', help='Start backend server')
    parser.add_argument('--both', action='store_true', help='Start both servers')
    parser.add_argument('--dev', action='store_true', help='Development mode')
    parser.add_argument('--production', action='store_true', help='Production mode (requires SECRET_KEY)')
    parser.add_argument('--frontend-port', type=int, default=3000, help='Frontend port')
    parser.add_argument('--backend-port', type=int, default=5000, help='Backend port')
    parser.add_argument('--verbose', action='store_true', help='Show real-time backend output')
    parser.add_argument('--help', action='store_true', help='Show help')
    
    args = parser.parse_args()
    
    # Show help
    if args.help or len(sys.argv) == 1:
        print_banner()
        print_help()
        return
    
    # Print banner
    print_banner()
    
    # Initialize server manager
    manager = ServerManager()
    
    # Check dependencies
    if not manager.check_dependencies():
        manager._print_status("Dependency check failed. Please fix the issues above.", "ERROR")
        sys.exit(1)
    
    try:
        # Determine what to start
        start_frontend = args.frontend or args.both or args.dev
        start_backend = args.backend or args.both or args.dev
        dev_mode = args.dev
        production_mode = args.production
        
        if not start_frontend and not start_backend:
            manager._print_status("No servers specified. Use --help for usage information.", "WARNING")
            return
        
        # Start servers
        success = True
        
        if start_backend:
            if not manager.start_backend_server(args.backend_port, dev_mode, production_mode, args.verbose):
                success = False
        
        if start_frontend and success:
            if not manager.start_frontend_server(args.frontend_port, dev_mode):
                success = False
        
        if not success:
            manager._print_status("Failed to start one or more servers", "ERROR")
            manager.stop_all_servers()
            sys.exit(1)
        
        # Print access information
        print(f"\n{Colors.BOLD}🚀 SERVERS RUNNING:{Colors.ENDC}")
        if start_frontend:
            print(f"   {Colors.OKCYAN}Frontend:{Colors.ENDC} http://localhost:{args.frontend_port}")
        if start_backend:
            print(f"   {Colors.OKCYAN}Backend:{Colors.ENDC}  http://localhost:{args.backend_port}")
        
        print(f"\n{Colors.WARNING}Press Ctrl+C to stop all servers{Colors.ENDC}\n")
        
        # Monitor servers
        manager.monitor_servers()
        
    except KeyboardInterrupt:
        manager._print_status("Received keyboard interrupt", "INFO")
    except Exception as e:
        manager._print_status(f"Unexpected error: {str(e)}", "ERROR")
    finally:
        manager.stop_all_servers()
        manager._print_status("CLI terminated", "INFO")


if __name__ == '__main__':
    main() 