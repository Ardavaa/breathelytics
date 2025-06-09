# `breathelytics`

<!-- **AI-Powered Respiratory Disease Detection Platform** -->
![Github Banner](doc/banner.png)

Breathelytics is a web-based platform that leverages advanced machine learning to analyze respiratory sounds and detect potential lung diseases. Using AI-powered audio analysis, the platform provides instant health insights from simple breathing or cough recordings.

---

## Team

| **Student ID** | **Name**                    | **Role**                                   |
| -------------- | --------------------------- | ------------------------------------------ |
| 103052300001   | Muhammad Karov Ardava Barus | Lead, AI/ML Engineer, Full Stack Developer |
| 103052300025   | Vadly Aryu Septian          | Front End Developer, AI/ML Engineer        |
| 103052300076   | Muhammad Zikra Al Rizkya    | AI/ML Engineer                             |
| 103052300087   | Rifa Mayshakori             | AI/ML Engineer                             |
| 103052300067   | Akhmad Muzakkii             | AI/ML Engineer                             |

---

## Features

- **🎤 Audio Upload & Analysis**: Upload respiratory audio files (WAV, MP3, M4A, FLAC) for instant AI analysis
- **🧠 AI-Powered Disease Detection**: Advanced machine learning model trained to detect 8 respiratory conditions:
  - Healthy (Normal)
  - Pneumonia
  - Bronchiolitis  
  - Bronchiectasis
  - COPD (Chronic Obstructive Pulmonary Disease)
  - URTI (Upper Respiratory Tract Infection)
  - LRTI (Lower Respiratory Tract Infection)
  - Asthma
- **📊 Confidence Scoring**: Provides confidence levels and detailed probability distributions
- **📋 Comprehensive Reports**: Generate downloadable analysis reports with recommendations
- **🎨 Modern UI/UX**: Clean, responsive interface with real-time progress tracking
- **⚡ Real-time Processing**: Fast analysis with live progress updates
- **🔒 Secure File Handling**: Temporary file processing with automatic cleanup
- **🛠️ Advanced CLI Tools**: Convenient command-line interface for easy development and deployment
- **🔧 Robust Audio Processing**: Enhanced pipeline with automatic sample rate adjustment and error handling
- **📱 Cross-Platform Support**: Works on Windows, macOS, and Linux with dedicated startup scripts

---

## Architecture

### Backend (Flask API)
- **Framework**: Python Flask with Flask-CORS
- **ML Pipeline**: Custom respiratory disease classification model with enhanced audio processing
- **Audio Processing**: Librosa for feature extraction with dynamic parameter adjustment
- **File Handling**: Secure upload validation and temporary storage
- **Enhanced Error Handling**: Robust pipeline with Nyquist frequency protection
- **API Endpoints**:
  - `GET /api/health` - Health check and model status
  - `POST /api/predict` - Main prediction endpoint
  - `GET /api/diseases` - Disease information
  - `GET /api/pipeline-status` - Model status

### Frontend (Vanilla JavaScript)
- **Technology**: Pure JavaScript, HTML5, CSS3
- **Design**: Modern responsive UI with CSS Grid/Flexbox
- **Enhanced Navigation**: Active/hover states for navbar and footer
- **Features**: 
  - Drag & drop file upload
  - Real-time progress tracking
  - Dynamic results visualization
  - Disease-specific UI themes
  - Mobile-responsive design
  - Smooth transitions and animations

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ 
- Git (for cloning)
- Modern web browser

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/breathelytics.git
   cd breathelytics
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv .venv
   
   # On Windows:
   .venv\Scripts\activate
   
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the application using CLI** (Recommended):
   ```bash
   # Start both frontend and backend
   python cli.py --both
   
   # Development mode with auto-reload
   python cli.py --dev
   
   # Show verbose output for debugging
   python cli.py --both --verbose
   ```

5. **Open in browser**: Navigate to `http://localhost:3000`

---

## 🛠️ CLI Tools

We provide multiple convenient ways to start your application:

### 🎯 Command Line Interface (Recommended)

```bash
# 🚀 Start both servers (production-ready)
python cli.py --both

# 🔧 Development mode (auto-reload, debugging)
python cli.py --dev

# 🌐 Frontend only (port 3000)
python cli.py --frontend

# ⚙️ Backend only (port 5000)
python cli.py --backend

# 📊 Verbose mode (show real-time logs)
python cli.py --backend --verbose

# 🎛️ Custom ports
python cli.py --both --frontend-port 8080 --backend-port 5001

# 🏭 Production mode (requires SECRET_KEY env var)
python cli.py --both --production

# ❓ Show help
python cli.py --help
```

### 🖱️ Interactive Menus

#### Windows Users
```bash
# Double-click or run in Command Prompt:
start-servers.bat
```

#### macOS/Linux Users
```bash
# Make executable (first time only):
chmod +x start-servers.sh

# Run:
./start-servers.sh
```

### ⚡ One-Line Quick Start
```bash
# Activate venv and start both servers
source .venv/Scripts/activate && python cli.py --both  # Windows Git Bash
source .venv/bin/activate && python cli.py --both     # macOS/Linux
```

---

## 🔧 Manual Setup (Alternative)

If you prefer the traditional approach:

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd src/breathelytics-backend
   ```

2. **Install backend dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables** (optional):
   ```bash
   export FLASK_ENV=development
   export FLASK_DEBUG=True
   export SECRET_KEY=your-secret-key-here
   ```

4. **Run the Flask server**:
   ```bash
   python run.py
   ```
   ✅ Backend running at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd src/breathelytics-frontend
   ```

2. **Start development server**:
   ```bash
   # Option 1: Python HTTP server
   python -m http.server 3000
   
   # Option 2: Node.js (if available)
   npx serve . -p 3000
   ```
   ✅ Frontend running at `http://localhost:3000`

---

## 📖 Usage Guide

1. **🌐 Navigate** to `http://localhost:3000` in your web browser
2. **🎯 Click "Start Diagnosis"** or go to the "Predict" tab
3. **📁 Upload an audio file**:
   - Drag & drop or click to browse
   - **Optimal**: 5-10 second recordings
   - **Environment**: Quiet background recommended
   - **Formats**: WAV, MP3, M4A, FLAC
   - **Size limit**: Maximum 50MB
4. **⏳ Wait for analysis** (typically 2-5 seconds)
5. **📊 View results**:
   - Disease prediction with confidence score
   - Detailed probability breakdown
   - Health insights and recommendations
6. **📥 Download report** (optional)

---

## 🧪 API Testing

Test the backend API directly using curl:

```bash
# Health check
curl http://localhost:5000/api/health

# Prediction (replace with your audio file)
curl -X POST -F "audio=@your_audio.wav" http://localhost:5000/api/predict

# Get disease information
curl http://localhost:5000/api/diseases

# Pipeline status
curl http://localhost:5000/api/pipeline-status
```

---

## 📁 Project Structure

```
breathelytics/
├── 🔧 cli.py                          # Main CLI tool
├── 🖥️ start-servers.bat               # Windows interactive menu
├── 🐧 start-servers.sh                # macOS/Linux interactive menu
├── 📋 requirements.txt                # Root Python dependencies
├── 📖 README.md                       # This documentation
├── 📂 src/
│   ├── 🔙 breathelytics-backend/      # Flask API Backend
│   │   ├── 🐍 app.py                  # Main Flask application
│   │   ├── 🚀 run.py                  # Production startup script
│   │   ├── ⚙️ config.py               # Configuration management
│   │   ├── 🧠 pipeline.py             # ML processing pipeline
│   │   ├── 🛠️ utils.py                # Utility functions
│   │   ├── 📦 models.py               # Data models
│   │   ├── 🧪 test_api.py             # API tests
│   │   ├── 📋 requirements.txt        # Backend dependencies
│   │   ├── 📊 logs/                   # Application logs
│   │   ├── 📁 temp/                   # Temporary file storage
│   │   └── 🤖 respiratory_classifier.pkl  # Trained ML model
│   └── 🎨 breathelytics-frontend/     # Frontend Application
│       ├── 🌐 index.html              # Main HTML page
│       ├── 🎨 styles.css              # CSS styles with enhanced UI
│       ├── ⚡ script.js               # Main JavaScript logic
│       ├── 🔌 api-integration.js      # API communication
│       ├── 🧪 test-integration.html   # API testing interface
│       └── 🖼️ images/                 # UI assets and icons
└── 📄 doc/                            # Documentation assets
    └── 🖼️ banner.png                  # Project banner
```

---

## 🔧 Development

### 🆕 Adding New Features

1. **Backend**: Add new endpoints in `src/breathelytics-backend/app.py`
2. **Frontend**: Update `script.js` and `api-integration.js`
3. **Styling**: Modify `styles.css` for UI changes
4. **CLI**: Extend `cli.py` for new development tools

### 🌍 Environment Variables

Backend supports these environment variables:

```bash
# Flask Configuration
FLASK_ENV=development          # development, testing, production
FLASK_DEBUG=True              # Enable debug mode
FLASK_HOST=0.0.0.0            # Bind address
FLASK_PORT=5000               # Port number

# Security
SECRET_KEY=your-secret-key    # Required for production

# Directories
TEMP_DIR=/path/to/temp        # Custom temp directory
LOGS_DIR=/path/to/logs        # Custom logs directory

# Logging
LOG_LEVEL=INFO                # DEBUG, INFO, WARNING, ERROR
```

### 🧪 Testing

```bash
# Run backend tests
cd src/breathelytics-backend
python -m pytest test_api.py -v

# Test API integration
# Open src/breathelytics-frontend/test-integration.html in browser
```

---

## 🐛 Troubleshooting

### Common Issues

1. **❌ "Failed to fetch" error**:
   ```bash
   # Check if backend is running
   curl http://localhost:5000/api/health
   
   # Restart with verbose logging
   python cli.py --backend --verbose
   ```

2. **📁 File upload fails**:
   - ✅ Check file format (WAV, MP3, M4A, FLAC only)
   - ✅ Ensure file size < 50MB
   - ✅ Verify file is not corrupted
   - ✅ Check browser console for errors

3. **🔇 Audio processing errors**:
   - ✅ Verify audio file has valid sample rate
   - ✅ Check for background noise levels
   - ✅ Ensure audio duration is reasonable (5-30 seconds)

4. **🔧 CLI issues**:
   ```bash
   # Check virtual environment
   python cli.py --help
   
   # Dependency issues
   pip install -r requirements.txt
   
   # Port conflicts
   python cli.py --both --frontend-port 8080 --backend-port 5001
   ```

### 🔍 Debug Mode

Enable comprehensive debugging:

```bash
# Environment variables
export FLASK_ENV=development
export FLASK_DEBUG=True
export LOG_LEVEL=DEBUG

# Start with verbose logging
python cli.py --dev --verbose
```

### 📊 Log Files

Check application logs for detailed error information:

```bash
# Backend logs
tail -f src/breathelytics-backend/logs/breathelytics_api.log

# CLI logs (when not using --verbose)
tail -f src/breathelytics-backend/logs/backend_stdout.log
tail -f src/breathelytics-backend/logs/backend_stderr.log
```

---

## 🆕 Recent Updates

### v1.1.0 (Latest)
- **✨ Enhanced CLI Tools**: Added comprehensive command-line interface with verbose mode
- **🔧 Cross-Platform Scripts**: Interactive menus for Windows (.bat) and Unix (.sh)
- **🛡️ Robust Audio Processing**: Fixed Nyquist frequency errors for low sample rate audio files
- **🎨 UI Improvements**: Enhanced navigation with active/hover states
- **📊 Better Error Handling**: Improved logging and error reporting
- **⚡ Performance Optimizations**: Faster startup and more reliable processing

### Key Fixes
- **🐛 Audio Processing**: Resolved spectral contrast feature extraction errors
- **🔧 CLI Stability**: Enhanced process management and graceful shutdown
- **🌐 CORS Issues**: Improved cross-origin request handling
- **📱 Responsive Design**: Better mobile and tablet support

---

## 📄 License

This project is developed for educational purposes as part of an academic assignment.

---

## 🤝 Contributing

This is an academic project. For questions or suggestions, please contact the team members listed above.

---

## 📞 Support

If you encounter issues:

1. **🔍 Check the troubleshooting section** above
2. **📊 Enable verbose logging**: `python cli.py --backend --verbose`
3. **🧪 Test the API directly** using the provided curl commands
4. **📧 Contact the development team** for academic support

---

**⚡ Ready to analyze your respiratory health? Start the application and upload your first audio recording!**

```bash
# Quick start - copy and paste this:
python cli.py --both
# Then open: http://localhost:3000
```
