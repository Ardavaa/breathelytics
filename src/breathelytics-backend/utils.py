"""
Utility functions for Breathelytics Flask API.

Provides logging setup, file validation, and other helper functions.
"""

import os
import logging
import mimetypes
from pathlib import Path
from typing import List, Optional, Union
from werkzeug.datastructures import FileStorage

from config import Config


def setup_logging(log_level: str = 'INFO') -> logging.Logger:
    """
    Setup application logging configuration.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    logs_dir = Config.LOGS_DIR
    os.makedirs(logs_dir, exist_ok=True)
    
    # Configure logging
    log_file = os.path.join(logs_dir, 'breathelytics_api.log')
    
    # Create formatter
    formatter = logging.Formatter(Config.LOG_FORMAT)
    
    # Setup file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, log_level.upper()))
    file_handler.setFormatter(formatter)
    
    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(formatter)
    
    # Configure main logger
    logger = logging.getLogger('breathelytics')
    logger.setLevel(getattr(logging, log_level.upper()))
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
    filename = file.filename.lower()
    allowed_extensions = Config.ALLOWED_EXTENSIONS
    
    if not any(filename.endswith(f'.{ext}') for ext in allowed_extensions):
        return False
    
    # Check MIME type
    mime_type, _ = mimetypes.guess_type(filename)
    allowed_mime_types = [
        'audio/wav', 'audio/wave', 'audio/x-wav',
        'audio/mpeg', 'audio/mp3',
        'audio/flac', 'audio/x-flac',
        'audio/mp4', 'audio/m4a'
    ]
    
    if mime_type and mime_type not in allowed_mime_types:
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


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: File size in bytes
        
    Returns:
        str: Formatted file size (e.g., "1.5 MB")
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def get_confidence_interpretation(confidence: float) -> str:
    """
    Get human-readable interpretation of confidence score.
    
    Args:
        confidence: Confidence score between 0 and 1
        
    Returns:
        str: Confidence interpretation
    """
    if confidence >= 0.9:
        return "Very High Confidence"
    elif confidence >= 0.8:
        return "High Confidence"
    elif confidence >= 0.7:
        return "Moderate Confidence"
    elif confidence >= 0.6:
        return "Low Confidence"
    else:
        return "Very Low Confidence"


def get_health_recommendations(prediction: str, confidence: float) -> List[str]:
    """
    Get health recommendations based on prediction and confidence.
    
    Args:
        prediction: Predicted respiratory condition
        confidence: Prediction confidence score
        
    Returns:
        List[str]: List of health recommendations
    """
    base_recommendations = [
        "This is an AI-powered screening tool and should not replace professional medical advice.",
        "Consult with a healthcare provider for proper diagnosis and treatment."
    ]
    
    if prediction.lower() == 'healthy':
        if confidence >= 0.8:
            recommendations = [
                "Your respiratory sounds appear normal.",
                "Continue maintaining good respiratory health with regular exercise.",
                "Monitor any changes in breathing patterns."
            ]
        else:
            recommendations = [
                "Results suggest normal respiratory function, but confidence is moderate.",
                "Consider retaking the test with a clearer audio recording.",
                "Monitor for any respiratory symptoms."
            ]
    else:
        if confidence >= 0.8:
            recommendations = [
                f"The analysis suggests possible {prediction}.",
                "We strongly recommend consulting with a healthcare provider immediately.",
                "Bring these results to your doctor for further evaluation."
            ]
        else:
            recommendations = [
                f"The analysis suggests possible {prediction}, but with moderate confidence.",
                "Consider retaking the test or consulting with a healthcare provider.",
                "Monitor your symptoms and seek medical attention if they worsen."
            ]
    
    return recommendations + base_recommendations


def validate_audio_duration(file_path: str, max_duration_seconds: float = 30.0) -> bool:
    """
    Validate audio file duration.
    
    Args:
        file_path: Path to audio file
        max_duration_seconds: Maximum allowed duration
        
    Returns:
        bool: True if duration is valid, False otherwise
    """
    try:
        import librosa
        
        # Get audio duration without loading the full audio
        duration = librosa.get_duration(path=file_path)
        return duration <= max_duration_seconds
        
    except Exception:
        # If we can't determine duration, assume it's valid
        return True


def ensure_directory_exists(directory_path: str) -> bool:
    """
    Ensure a directory exists, create if it doesn't.
    
    Args:
        directory_path: Path to directory
        
    Returns:
        bool: True if directory exists or was created successfully
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        return True
    except Exception:
        return False


def safe_filename(filename: str) -> str:
    """
    Generate a safe filename by removing/replacing unsafe characters.
    
    Args:
        filename: Original filename
        
    Returns:
        str: Safe filename
    """
    import re
    
    # Remove unsafe characters
    safe_name = re.sub(r'[^\w\-_\.]', '_', filename)
    
    # Ensure filename is not too long
    if len(safe_name) > 100:
        name, ext = os.path.splitext(safe_name)
        safe_name = name[:95] + ext
    
    return safe_name


def calculate_processing_time_ms(start_time: float, end_time: float) -> float:
    """
    Calculate processing time in milliseconds.
    
    Args:
        start_time: Start timestamp
        end_time: End timestamp
        
    Returns:
        float: Processing time in milliseconds
    """
    return (end_time - start_time) * 1000.0 