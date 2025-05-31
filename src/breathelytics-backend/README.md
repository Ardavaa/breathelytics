# Breathelytics Flask API Backend

A robust Flask-based REST API for respiratory sound analysis and disease prediction using machine learning.

## 🚀 Features

- **RESTful API**: Clean, documented endpoints for respiratory analysis
- **ML Pipeline**: Advanced audio processing and feature extraction
- **Disease Detection**: Classifies 8 respiratory conditions with confidence scores
- **File Validation**: Comprehensive audio file validation and security
- **Error Handling**: Robust error handling with detailed logging
- **CORS Support**: Cross-origin support for frontend integration
- **Health Monitoring**: Health check and status endpoints
- **Type Safety**: Full type annotations and Pydantic validation

## 🏗️ Architecture

```
src/breathelytics-backend/
├── app.py                 # Main Flask application
├── pipeline.py           # ML pipeline and prediction logic
├── models.py             # Pydantic data models
├── config.py             # Configuration management
├── utils.py              # Utility functions
├── test_api.py           # Comprehensive test suite
├── run.py                # Production startup script
├── requirements.txt      # Dependencies
└── respiratory_classifier.pkl  # Pre-trained ML model
```

## 📋 API Endpoints

### Health & Status
- `GET /api/health` - Health check and system status
- `GET /api/pipeline/status` - ML pipeline status and configuration

### Prediction
- `POST /api/predict` - Upload audio file for respiratory disease prediction

### Information
- `GET /api/diseases` - Get information about detectable diseases

## 🔧 Installation & Setup

### Prerequisites
- Python 3.10+
- Virtual environment (recommended)

### Installation

1. **Navigate to backend directory:**
   ```bash
   cd src/breathelytics-backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify model file:**
   ```bash
   ls -la respiratory_classifier.pkl  # Should exist (1.7MB)
   ```

## 🚀 Running the Application

### Development Mode
```bash
# Set environment variables
export FLASK_ENV=development
export FLASK_DEBUG=true

# Run the application
python run.py
```

### Production Mode
```bash
# Set environment variables
export FLASK_ENV=production
export SECRET_KEY=your-secret-key-here

# Run the application
python run.py
```

### Using Docker (Optional)
```bash
# Build image
docker build -t breathelytics-api .

# Run container
docker run -p 5000:5000 breathelytics-api
```

## 📊 API Usage Examples

### Health Check
```bash
curl -X GET http://localhost:5000/api/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "version": "1.0.0",
  "model_available": true,
  "pipeline_status": "loaded"
}
```

### Predict Respiratory Condition
```bash
curl -X POST http://localhost:5000/api/predict \
  -F "audio=@path/to/your/audio.wav"
```

Response:
```json
{
  "prediction": "Healthy",
  "confidence": 0.85,
  "prediction_code": 4,
  "all_probabilities": {
    "Asthma": 0.12,
    "Bronchiectasis": 0.03,
    "Bronchiolitis": 0.05,
    "COPD": 0.08,
    "Healthy": 0.85,
    "LRTI": 0.02,
    "Pneumonia": 0.01,
    "URTI": 0.04
  },
  "timestamp": "2024-01-01T12:00:00.000Z",
  "file_info": {
    "original_filename": "audio.wav",
    "file_size": 1048576,
    "processing_time_ms": 1250
  }
}
```

### Get Disease Information
```bash
curl -X GET http://localhost:5000/api/diseases
```

## 🔬 ML Pipeline Details

### Supported Audio Formats
- WAV (recommended)
- MP3
- FLAC
- M4A

### Feature Extraction
The pipeline extracts comprehensive audio features:
- **Spectral Features**: MFCC, Chroma STFT, Mel Spectrograms, Spectral Contrast/Centroid/Bandwidth/Rolloff
- **Temporal Features**: Zero Crossing Rate
- **Statistical Measures**: Mean, Standard Deviation, Min, Max for each feature

### Preprocessing Steps
1. **Audio Loading**: Load audio with librosa
2. **Audio Trimming**: Normalize to 7.856 seconds duration
3. **Feature Extraction**: Extract multiple audio features
4. **Statistical Calculation**: Compute statistical measures
5. **Prediction**: Classify using pre-trained model

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest test_api.py -v

# Run specific test class
pytest test_api.py::TestBreathelyticsAPI -v

# Run with coverage
pytest test_api.py --cov=.
```

### Test Categories
- **API Tests**: Endpoint functionality and error handling
- **Pipeline Tests**: ML pipeline components and integration
- **Utility Tests**: Helper function validation
- **Integration Tests**: End-to-end system testing

## ⚙️ Configuration

### Environment Variables
```bash
# Server Configuration
FLASK_ENV=development|production
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
FLASK_DEBUG=true|false

# Security
SECRET_KEY=your-secret-key

# Directories
TEMP_DIR=/path/to/temp
LOGS_DIR=/path/to/logs

# Logging
LOG_LEVEL=DEBUG|INFO|WARNING|ERROR
```

### Configuration Files
- `config.py`: Application configuration classes
- Development, Testing, and Production configurations available

## 📝 Logging

The application provides comprehensive logging:
- **File Logging**: Logs to `logs/breathelytics_api.log`
- **Console Logging**: Real-time console output
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Structured Logging**: Consistent format with timestamps

## 🚨 Error Handling

### HTTP Status Codes
- `200`: Successful prediction
- `400`: Bad request (invalid file, missing parameters)
- `404`: Endpoint not found
- `405`: Method not allowed
- `500`: Internal server error
- `503`: Service unavailable (model not loaded)

### Error Response Format
```json
{
  "error": "Error type",
  "message": "Detailed error message",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

## 🔐 Security Features

- **File Validation**: MIME type and extension checking
- **File Size Limits**: Configurable maximum file size (default 50MB)
- **Secure Filenames**: Sanitized temporary file handling
- **CORS Configuration**: Controlled cross-origin access
- **Input Validation**: Pydantic models for request/response validation

## 📊 Performance

### Optimization Features
- **Pipeline Caching**: Singleton pattern for ML pipeline
- **Async Support**: Ready for async processing
- **Memory Management**: Automatic temporary file cleanup
- **Error Recovery**: Graceful degradation when model unavailable

### Benchmarks
- **Audio Processing**: ~1-3 seconds for 8-second audio file
- **Memory Usage**: ~100-200MB baseline
- **Throughput**: ~10-20 requests/minute (single-threaded)

## 🐛 Troubleshooting

### Common Issues

1. **Model File Missing**
   ```
   Error: Model file respiratory_classifier.pkl not found
   Solution: Ensure model file exists in backend directory
   ```

2. **Audio Processing Errors**
   ```
   Error: Feature extraction failed
   Solution: Check audio file format and quality
   ```

3. **Memory Issues**
   ```
   Error: Out of memory during processing
   Solution: Reduce file size or increase system memory
   ```

### Debug Mode
Enable debug logging for detailed troubleshooting:
```bash
export LOG_LEVEL=DEBUG
python run.py
```

## 🤝 Contributing

1. Follow Python coding standards (PEP 8)
2. Add type annotations to all functions
3. Write comprehensive docstrings (Google style)
4. Include tests for new functionality
5. Update documentation for API changes

## 📄 License

This project is part of the Breathelytics application for respiratory health analysis.

---

For more information, see the main project README or contact the development team. 