# Breathelytics Frontend - Flask API Integration

## 🎯 Overview

This frontend has been successfully integrated with the Flask backend API to provide real-time respiratory disease prediction. The integration includes comprehensive error handling, real-time updates, and a seamless user experience.

## 🔧 Files Modified/Added

### New Files
- **`api-integration.js`** - Core API communication layer
- **`test-integration.html`** - Standalone testing interface
- **`README-Integration.md`** - This documentation

### Modified Files
- **`script.js`** - Enhanced with real API calls and error handling
- **`index.html`** - Updated script includes and file input configuration

## 🚀 Features Implemented

### ✅ Real-Time API Communication
- Health check monitoring
- Automatic retry logic with exponential backoff
- Connection status indicators
- Graceful error handling

### ✅ Audio File Prediction
- Support for WAV, MP3, M4A, and FLAC formats
- File size validation (up to 50MB)
- Real-time progress tracking
- Confidence score visualization

### ✅ Enhanced User Experience
- Dynamic UI updates based on prediction results
- Detailed health recommendations
- Professional report generation
- Visual confidence indicators

### ✅ Error Handling
- Network connectivity checks
- API availability validation
- File format validation
- User-friendly error messages

## 🔗 API Endpoints Integration

### 1. Health Check (`GET /api/health`)
```javascript
const health = await BreathelyticsAPI.checkAPIHealth();
// Returns: { status, model_available, pipeline_status, version, timestamp }
```

### 2. Disease Prediction (`POST /api/predict`)
```javascript
const result = await BreathelyticsAPI.predictRespiratoryDisease(audioFile);
// Returns: { prediction, confidence, probabilities, processing_time, ... }
```

### 3. Disease Information (`GET /api/diseases`)
```javascript
const diseases = await BreathelyticsAPI.getDiseaseInfo();
// Returns: { diseases: [...], total_count, categories }
```

### 4. Pipeline Status (`GET /api/pipeline/status`)
```javascript
const status = await BreathelyticsAPI.getPipelineStatus();
// Returns: { status, components, last_updated, ... }
```

## 🎮 How to Use

### 1. Start the Flask Backend
```bash
cd src/breathelytics-backend
python run.py
```
The backend should be running on `http://localhost:5000`

### 2. Serve the Frontend
You can use any web server. For example:

```bash
cd src/breathelytics-frontend

# Using Python's built-in server
python -m http.server 8000

# Using Node.js http-server (if installed)
npx http-server -p 8000

# Using PHP (if installed)
php -S localhost:8000
```

### 3. Access the Application
- **Main Application**: `http://localhost:8000`
- **Test Interface**: `http://localhost:8000/test-integration.html`

## 🧪 Testing the Integration

### Automated Testing
Use the test interface at `test-integration.html` to verify:
1. API health and connectivity
2. Disease information retrieval
3. Pipeline status
4. Audio file prediction workflow

### Manual Testing
1. Upload an audio file through the main interface
2. Watch the real-time progress indicators
3. Verify the prediction results display correctly
4. Test the report download functionality
5. Try the "New Analysis" feature

## 📋 Prediction Workflow

```
1. User uploads audio file
   ↓
2. File validation (type, size)
   ↓
3. API connectivity check
   ↓
4. Real-time progress display
   ↓
5. API prediction call
   ↓
6. Results processing and display
   ↓
7. Report generation capability
```

## 🎨 UI/UX Enhancements

### Dynamic Content Updates
- **Confidence Score**: Real-time circular progress animation
- **Detection Badge**: Color-coded health status (green/orange/red)
- **Health Metrics**: Dynamic status based on prediction
- **Recommendations**: Context-aware health advice

### Visual Feedback
- Loading states during processing
- Progress bars with status messages
- Success/error notifications
- Smooth transitions between steps

### Responsive Error Handling
- Connection warnings
- File validation messages
- API error explanations
- Retry mechanisms

## 🔧 Configuration

### API Configuration (in `api-integration.js`)
```javascript
const API_CONFIG = {
    BASE_URL: 'http://localhost:5000/api',  // Flask backend URL
    TIMEOUT: 30000,                         // 30 seconds
    RETRY_ATTEMPTS: 3,                      // Auto-retry failed requests
    RETRY_DELAY: 1000                       // 1 second between retries
};
```

### Supported File Formats
- **WAV** - Uncompressed audio (recommended)
- **MP3** - Compressed audio
- **M4A** - Apple audio format
- **FLAC** - Lossless compressed audio

### File Size Limits
- **Frontend validation**: 50MB (configurable)
- **Backend limit**: 50MB (Flask configuration)

## 🔒 Security Considerations

### CORS Handling
The Flask backend includes CORS support for frontend communication:
```python
CORS(app, origins=['http://localhost:8000', 'http://127.0.0.1:8000'])
```

### File Validation
- Client-side file type checking
- Server-side validation and sanitization
- Size limits to prevent abuse
- Temporary file cleanup

## 🐛 Troubleshooting

### Common Issues

1. **"Cannot connect to prediction service"**
   - Ensure Flask backend is running on `http://localhost:5000`
   - Check firewall settings
   - Verify CORS configuration

2. **"Invalid file type" errors**
   - Ensure file has correct extension (.wav, .mp3, .m4a, .flac)
   - Check file is not corrupted
   - Verify browser file type detection

3. **"Request timeout" errors**
   - Check network connectivity
   - Ensure file size is under 50MB
   - Verify backend processing capabilities

4. **API not initializing**
   - Check browser console for JavaScript errors
   - Ensure `api-integration.js` loads before `script.js`
   - Verify API endpoint URLs

### Debug Mode
Enable debug logging in browser console:
```javascript
window.BreathelyticsAPI.config.DEBUG = true;
```

## 📊 Performance Optimizations

### Frontend Optimizations
- Lazy loading of API connections
- Efficient file validation
- Minimal DOM manipulations
- Cached API responses

### Backend Integration
- Retry logic for failed requests
- Timeout handling
- Connection pooling
- Error recovery mechanisms

## 🔮 Future Enhancements

### Planned Features
- [ ] Real-time audio recording
- [ ] Batch file processing
- [ ] Historical analysis tracking
- [ ] Advanced visualization charts
- [ ] WebSocket support for live updates
- [ ] Progressive Web App (PWA) capabilities

### Integration Improvements
- [ ] Authentication/authorization
- [ ] Rate limiting
- [ ] Caching strategies
- [ ] Offline mode support

## 📞 Support

For issues related to the integration:
1. Check the test interface for API connectivity
2. Review browser console for JavaScript errors
3. Verify Flask backend logs
4. Ensure all dependencies are installed

## 🎉 Success Indicators

The integration is working correctly when:
- ✅ Test interface shows all green checkmarks
- ✅ Main app successfully predicts diseases
- ✅ Real-time progress indicators work
- ✅ Results display with proper confidence scores
- ✅ Reports can be downloaded
- ✅ Error messages are informative and helpful

---

**Integration completed successfully! 🎊**

The Breathelytics frontend now provides a seamless, real-time respiratory disease prediction experience powered by the Flask ML backend. 