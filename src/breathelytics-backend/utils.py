"""
Utility functions for the Breathelytics backend.

Provides helper functions for logging, file validation, and system operations.
"""

import os
import logging
from pathlib import Path
from typing import Optional
from werkzeug.datastructures import FileStorage


def setup_logging(log_level: str = 'INFO') -> logging.Logger:
    """
    Setup logging configuration for the application.
    
    Args:
        log_level: Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR')
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Setup file handler for API logs
    file_handler = logging.FileHandler(log_dir / 'breathelytics_api.log')
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(detailed_formatter)
    
    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(simple_formatter)
    
    # Configure root logger
    logger = logging.getLogger('breathelytics')
    logger.setLevel(numeric_level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Prevent duplicate logs
    logger.propagate = False
    
    return logger


def validate_audio_file(file: FileStorage) -> bool:
    """
    Validate uploaded audio file format and basic properties.
    
    Args:
        file: Uploaded file from Flask request
        
    Returns:
        bool: True if file is valid, False otherwise
    """
    if not file or not file.filename:
        return False
    
    # Check file extension
    allowed_extensions = {'.wav', '.mp3', '.flac', '.m4a'}
    file_extension = Path(file.filename).suffix.lower()
    
    if file_extension not in allowed_extensions:
        return False
    
    # Basic content type check (if available)
    if file.content_type:
        allowed_mimes = {
            'audio/wav', 'audio/wave', 'audio/x-wav',
            'audio/mpeg', 'audio/mp3',
            'audio/flac', 'audio/x-flac',
            'audio/mp4', 'audio/m4a'
        }
        if file.content_type not in allowed_mimes:
            return False
    
    return True


def cleanup_temp_files(temp_dir: str, max_age_hours: int = 24) -> int:
    """
    Clean up old temporary files.
    
    Args:
        temp_dir: Directory containing temporary files
        max_age_hours: Maximum age of files to keep (in hours)
        
    Returns:
        int: Number of files cleaned up
    """
    import time
    
    if not os.path.exists(temp_dir):
        return 0
    
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    cleaned_count = 0
    
    try:
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            
            if os.path.isfile(file_path):
                file_age = current_time - os.path.getmtime(file_path)
                
                if file_age > max_age_seconds:
                    os.remove(file_path)
                    cleaned_count += 1
                    
    except Exception as e:
        logger = logging.getLogger('breathelytics')
        logger.warning(f"Error during temp file cleanup: {str(e)}")
    
    return cleaned_count 