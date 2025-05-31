#!/usr/bin/env python3
"""
Production startup script for Breathelytics Flask API.

Handles environment setup, logging configuration, and graceful startup/shutdown.
"""

import os
import sys
import signal
import logging
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app import app
from config import get_config
from utils import cleanup_temp_files


def setup_signal_handlers() -> None:
    """Setup signal handlers for graceful shutdown."""
    
    def signal_handler(signum: int, frame) -> None:
        """Handle shutdown signals gracefully."""
        logger = logging.getLogger('breathelytics')
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        
        # Cleanup temporary files
        try:
            config = get_config()
            cleaned_count = cleanup_temp_files(config.TEMP_DIR)
            logger.info(f"Cleaned up {cleaned_count} temporary files")
        except Exception as e:
            logger.warning(f"Error during cleanup: {str(e)}")
        
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


def validate_environment() -> bool:
    """
    Validate that the environment is properly configured.
    
    Returns:
        bool: True if environment is valid, False otherwise
    """
    logger = logging.getLogger('breathelytics')
    
    # Check if model file exists
    model_path = Path(__file__).parent / 'respiratory_classifier.pkl'
    if not model_path.exists():
        logger.warning(f"Model file not found: {model_path}")
        logger.warning("Prediction endpoint will return 503 errors")
    else:
        logger.info(f"Model file found: {model_path}")
    
    # Check Python version
    if sys.version_info < (3, 10):
        logger.error(f"Python 3.10+ required, found {sys.version}")
        return False
    
    # Check required directories
    config = get_config()
    try:
        config.init_directories()
        logger.info("Required directories initialized")
    except Exception as e:
        logger.error(f"Failed to create directories: {str(e)}")
        return False
    
    return True


def main() -> None:
    """Main entry point for the application."""
    
    # Get configuration
    config = get_config()
    
    # Setup signal handlers
    setup_signal_handlers()
    
    # Validate environment
    if not validate_environment():
        sys.exit(1)
    
    # Get logger
    logger = logging.getLogger('breathelytics')
    
    # Print startup information
    logger.info("=" * 50)
    logger.info("Starting Breathelytics Flask API")
    logger.info(f"Version: {config.VERSION}")
    logger.info(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    logger.info(f"Host: {config.HOST}")
    logger.info(f"Port: {config.PORT}")
    logger.info(f"Debug: {config.DEBUG}")
    logger.info("=" * 50)
    
    try:
        # Initialize ML pipeline on startup
        from pipeline import create_respiratory_pipeline
        
        logger.info("Initializing ML pipeline...")
        pipeline = create_respiratory_pipeline()
        logger.info("ML pipeline initialized successfully")
        
        # Start the Flask application
        logger.info("Starting Flask server...")
        app.run(
            host='0.0.0.0',  # Override to bind to all interfaces
            port=config.PORT,
            debug=config.DEBUG,
            threaded=True,
            use_reloader=False  # Disable reloader in production
        )
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Application startup failed: {str(e)}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("Application stopped")


if __name__ == '__main__':
    main() 