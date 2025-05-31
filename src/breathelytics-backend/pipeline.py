"""
Respiratory Sound Analysis Pipeline

Enhanced ML pipeline for preprocessing respiratory audio and predicting diseases.
Includes comprehensive feature extraction and statistical analysis.
"""

import os
import time
from typing import Dict, Any, List, Optional, Union, Tuple
import numpy as np
import pandas as pd
import librosa
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
import joblib
import logging

logger = logging.getLogger('breathelytics')


class AudioLoader(BaseEstimator, TransformerMixin):
    """
    Custom transformer to load audio files and extract basic properties.
    
    Loads audio files using librosa and prepares them for further processing.
    """
    
    def __init__(self, sample_rate: Optional[int] = None, mono: bool = True) -> None:
        """
        Initialize AudioLoader.
        
        Args:
            sample_rate: Target sample rate for audio loading
            mono: Whether to convert to mono audio
        """
        self.sample_rate = sample_rate
        self.mono = mono
    
    def fit(self, X: Any, y: Optional[Any] = None) -> 'AudioLoader':
        """Fit method (no-op for transformers)."""
        return self
    
    def transform(self, X: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Load audio files from a list of file paths.
        
        Args:
            X: List of file paths to audio files
            
        Returns:
            Dict containing audio data and metadata for each file
            
        Raises:
            FileNotFoundError: If audio file doesn't exist
            ValueError: If audio file cannot be loaded
        """
        result = {}
        
        for file_path in X:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Audio file not found: {file_path}")
            
            try:
                filename = os.path.basename(file_path)
                y, sr = librosa.load(
                    file_path, 
                    sr=self.sample_rate, 
                    mono=self.mono
                )
                
                result[filename] = {
                    'data': y,
                    'sample_rate': sr,
                    'original_path': file_path,
                    'duration': len(y) / sr
                }
                
                logger.debug(f"Loaded audio file: {filename}, duration: {len(y) / sr:.2f}s")
                
            except Exception as e:
                logger.error(f"Failed to load audio file {file_path}: {str(e)}")
                raise ValueError(f"Cannot load audio file {file_path}: {str(e)}")
        
        return result


class AudioTrimmer(BaseEstimator, TransformerMixin):
    """
    Custom transformer to trim audio to consistent duration.
    
    Ensures all audio samples have the same duration for consistent feature extraction.
    """
    
    def __init__(self, target_duration: float = 7.8560090702947845) -> None:
        """
        Initialize AudioTrimmer.
        
        Args:
            target_duration: Target duration in seconds
        """
        self.target_duration = target_duration
    
    def fit(self, X: Any, y: Optional[Any] = None) -> 'AudioTrimmer':
        """Fit method (no-op for transformers)."""
        return self
    
    def transform(self, X: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Trim audio files to consistent duration.
        
        Args:
            X: Dictionary containing audio data from AudioLoader
            
        Returns:
            Dict containing trimmed audio data
        """
        trimmed = {}
        
        for filename, audio_info in X.items():
            sample_rate = audio_info['sample_rate']
            target_samples = int(self.target_duration * sample_rate)
            
            # Trim or pad audio to target length
            if len(audio_info['data']) < target_samples:
                # Pad with zeros if too short
                trimmed_data = np.pad(
                    audio_info['data'], 
                    (0, target_samples - len(audio_info['data'])), 
                    'constant'
                )
                logger.debug(f"Padded audio {filename} from {len(audio_info['data'])} to {target_samples} samples")
            else:
                # Trim if too long
                trimmed_data = audio_info['data'][:target_samples]
                logger.debug(f"Trimmed audio {filename} from {len(audio_info['data'])} to {target_samples} samples")
            
            trimmed[filename] = {
                'data': trimmed_data,
                'sample_rate': sample_rate,
                'duration': self.target_duration,
                'original_duration': audio_info.get('duration', 0)
            }
        
        return trimmed


class FeatureExtractor(BaseEstimator, TransformerMixin):
    """
    Custom transformer to extract comprehensive audio features.
    
    Extracts multiple types of audio features including spectral and temporal characteristics.
    """
    
    def __init__(self, n_mfcc: int = 13) -> None:
        """
        Initialize FeatureExtractor.
        
        Args:
            n_mfcc: Number of MFCC coefficients to extract
        """
        self.n_mfcc = n_mfcc
    
    def fit(self, X: Any, y: Optional[Any] = None) -> 'FeatureExtractor':
        """Fit method (no-op for transformers)."""
        return self
    
    def transform(self, X: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, np.ndarray]]:
        """
        Extract comprehensive audio features.
        
        Args:
            X: Dictionary containing trimmed audio data
            
        Returns:
            Dict containing extracted features for each audio file
        """
        features = {}
        
        for filename, audio_info in X.items():
            y_audio = audio_info['data']
            sr = audio_info['sample_rate']
            
            try:
                start_time = time.time()
                
                file_features = {}
                
                # Spectral features
                file_features['chroma_stft'] = librosa.feature.chroma_stft(y=y_audio, sr=sr)
                file_features['mfcc'] = librosa.feature.mfcc(y=y_audio, sr=sr, n_mfcc=self.n_mfcc)
                file_features['mel_spectrogram'] = librosa.feature.melspectrogram(y=y_audio, sr=sr)
                file_features['spectral_contrast'] = librosa.feature.spectral_contrast(y=y_audio, sr=sr)
                file_features['spectral_centroid'] = librosa.feature.spectral_centroid(y=y_audio, sr=sr)
                file_features['spectral_bandwidth'] = librosa.feature.spectral_bandwidth(y=y_audio, sr=sr)
                file_features['spectral_rolloff'] = librosa.feature.spectral_rolloff(y=y_audio, sr=sr)
                
                # Temporal features
                file_features['zero_crossing_rate'] = librosa.feature.zero_crossing_rate(y=y_audio)
                
                features[filename] = file_features
                
                extraction_time = time.time() - start_time
                logger.debug(f"Feature extraction for {filename} completed in {extraction_time:.2f}s")
                
            except Exception as e:
                logger.error(f"Feature extraction failed for {filename}: {str(e)}")
                raise ValueError(f"Feature extraction failed for {filename}: {str(e)}")
        
        return features


class FeatureStatisticsCalculator(BaseEstimator, TransformerMixin):
    """
    Custom transformer to calculate statistical measures of extracted features.
    
    Computes mean, std, max, and min for each feature type.
    """
    
    def __init__(self, excluded_features: Optional[List[str]] = None) -> None:
        """
        Initialize FeatureStatisticsCalculator.
        
        Args:
            excluded_features: List of feature names to exclude from final dataset
        """
        self.excluded_features = excluded_features or []
    
    def fit(self, X: Any, y: Optional[Any] = None) -> 'FeatureStatisticsCalculator':
        """Fit method (no-op for transformers)."""
        return self
    
    def transform(self, X: Dict[str, Dict[str, np.ndarray]]) -> pd.DataFrame:
        """
        Calculate statistics for each feature.
        
        Args:
            X: Dictionary containing extracted features
            
        Returns:
            DataFrame with statistical measures for all features
        """
        feature_stats = []
        
        for filename, features in X.items():
            file_stats = {'filename': filename}
            
            for feature_name, feature_data in features.items():
                # Calculate statistical measures
                file_stats[f'{feature_name}_mean'] = np.mean(feature_data)
                file_stats[f'{feature_name}_std'] = np.std(feature_data)
                file_stats[f'{feature_name}_max'] = np.max(feature_data)
                file_stats[f'{feature_name}_min'] = np.min(feature_data)
            
            feature_stats.append(file_stats)
        
        # Create DataFrame
        df = pd.DataFrame(feature_stats)
        
        # Exclude specified features
        for feature in self.excluded_features:
            if feature in df.columns:
                df = df.drop(feature, axis=1)
                logger.debug(f"Excluded feature: {feature}")
        
        # Keep only numeric columns for prediction
        numeric_df = df.select_dtypes(exclude=['object'])
        
        logger.info(f"Feature statistics calculated. Shape: {numeric_df.shape}")
        return numeric_df


def create_respiratory_pipeline(
    target_duration: float = 7.8560090702947845,
    excluded_features: Optional[List[str]] = None
) -> Pipeline:
    """
    Create a comprehensive pipeline for respiratory sound classification.
    
    Args:
        target_duration: Target audio duration in seconds
        excluded_features: Features to exclude from processing
        
    Returns:
        Pipeline: Configured scikit-learn pipeline
    """
    if excluded_features is None:
        excluded_features = ['mel_spectrogram_min', 'chroma_stft_max']
    
    pipeline = Pipeline([
        ('load_audio', AudioLoader()),
        ('trim_audio', AudioTrimmer(target_duration=target_duration)),
        ('extract_features', FeatureExtractor()),
        ('calculate_statistics', FeatureStatisticsCalculator(excluded_features=excluded_features))
    ])
    
    logger.info(f"Created respiratory pipeline with {len(pipeline.steps)} steps")
    return pipeline


def predict_respiratory_condition(
    wav_file_path: str, 
    model_path: str = 'respiratory_classifier.pkl'
) -> Dict[str, Any]:
    """
    Predict respiratory condition from a WAV file using a saved model.
    
    Args:
        wav_file_path: Path to the WAV audio file
        model_path: Path to the saved ML model
        
    Returns:
        Dict containing prediction results and probabilities
        
    Raises:
        FileNotFoundError: If model or audio file doesn't exist
        ValueError: If prediction fails
    """
    start_time = time.time()
    
    # Validate inputs
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file {model_path} not found")
    
    if not os.path.exists(wav_file_path):
        raise FileNotFoundError(f"Audio file {wav_file_path} not found")
    
    try:
        # Load the saved model
        logger.info(f"Loading model from: {model_path}")
        model = joblib.load(model_path)
        
        # Create preprocessing pipeline
        preprocessing_pipeline = create_respiratory_pipeline()
        
        # Process the audio file
        logger.info(f"Processing audio file: {wav_file_path}")
        features_df = preprocessing_pipeline.transform([wav_file_path])
        
        # Make prediction
        prediction_code = model.predict(features_df)[0]
        probabilities = model.predict_proba(features_df)[0]
        
        # Get the class with highest probability
        max_prob = np.max(probabilities)
        
        # Map numeric predictions to original class labels
        diagnosis_labels = [
            'Asthma', 'Bronchiectasis', 'Bronchiolitis', 'COPD', 
            'Healthy', 'LRTI', 'Pneumonia', 'URTI'
        ]
        
        # Validate prediction code
        if prediction_code >= len(diagnosis_labels):
            raise ValueError(f"Invalid prediction code: {prediction_code}")
        
        prediction = diagnosis_labels[prediction_code]
        
        # Create probability dictionary
        all_probs_dict = {
            diagnosis_labels[i]: float(prob) 
            for i, prob in enumerate(probabilities)
        }
        
        processing_time = time.time() - start_time
        
        result = {
            'prediction': prediction,
            'prediction_code': int(prediction_code),
            'probability': float(max_prob),
            'all_probabilities': all_probs_dict,
            'processing_time_seconds': processing_time,
            'feature_count': len(features_df.columns)
        }
        
        logger.info(f"Prediction completed: {prediction} (confidence: {max_prob:.2%}) "
                   f"in {processing_time:.2f}s")
        
        return result
        
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}", exc_info=True)
        raise ValueError(f"Prediction failed: {str(e)}")


def validate_model_compatibility(model_path: str) -> Dict[str, Any]:
    """
    Validate that the saved model is compatible with the current pipeline.
    
    Args:
        model_path: Path to the saved model
        
    Returns:
        Dict containing model validation results
        
    Raises:
        FileNotFoundError: If model file doesn't exist
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file {model_path} not found")
    
    try:
        model = joblib.load(model_path)
        
        # Check if model has required methods
        has_predict = hasattr(model, 'predict')
        has_predict_proba = hasattr(model, 'predict_proba')
        has_classes = hasattr(model, 'classes_')
        
        model_info = {
            'model_type': type(model).__name__,
            'has_predict': has_predict,
            'has_predict_proba': has_predict_proba,
            'has_classes': has_classes,
            'classes_count': len(model.classes_) if has_classes else 0,
            'is_compatible': has_predict and has_predict_proba and has_classes
        }
        
        if has_classes:
            model_info['classes'] = model.classes_.tolist()
        
        logger.info(f"Model validation completed. Compatible: {model_info['is_compatible']}")
        return model_info
        
    except Exception as e:
        logger.error(f"Model validation failed: {str(e)}")
        raise ValueError(f"Model validation failed: {str(e)}")


if __name__ == "__main__":
    # Example usage and testing
    import sys
    
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
        
        try:
            result = predict_respiratory_condition(test_file)
            print(f"Prediction: {result['prediction']}")
            print(f"Confidence: {result['probability']:.2%}")
            print(f"Processing time: {result['processing_time_seconds']:.2f}s")
            
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print("Usage: python pipeline.py <audio_file_path>")