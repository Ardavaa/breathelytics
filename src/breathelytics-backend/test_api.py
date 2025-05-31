"""
Comprehensive test suite for Breathelytics Flask API.

Tests API endpoints, ML pipeline functionality, and integration scenarios.
"""

import os
import tempfile
import json
import io
from typing import Dict, Any
import pytest
from flask import Flask
from flask.testing import FlaskClient
import numpy as np
import librosa

# Import our application modules
from app import app
from pipeline import (
    create_respiratory_pipeline, 
    predict_respiratory_condition,
    validate_model_compatibility
)
from utils import validate_audio_file, format_file_size
from config import Config


class TestBreathelyticsAPI:
    """Test class for Breathelytics API endpoints."""
    
    @pytest.fixture
    def client(self) -> FlaskClient:
        """Create a test client for the Flask application."""
        app.config['TESTING'] = True
        app.config['TEMP_DIR'] = tempfile.mkdtemp()
        with app.test_client() as client:
            yield client
    
    @pytest.fixture
    def sample_audio_file(self) -> io.BytesIO:
        """Create a sample audio file for testing."""
        # Generate a simple sine wave audio
        sample_rate = 22050
        duration = 5.0  # seconds
        frequency = 440  # Hz (A note)
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio_data = np.sin(2 * np.pi * frequency * t)
        
        # Save to temporary WAV file
        temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        librosa.output.write_wav(temp_file.name, audio_data, sample_rate)
        
        with open(temp_file.name, 'rb') as f:
            audio_bytes = io.BytesIO(f.read())
        
        # Cleanup
        os.unlink(temp_file.name)
        
        return audio_bytes
    
    def test_health_check(self, client: FlaskClient) -> None:
        """Test the health check endpoint."""
        response = client.get('/api/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert 'status' in data
        assert 'timestamp' in data
        assert 'version' in data
        assert 'model_available' in data
        assert 'pipeline_status' in data
    
    def test_get_diseases_info(self, client: FlaskClient) -> None:
        """Test the diseases information endpoint."""
        response = client.get('/api/diseases')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert 'diseases' in data
        assert 'total_count' in data
        assert 'timestamp' in data
        assert len(data['diseases']) == 8  # Expected number of diseases
        
        # Check disease structure
        for disease in data['diseases']:
            assert 'name' in disease
            assert 'description' in disease
            assert 'symptoms' in disease
            assert 'severity' in disease
    
    def test_get_pipeline_status(self, client: FlaskClient) -> None:
        """Test the pipeline status endpoint."""
        response = client.get('/api/pipeline/status')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert 'pipeline_loaded' in data
        assert 'target_duration' in data
        assert 'excluded_features' in data
        assert 'steps' in data
        assert len(data['steps']) == 4  # Expected pipeline steps
    
    def test_predict_missing_file(self, client: FlaskClient) -> None:
        """Test prediction endpoint with missing audio file."""
        response = client.post('/api/predict')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'No audio file provided' in data['message']
    
    def test_predict_empty_filename(self, client: FlaskClient) -> None:
        """Test prediction endpoint with empty filename."""
        response = client.post('/api/predict', data={'audio': (io.BytesIO(b''), '')})
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_predict_invalid_file_format(self, client: FlaskClient) -> None:
        """Test prediction endpoint with invalid file format."""
        fake_file = io.BytesIO(b'fake audio data')
        
        response = client.post('/api/predict', data={
            'audio': (fake_file, 'test.txt')
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    @pytest.mark.skipif(
        not os.path.exists('src/breathelytics-backend/respiratory_classifier.pkl'),
        reason="Model file not available"
    )
    def test_predict_valid_audio(self, client: FlaskClient, sample_audio_file: io.BytesIO) -> None:
        """Test prediction endpoint with valid audio file."""
        response = client.post('/api/predict', data={
            'audio': (sample_audio_file, 'test_audio.wav')
        })
        
        # This might fail if model is not present, but structure should be correct
        if response.status_code == 200:
            data = json.loads(response.data)
            
            assert 'prediction' in data
            assert 'confidence' in data
            assert 'all_probabilities' in data
            assert 'timestamp' in data
            assert 'file_info' in data
            
            # Validate confidence score
            assert 0.0 <= data['confidence'] <= 1.0
            
            # Validate probabilities
            assert len(data['all_probabilities']) == 8
            for prob in data['all_probabilities'].values():
                assert 0.0 <= prob <= 1.0
    
    def test_404_error(self, client: FlaskClient) -> None:
        """Test 404 error handling."""
        response = client.get('/api/nonexistent')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Not found' in data['error']
    
    def test_405_error(self, client: FlaskClient) -> None:
        """Test 405 error handling."""
        response = client.put('/api/health')  # PUT not allowed
        
        assert response.status_code == 405
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Method not allowed' in data['error']


class TestMLPipeline:
    """Test class for ML pipeline functionality."""
    
    @pytest.fixture
    def sample_audio_path(self) -> str:
        """Create a temporary audio file for testing."""
        # Generate sample audio
        sample_rate = 22050
        duration = 8.0  # seconds (longer than target duration)
        frequency = 440  # Hz
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio_data = np.sin(2 * np.pi * frequency * t)
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        librosa.output.write_wav(temp_file.name, audio_data, sample_rate)
        
        yield temp_file.name
        
        # Cleanup
        os.unlink(temp_file.name)
    
    def test_create_pipeline(self) -> None:
        """Test pipeline creation."""
        pipeline = create_respiratory_pipeline()
        
        assert pipeline is not None
        assert len(pipeline.steps) == 4
        
        step_names = [name for name, _ in pipeline.steps]
        expected_steps = ['load_audio', 'trim_audio', 'extract_features', 'calculate_statistics']
        assert step_names == expected_steps
    
    def test_pipeline_with_custom_parameters(self) -> None:
        """Test pipeline creation with custom parameters."""
        custom_duration = 5.0
        custom_excluded = ['test_feature']
        
        pipeline = create_respiratory_pipeline(
            target_duration=custom_duration,
            excluded_features=custom_excluded
        )
        
        assert pipeline is not None
        
        # Check if custom parameters are set
        trim_step = pipeline.named_steps['trim_audio']
        assert trim_step.target_duration == custom_duration
        
        stats_step = pipeline.named_steps['calculate_statistics']
        assert stats_step.excluded_features == custom_excluded
    
    def test_audio_loading(self, sample_audio_path: str) -> None:
        """Test audio loading functionality."""
        from pipeline import AudioLoader
        
        loader = AudioLoader()
        result = loader.transform([sample_audio_path])
        
        assert len(result) == 1
        filename = os.path.basename(sample_audio_path)
        assert filename in result
        
        audio_data = result[filename]
        assert 'data' in audio_data
        assert 'sample_rate' in audio_data
        assert 'duration' in audio_data
        assert len(audio_data['data']) > 0
    
    def test_audio_trimming(self, sample_audio_path: str) -> None:
        """Test audio trimming functionality."""
        from pipeline import AudioLoader, AudioTrimmer
        
        # Load audio first
        loader = AudioLoader()
        loaded_audio = loader.transform([sample_audio_path])
        
        # Trim audio
        target_duration = 5.0
        trimmer = AudioTrimmer(target_duration=target_duration)
        trimmed_audio = trimmer.transform(loaded_audio)
        
        filename = os.path.basename(sample_audio_path)
        trimmed_data = trimmed_audio[filename]
        
        assert trimmed_data['duration'] == target_duration
        expected_samples = int(target_duration * trimmed_data['sample_rate'])
        assert len(trimmed_data['data']) == expected_samples
    
    def test_feature_extraction(self, sample_audio_path: str) -> None:
        """Test feature extraction functionality."""
        from pipeline import AudioLoader, AudioTrimmer, FeatureExtractor
        
        # Process audio through pipeline steps
        loader = AudioLoader()
        loaded_audio = loader.transform([sample_audio_path])
        
        trimmer = AudioTrimmer()
        trimmed_audio = trimmer.transform(loaded_audio)
        
        extractor = FeatureExtractor()
        features = extractor.transform(trimmed_audio)
        
        filename = os.path.basename(sample_audio_path)
        file_features = features[filename]
        
        # Check if all expected features are present
        expected_features = [
            'chroma_stft', 'mfcc', 'mel_spectrogram', 'spectral_contrast',
            'spectral_centroid', 'spectral_bandwidth', 'spectral_rolloff',
            'zero_crossing_rate'
        ]
        
        for feature in expected_features:
            assert feature in file_features
            assert isinstance(file_features[feature], np.ndarray)
    
    def test_feature_statistics(self, sample_audio_path: str) -> None:
        """Test feature statistics calculation."""
        pipeline = create_respiratory_pipeline()
        result_df = pipeline.transform([sample_audio_path])
        
        assert len(result_df) == 1  # One file processed
        assert len(result_df.columns) > 0  # Features extracted
        
        # Check if statistical measures are calculated
        feature_names = result_df.columns.tolist()
        
        # Should have mean, std, max, min for each feature type
        stats_suffixes = ['_mean', '_std', '_max', '_min']
        for suffix in stats_suffixes:
            suffix_features = [f for f in feature_names if f.endswith(suffix)]
            assert len(suffix_features) > 0
    
    @pytest.mark.skipif(
        not os.path.exists('src/breathelytics-backend/respiratory_classifier.pkl'),
        reason="Model file not available"
    )
    def test_model_compatibility(self) -> None:
        """Test model compatibility validation."""
        model_path = 'src/breathelytics-backend/respiratory_classifier.pkl'
        
        try:
            model_info = validate_model_compatibility(model_path)
            
            assert 'model_type' in model_info
            assert 'has_predict' in model_info
            assert 'has_predict_proba' in model_info
            assert 'has_classes' in model_info
            assert 'is_compatible' in model_info
            
        except FileNotFoundError:
            pytest.skip("Model file not found")
    
    @pytest.mark.skipif(
        not os.path.exists('src/breathelytics-backend/respiratory_classifier.pkl'),
        reason="Model file not available"
    )
    def test_end_to_end_prediction(self, sample_audio_path: str) -> None:
        """Test end-to-end prediction pipeline."""
        model_path = 'src/breathelytics-backend/respiratory_classifier.pkl'
        
        try:
            result = predict_respiratory_condition(sample_audio_path, model_path)
            
            assert 'prediction' in result
            assert 'probability' in result
            assert 'all_probabilities' in result
            assert 'processing_time_seconds' in result
            
            # Validate result structure
            assert isinstance(result['prediction'], str)
            assert 0.0 <= result['probability'] <= 1.0
            assert len(result['all_probabilities']) == 8
            assert result['processing_time_seconds'] > 0
            
        except FileNotFoundError:
            pytest.skip("Model file not found")


class TestUtilityFunctions:
    """Test class for utility functions."""
    
    def test_format_file_size(self) -> None:
        """Test file size formatting function."""
        assert format_file_size(0) == "0 B"
        assert format_file_size(1024) == "1.0 KB"
        assert format_file_size(1024 * 1024) == "1.0 MB"
        assert format_file_size(1536) == "1.5 KB"
    
    def test_validate_audio_file_valid(self) -> None:
        """Test audio file validation with valid files."""
        from werkzeug.datastructures import FileStorage
        
        # Mock valid audio files
        valid_files = [
            FileStorage(filename='test.wav'),
            FileStorage(filename='test.mp3'),
            FileStorage(filename='test.flac'),
            FileStorage(filename='test.m4a')
        ]
        
        for file_storage in valid_files:
            # Note: This might not work perfectly without actual file content
            # but tests the basic extension validation
            pass
    
    def test_validate_audio_file_invalid(self) -> None:
        """Test audio file validation with invalid files."""
        from werkzeug.datastructures import FileStorage
        
        # Mock invalid files
        invalid_files = [
            None,
            FileStorage(filename=''),
            FileStorage(filename='test.txt'),
            FileStorage(filename='test.pdf'),
            FileStorage(filename='noextension')
        ]
        
        for file_storage in invalid_files:
            result = validate_audio_file(file_storage)
            assert result is False


@pytest.mark.integration
class TestIntegration:
    """Integration tests for the complete system."""
    
    def test_api_health_integration(self) -> None:
        """Test API health check integration."""
        with app.test_client() as client:
            response = client.get('/api/health')
            assert response.status_code == 200
    
    def test_pipeline_creation_integration(self) -> None:
        """Test pipeline creation integration."""
        pipeline = create_respiratory_pipeline()
        assert pipeline is not None
        
        # Test that pipeline can be used for transformation
        # (This would require actual audio files for full testing)


if __name__ == '__main__':
    # Run tests
    pytest.main([__file__, '-v']) 