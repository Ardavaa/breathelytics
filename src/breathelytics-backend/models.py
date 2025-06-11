"""
Pydantic models for request/response validation in Breathelytics API.

Defines data models for API requests, responses, and internal data structures.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field, validator


class PredictionRequest(BaseModel):
    """Model for prediction request data."""
    
    file_data: bytes = Field(..., description="Audio file binary data")
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., gt=0, description="File size in bytes")
    
    @validator('filename')
    def validate_filename(cls, v: str) -> str:
        """Validate filename has proper extension."""
        allowed_extensions = ['.wav', '.mp3', '.flac', '.m4a']
        if not any(v.lower().endswith(ext) for ext in allowed_extensions):
            raise ValueError(f"File must have one of these extensions: {allowed_extensions}")
        return v


class PredictionResponse(BaseModel):
    """Model for prediction response data."""
    
    prediction: str = Field(..., description="Predicted respiratory condition")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Prediction confidence score")
    prediction_code: int = Field(..., ge=0, description="Numeric prediction code")
    all_probabilities: Dict[str, float] = Field(..., description="Probabilities for all conditions")
    timestamp: str = Field(..., description="Prediction timestamp in ISO format")
    file_info: Dict[str, Any] = Field(..., description="Information about processed file")
    
    @validator('all_probabilities')
    def validate_probabilities(cls, v: Dict[str, float]) -> Dict[str, float]:
        """Validate that all probabilities are between 0 and 1."""
        for condition, prob in v.items():
            if not (0.0 <= prob <= 1.0):
                raise ValueError(f"Probability for {condition} must be between 0 and 1")
        return v


class HealthCheckResponse(BaseModel):
    """Model for health check response."""
    
    status: str = Field(..., description="Service health status")
    timestamp: str = Field(..., description="Health check timestamp")
    version: str = Field(..., description="API version")
    model_available: bool = Field(..., description="Whether ML model is available")
    pipeline_status: str = Field(..., description="ML pipeline status")


class DiseaseInfo(BaseModel):
    """Model for disease information."""
    
    name: str = Field(..., description="Disease name")
    description: str = Field(..., description="Disease description")
    symptoms: List[str] = Field(..., description="Common symptoms")
    severity: str = Field(..., description="Disease severity level")


class DiseasesResponse(BaseModel):
    """Model for diseases information response."""
    
    diseases: List[DiseaseInfo] = Field(..., description="List of detectable diseases")
    total_count: int = Field(..., ge=0, description="Total number of diseases")
    timestamp: str = Field(..., description="Response timestamp")


class PipelineStatus(BaseModel):
    """Model for ML pipeline status."""
    
    pipeline_loaded: bool = Field(..., description="Whether pipeline is loaded")
    target_duration: float = Field(..., gt=0, description="Target audio duration in seconds")
    excluded_features: List[str] = Field(..., description="Features excluded from processing")
    steps: List[str] = Field(..., description="Pipeline processing steps")
    timestamp: str = Field(..., description="Status timestamp")


class ErrorResponse(BaseModel):
    """Model for error responses."""
    
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    timestamp: str = Field(..., description="Error timestamp")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")


class AudioFeatures(BaseModel):
    """Model for extracted audio features."""
    
    chroma_stft_mean: float = Field(..., description="Chroma STFT mean")
    chroma_stft_std: float = Field(..., description="Chroma STFT standard deviation")
    chroma_stft_min: float = Field(..., description="Chroma STFT minimum")
    chroma_stft_max: float = Field(..., description="Chroma STFT maximum")
    
    mfcc_mean: float = Field(..., description="MFCC mean")
    mfcc_std: float = Field(..., description="MFCC standard deviation")
    mfcc_min: float = Field(..., description="MFCC minimum")
    mfcc_max: float = Field(..., description="MFCC maximum")
    
    mel_spectrogram_mean: float = Field(..., description="Mel spectrogram mean")
    mel_spectrogram_std: float = Field(..., description="Mel spectrogram standard deviation")
    mel_spectrogram_min: float = Field(..., description="Mel spectrogram minimum")
    mel_spectrogram_max: float = Field(..., description="Mel spectrogram maximum")
    
    spectral_contrast_mean: float = Field(..., description="Spectral contrast mean")
    spectral_contrast_std: float = Field(..., description="Spectral contrast standard deviation")
    spectral_contrast_min: float = Field(..., description="Spectral contrast minimum")
    spectral_contrast_max: float = Field(..., description="Spectral contrast maximum")
    
    spectral_centroid_mean: float = Field(..., description="Spectral centroid mean")
    spectral_centroid_std: float = Field(..., description="Spectral centroid standard deviation")
    spectral_centroid_min: float = Field(..., description="Spectral centroid minimum")
    spectral_centroid_max: float = Field(..., description="Spectral centroid maximum")
    
    spectral_bandwidth_mean: float = Field(..., description="Spectral bandwidth mean")
    spectral_bandwidth_std: float = Field(..., description="Spectral bandwidth standard deviation")
    spectral_bandwidth_min: float = Field(..., description="Spectral bandwidth minimum")
    spectral_bandwidth_max: float = Field(..., description="Spectral bandwidth maximum")
    
    spectral_rolloff_mean: float = Field(..., description="Spectral rolloff mean")
    spectral_rolloff_std: float = Field(..., description="Spectral rolloff standard deviation")
    spectral_rolloff_min: float = Field(..., description="Spectral rolloff minimum")
    spectral_rolloff_max: float = Field(..., description="Spectral rolloff maximum")
    
    zero_crossing_rate_mean: float = Field(..., description="Zero crossing rate mean")
    zero_crossing_rate_std: float = Field(..., description="Zero crossing rate standard deviation")
    zero_crossing_rate_min: float = Field(..., description="Zero crossing rate minimum")
    zero_crossing_rate_max: float = Field(..., description="Zero crossing rate maximum")


class ProcessingMetrics(BaseModel):
    """Model for processing performance metrics."""
    
    processing_time_ms: float = Field(..., ge=0, description="Total processing time in milliseconds")
    audio_duration_ms: float = Field(..., ge=0, description="Audio duration in milliseconds")
    feature_extraction_time_ms: float = Field(..., ge=0, description="Feature extraction time")
    prediction_time_ms: float = Field(..., ge=0, description="Model prediction time")
    file_size_bytes: int = Field(..., ge=0, description="File size in bytes")


class AIInsightResponse(BaseModel):
    """Model for AI-generated medical insights."""
    
    summary: str = Field(..., description="Brief summary of the analysis")
    condition_explanation: str = Field(..., description="Explanation of the detected condition")
    confidence_interpretation: str = Field(..., description="Interpretation of confidence level")
    insights: List[str] = Field(..., description="Key insights from the analysis")
    recommendations: Dict[str, List[str]] = Field(..., description="Categorized recommendations")
    risk_level: str = Field(..., description="Risk level: LOW/MODERATE/HIGH")
    next_steps: str = Field(..., description="Recommended next steps")
    disclaimer: str = Field(..., description="Medical disclaimer")
    llm_status: str = Field(..., description="LLM processing status")
    processing_time_ms: int = Field(..., description="LLM processing time in milliseconds")


class EnhancedPredictionResponse(PredictionResponse):
    """Enhanced prediction response with AI insights."""
    
    ai_insights: Optional[AIInsightResponse] = Field(None, description="AI-generated medical insights")


class DetailedPredictionResponse(PredictionResponse):
    """Extended prediction response with additional details."""
    
    features: Optional[AudioFeatures] = Field(None, description="Extracted audio features")
    metrics: Optional[ProcessingMetrics] = Field(None, description="Processing performance metrics")
    recommendations: Optional[List[str]] = Field(None, description="Health recommendations")
    confidence_interpretation: Optional[str] = Field(None, description="Confidence level interpretation")
    ai_insights: Optional[AIInsightResponse] = Field(None, description="AI-generated medical insights") 