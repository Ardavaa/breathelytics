/**
 * Breathelytics Flask API Integration
 * 
 * Handles communication with the Flask backend for respiratory disease prediction
 */

// API Configuration
const API_CONFIG = {
    BASE_URL: 'http://localhost:5000/api',
    TIMEOUT: 30000, // 30 seconds
    RETRY_ATTEMPTS: 3,
    RETRY_DELAY: 1000 // 1 second
};

// API Status
let apiStatus = {
    connected: false,
    modelAvailable: false,
    lastChecked: null
};

/**
 * Check API health and connectivity
 */
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}/health`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        
        apiStatus = {
            connected: true,
            modelAvailable: data.model_available || false,
            pipelineStatus: data.pipeline_status || 'unknown',
            version: data.version || 'unknown',
            lastChecked: new Date().toISOString()
        };

        console.log('API Health Check:', data);
        return data;

    } catch (error) {
        console.error('API Health Check Failed:', error);
        apiStatus = {
            connected: false,
            modelAvailable: false,
            lastChecked: new Date().toISOString(),
            error: error.message
        };
        throw error;
    }
}

/**
 * Get disease information from API
 */
async function getDiseaseInfo() {
    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}/diseases`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        console.log('Disease Info Retrieved:', data);
        return data;

    } catch (error) {
        console.error('Failed to get disease info:', error);
        throw error;
    }
}

/**
 * Upload audio file and get prediction
 */
async function predictRespiratoryDisease(audioFile, progressCallback = null) {
    if (!apiStatus.connected) {
        throw new Error('API is not connected. Please check your connection.');
    }

    if (!apiStatus.modelAvailable) {
        throw new Error('ML model is not available. Please contact support.');
    }

    // Validate file
    const validTypes = ['audio/wav', 'audio/mp3', 'audio/mpeg', 'audio/m4a', 'audio/flac'];
    if (!validTypes.includes(audioFile.type) && !audioFile.name.match(/\.(wav|mp3|m4a|flac)$/i)) {
        throw new Error('Invalid file type. Please upload WAV, MP3, M4A, or FLAC files.');
    }

    // Check file size (50MB limit from backend)
    const maxSize = 50 * 1024 * 1024; // 50MB
    if (audioFile.size > maxSize) {
        throw new Error(`File too large. Maximum size is ${Math.round(maxSize / 1024 / 1024)}MB.`);
    }

    try {
        // Create FormData
        const formData = new FormData();
        formData.append('audio', audioFile);

        // Create AbortController for timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.TIMEOUT);

        // Make prediction request
        const response = await fetch(`${API_CONFIG.BASE_URL}/predict`, {
            method: 'POST',
            body: formData,
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
        }

        const result = await response.json();
        console.log('Prediction Result:', result);

        // Validate response structure
        if (!result.prediction || typeof result.confidence !== 'number') {
            throw new Error('Invalid response format from server');
        }

        return result;

    } catch (error) {
        if (error.name === 'AbortError') {
            throw new Error('Request timeout. Please try again with a smaller file.');
        }
        
        console.error('Prediction Failed:', error);
        throw error;
    }
}

/**
 * Get pipeline status
 */
async function getPipelineStatus() {
    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}/pipeline/status`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        console.log('Pipeline Status:', data);
        return data;

    } catch (error) {
        console.error('Failed to get pipeline status:', error);
        throw error;
    }
}

/**
 * Retry wrapper for API calls
 */
async function retryOperation(operation, maxRetries = API_CONFIG.RETRY_ATTEMPTS) {
    let lastError;
    
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
            return await operation();
        } catch (error) {
            lastError = error;
            
            if (attempt === maxRetries) {
                break;
            }
            
            console.warn(`Attempt ${attempt} failed, retrying in ${API_CONFIG.RETRY_DELAY}ms...`, error.message);
            await new Promise(resolve => setTimeout(resolve, API_CONFIG.RETRY_DELAY * attempt));
        }
    }
    
    throw lastError;
}

/**
 * Format confidence score for display
 */
function formatConfidence(confidence) {
    return Math.round(confidence * 100);
}

/**
 * Get confidence level description
 */
function getConfidenceLevel(confidence) {
    const percentage = confidence * 100;
    
    if (percentage >= 90) return 'Very High';
    if (percentage >= 80) return 'High';
    if (percentage >= 70) return 'Moderate';
    if (percentage >= 60) return 'Low';
    return 'Very Low';
}

/**
 * Format disease probabilities for display
 */
function formatProbabilities(probabilities) {
    return Object.entries(probabilities)
        .map(([disease, probability]) => ({
            disease,
            probability: Math.round(probability * 100),
            formatted: `${Math.round(probability * 100)}%`
        }))
        .sort((a, b) => b.probability - a.probability);
}

/**
 * Get health recommendations based on prediction
 */
function getHealthRecommendations(prediction, confidence) {
    const recommendations = [];
    
    if (prediction.toLowerCase() === 'healthy') {
        if (confidence >= 0.8) {
            recommendations.push(
                'Your respiratory sounds appear normal',
                'Continue maintaining good respiratory health with regular exercise',
                'Monitor any changes in breathing patterns'
            );
        } else {
            recommendations.push(
                'Results suggest normal respiratory function, but confidence is moderate',
                'Consider retaking the test with a clearer audio recording',
                'Monitor for any respiratory symptoms'
            );
        }
    } else {
        if (confidence >= 0.8) {
            recommendations.push(
                `The analysis suggests possible ${prediction}`,
                'We strongly recommend consulting with a healthcare provider immediately',
                'Bring these results to your doctor for further evaluation'
            );
        } else {
            recommendations.push(
                `The analysis suggests possible ${prediction}, but with moderate confidence`,
                'Consider retaking the test or consulting with a healthcare provider',
                'Monitor your symptoms and seek medical attention if they worsen'
            );
        }
    }
    
    // Always add disclaimer
    recommendations.push(
        'This is an AI-powered screening tool and should not replace professional medical advice',
        'Consult with a healthcare provider for proper diagnosis and treatment'
    );
    
    return recommendations;
}

/**
 * Initialize API connection on page load
 */
async function initializeAPI() {
    try {
        console.log('Initializing API connection...');
        await checkAPIHealth();
        console.log('API initialized successfully:', apiStatus);
        return true;
    } catch (error) {
        console.error('Failed to initialize API:', error);
        return false;
    }
}

// Export functions for use in main script
window.BreathelyticsAPI = {
    checkAPIHealth,
    getDiseaseInfo,
    predictRespiratoryDisease,
    getPipelineStatus,
    retryOperation,
    formatConfidence,
    getConfidenceLevel,
    formatProbabilities,
    getHealthRecommendations,
    initializeAPI,
    apiStatus: () => apiStatus,
    config: API_CONFIG
};

// Auto-initialize on load
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', () => {
        initializeAPI().then(success => {
            if (success) {
                console.log('✅ Breathelytics API ready');
                // Dispatch custom event to notify main script
                document.dispatchEvent(new CustomEvent('breathelytics-api-ready', {
                    detail: { apiStatus }
                }));
            } else {
                console.warn('⚠️ Breathelytics API initialization failed');
                document.dispatchEvent(new CustomEvent('breathelytics-api-error', {
                    detail: { error: 'Failed to connect to API' }
                }));
            }
        });
    });
} 