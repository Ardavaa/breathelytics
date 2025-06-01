"""
Breathelytics Flask API Server

A Flask-based REST API for respiratory sound analysis and disease prediction.
Integrates with the ML pipeline for real-time audio processing and classification.
"""

import os
import logging
import tempfile
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest, InternalServerError
import pandas as pd

from pipeline import predict_respiratory_condition, create_respiratory_pipeline
from models import PredictionRequest, PredictionResponse, HealthCheckResponse
from utils import setup_logging, validate_audio_file, cleanup_temp_files
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for frontend integration
CORS(app, resources={
    r"/api/*": {
        "origins": "*",  # Allow all origins for development
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Setup logging
logger = setup_logging()

# Global variables for pipeline caching
_preprocessing_pipeline = None
_model_loaded = False


def get_preprocessing_pipeline():
    """Get or create the preprocessing pipeline (singleton pattern)."""
    global _preprocessing_pipeline
    if _preprocessing_pipeline is None:
        logger.info("Initializing preprocessing pipeline...")
        _preprocessing_pipeline = create_respiratory_pipeline()
    return _preprocessing_pipeline


@app.route('/api/health', methods=['GET'])
def health_check() -> Dict[str, Any]:
    """
    Health check endpoint to verify API status and model availability.
    
    Returns:
        Dict[str, Any]: Health status information
    """
    try:
        model_path = os.path.join(app.config['MODEL_DIR'], 'respiratory_classifier.pkl')
        model_exists = os.path.exists(model_path)
        
        pipeline_status = "loaded" if _preprocessing_pipeline is not None else "not_loaded"
        
        response = HealthCheckResponse(
            status="healthy",
            timestamp=datetime.utcnow().isoformat(),
            version=app.config['VERSION'],
            model_available=model_exists,
            pipeline_status=pipeline_status
        )
        
        return jsonify(response.dict()), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500


@app.route('/api/predict', methods=['POST'])
def predict_respiratory_disease() -> Dict[str, Any]:
    """
    Main prediction endpoint for respiratory disease detection.
    
    Expects a multipart/form-data request with an audio file.
    
    Returns:
        Dict[str, Any]: Prediction results with probabilities and metadata
    """
    temp_file_path = None
    
    try:
        # Validate request
        if 'audio' not in request.files:
            raise BadRequest("No audio file provided in request")
        
        file = request.files['audio']
        if file.filename == '':
            raise BadRequest("No file selected")
        
        # Validate audio file
        if not validate_audio_file(file):
            raise BadRequest("Invalid audio file format. Please upload WAV, MP3, or FLAC files.")
        
        # Create temporary file
        temp_dir = app.config['TEMP_DIR']
        os.makedirs(temp_dir, exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(secure_filename(file.filename))[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        temp_file_path = os.path.join(temp_dir, unique_filename)
        
        # Save uploaded file
        file.save(temp_file_path)
        logger.info(f"Saved uploaded file to: {temp_file_path}")
        
        # Validate file size
        file_size = os.path.getsize(temp_file_path)
        if file_size > app.config['MAX_FILE_SIZE']:
            raise BadRequest(f"File too large. Maximum size: {app.config['MAX_FILE_SIZE']} bytes")
        
        # Get model path
        model_path = os.path.join(app.config['MODEL_DIR'], 'respiratory_classifier.pkl')
        
        # Make prediction
        logger.info("Starting prediction process...")
        prediction_result = predict_respiratory_condition(temp_file_path, model_path)
        
        # Create response
        response = PredictionResponse(
            prediction=prediction_result['prediction'],
            confidence=float(prediction_result['probability']),
            all_probabilities=prediction_result['all_probabilities'],
            prediction_code=int(prediction_result['prediction_code']),
            timestamp=datetime.utcnow().isoformat(),
            file_info={
                "original_filename": secure_filename(file.filename),
                "file_size": file_size,
                "processing_time_ms": 0  # Will be calculated later
            }
        )
        
        logger.info(f"Prediction completed: {prediction_result['prediction']} "
                   f"(confidence: {prediction_result['probability']:.2%})")
        
        return jsonify(response.dict()), 200
        
    except BadRequest as e:
        logger.warning(f"Bad request: {str(e)}")
        return jsonify({
            "error": "Invalid request",
            "message": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 400
        
    except FileNotFoundError as e:
        logger.error(f"Model file not found: {str(e)}")
        return jsonify({
            "error": "Model not available",
            "message": "Prediction model not found. Please contact system administrator.",
            "timestamp": datetime.utcnow().isoformat()
        }), 503
        
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Prediction failed",
            "message": "An error occurred during prediction. Please try again.",
            "timestamp": datetime.utcnow().isoformat()
        }), 500
        
    finally:
        # Cleanup temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                logger.debug(f"Cleaned up temporary file: {temp_file_path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temporary file {temp_file_path}: {str(e)}")


@app.route('/api/diseases', methods=['GET'])
def get_disease_info() -> Dict[str, Any]:
    """
    Get information about detectable respiratory diseases.
    
    Returns:
        Dict[str, Any]: List of diseases with descriptions and symptoms
    """
    try:
        diseases = [
            {
                "name": "Asthma",
                "description": "A respiratory condition where airways narrow and swell, producing extra mucus.",
                "symptoms": ["Shortness of breath", "Chest tightness", "Wheezing", "Coughing"],
                "severity": "Moderate"
            },
            {
                "name": "Bronchiectasis", 
                "description": "A condition where the bronchi are abnormally widened and thickened.",
                "symptoms": ["Persistent cough", "Daily sputum production", "Shortness of breath"],
                "severity": "Severe"
            },
            {
                "name": "Bronchiolitis",
                "description": "Inflammation of the small airways in the lungs.",
                "symptoms": ["Cough", "Wheezing", "Shortness of breath", "Fever"],
                "severity": "Mild to Moderate"
            },
            {
                "name": "COPD",
                "description": "Chronic Obstructive Pulmonary Disease - progressive lung disease.",
                "symptoms": ["Chronic cough", "Shortness of breath", "Excessive mucus"],
                "severity": "Severe"
            },
            {
                "name": "Healthy",
                "description": "Normal respiratory function with no detected abnormalities.",
                "symptoms": ["None"],
                "severity": "None"
            },
            {
                "name": "LRTI",
                "description": "Lower Respiratory Tract Infection affecting lungs and airways.",
                "symptoms": ["Productive cough", "Fever", "Shortness of breath"],
                "severity": "Moderate"
            },
            {
                "name": "Pneumonia",
                "description": "Infection that inflames air sacs in one or both lungs.",
                "symptoms": ["Cough with phlegm", "Fever", "Chills", "Difficulty breathing"],
                "severity": "Severe"
            },
            {
                "name": "URTI",
                "description": "Upper Respiratory Tract Infection affecting nose, throat, and sinuses.",
                "symptoms": ["Runny nose", "Sore throat", "Cough", "Sneezing"],
                "severity": "Mild"
            }
        ]
        
        return jsonify({
            "diseases": diseases,
            "total_count": len(diseases),
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to get disease info: {str(e)}")
        return jsonify({
            "error": "Failed to retrieve disease information",
            "timestamp": datetime.utcnow().isoformat()
        }), 500


@app.route('/api/pipeline/status', methods=['GET'])
def get_pipeline_status() -> Dict[str, Any]:
    """
    Get current status of the ML pipeline.
    
    Returns:
        Dict[str, Any]: Pipeline status and configuration
    """
    try:
        pipeline = get_preprocessing_pipeline()
        
        return jsonify({
            "pipeline_loaded": pipeline is not None,
            "target_duration": 7.8560090702947845,
            "excluded_features": ['mel_spectrogram_min', 'chroma_stft_max'],
            "steps": [
                "AudioLoader",
                "AudioTrimmer", 
                "FeatureExtractor",
                "FeatureStatisticsCalculator"
            ],
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to get pipeline status: {str(e)}")
        return jsonify({
            "error": "Failed to retrieve pipeline status",
            "timestamp": datetime.utcnow().isoformat()
        }), 500


@app.errorhandler(404)
def not_found(error) -> Dict[str, Any]:
    """Handle 404 errors."""
    return jsonify({
        "error": "Not found",
        "message": "The requested endpoint does not exist",
        "timestamp": datetime.utcnow().isoformat()
    }), 404


@app.errorhandler(405)
def method_not_allowed(error) -> Dict[str, Any]:
    """Handle 405 errors."""
    return jsonify({
        "error": "Method not allowed",
        "message": "The requested method is not allowed for this endpoint",
        "timestamp": datetime.utcnow().isoformat()
    }), 405


@app.errorhandler(500)
def internal_error(error) -> Dict[str, Any]:
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred",
        "timestamp": datetime.utcnow().isoformat()
    }), 500


if __name__ == '__main__':
    # Initialize pipeline on startup
    try:
        get_preprocessing_pipeline()
        logger.info("Preprocessing pipeline initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize pipeline: {str(e)}")
    
    # Run the application
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    ) 