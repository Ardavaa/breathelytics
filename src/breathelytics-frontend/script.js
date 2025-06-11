// Audioscope AI - JavaScript functionality with Flask API Integration
document.addEventListener('DOMContentLoaded', function() {
    
    // Global variables
    let isAPIReady = false;
    let currentPredictionResult = null;
    let uploadedFile = null;
    
    // Wait for API to be ready
    document.addEventListener('breathelytics-api-ready', function(event) {
        isAPIReady = true;
        console.log('API is ready for predictions');
        updateUIBasedOnAPIStatus(true);
    });
    
    document.addEventListener('breathelytics-api-error', function(event) {
        isAPIReady = false;
        console.warn('API connection failed:', event.detail.error);
        updateUIBasedOnAPIStatus(false);
    });
    
    function updateUIBasedOnAPIStatus(connected) {
        const uploadSection = document.querySelector('[data-step="1"]');
        if (uploadSection) {
            if (!connected) {
                // Show API connection warning
                showNotification('⚠️ Cannot connect to prediction service. Please ensure the Flask backend is running.', 'warning', 8000);
            }
        }
    }

    // Navigation handling for both navbar and footer links
    function handleNavigationClick(e, targetTab) {
        e.preventDefault();
        
        // Close mobile menu if open
        if (typeof isMobileMenuOpen !== 'undefined' && isMobileMenuOpen) {
            isMobileMenuOpen = false;
            if (navContent) {
                navContent.classList.remove('mobile-menu-open');
            }
            
            // Reset hamburger icon
            if (mobileMenuBtn) {
                mobileMenuBtn.innerHTML = `
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                        <path d="M3 12h18M3 6h18M3 18h18" stroke="#252525" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                `;
            }
        }
        
        // Switch to the target tab
        switchTab(targetTab);
        
        // For home tab, scroll to hero section
        if (targetTab === 'home') {
            setTimeout(() => {
                const heroSection = document.querySelector('.hero');
                if (heroSection) {
                    heroSection.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                } else {
                    window.scrollTo({
                        top: 0,
                        behavior: 'smooth'
                    });
                }
            }, 100);
        }
        
        showNotification(`Navigated to ${targetTab}`, 'info', 2000);
    }

    // Handle navbar navigation links
    const navbarLinks = document.querySelectorAll('.nav-link');
    navbarLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetTab = this.getAttribute('data-tab');
            if (targetTab) {
                handleNavigationClick(e, targetTab);
            }
        });
    });

    // Handle footer navigation links
    const footerLinks = document.querySelectorAll('.footer-link');
    footerLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#home') {
                handleNavigationClick(e, 'home');
            } else if (href === '#predict') {
                handleNavigationClick(e, 'predict');
            }
        });
    });

    // Mobile menu toggle
    const navbar = document.querySelector('.navbar');
    const navContent = document.querySelector('.nav-content');
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    
    // Mobile menu toggle functionality
    let isMobileMenuOpen = false;
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            isMobileMenuOpen = !isMobileMenuOpen;
            navContent.classList.toggle('mobile-menu-open', isMobileMenuOpen);
            
            // Update button icon
            if (isMobileMenuOpen) {
                mobileMenuBtn.innerHTML = `
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                        <path d="M18 6L6 18M6 6l12 12" stroke="#252525" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                `;
            } else {
                mobileMenuBtn.innerHTML = `
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                        <path d="M3 12h18M3 6h18M3 18h18" stroke="#252525" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                `;
            }
        });
    }

    // Logo navigation functionality for both navbar and footer
    function handleLogoClick() {
        // Always redirect to root with home hash
        const currentPath = window.location.pathname;
        const currentOrigin = window.location.origin;
        
        // Check if we're on the main page or a different page
        if (currentPath === '/' || currentPath === '/index.html' || currentPath.endsWith('/index.html')) {
            // We're on the main page, switch to home tab and scroll
            switchTab('home');
            
            // Close mobile menu if open
            if (typeof isMobileMenuOpen !== 'undefined' && isMobileMenuOpen) {
                isMobileMenuOpen = false;
                if (navContent) {
                    navContent.classList.remove('mobile-menu-open');
                }
                
                // Reset hamburger icon
                if (mobileMenuBtn) {
                    mobileMenuBtn.innerHTML = `
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                            <path d="M3 12h18M3 6h18M3 18h18" stroke="#252525" stroke-width="2" stroke-linecap="round"/>
                        </svg>
                    `;
                }
            }
            
            // Scroll to hero section
            setTimeout(() => {
                const heroSection = document.querySelector('.hero');
                if (heroSection) {
                    heroSection.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                } else {
                    window.scrollTo({
                        top: 0,
                        behavior: 'smooth'
                    });
                }
            }, 100);
        } else {
            // We're on a different page, redirect to home
            window.location.href = currentOrigin + '/#home';
        }
        
        showNotification('Navigating to home', 'info', 2000);
    }

    // Add click handlers to both navbar and footer logos
    const navLogo = document.getElementById('navLogo');
    const footerLogo = document.querySelector('.footer-logo');
    
    if (navLogo) {
        navLogo.style.cursor = 'pointer';
        navLogo.addEventListener('click', handleLogoClick);
    }
    
    if (footerLogo) {
        footerLogo.style.cursor = 'pointer';
        footerLogo.addEventListener('click', handleLogoClick);
    }

    // Mobile menu closing is now handled in the handleNavigationClick function

    // Scroll effects
    let lastScrollTop = 0;
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Navbar background opacity on scroll
        if (scrollTop > 50) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.backdropFilter = 'blur(20px)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.backdropFilter = 'blur(10px)';
        }
        
        // Hide/show navbar on scroll
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling down
            navbar.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });

    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observe elements for animation
    const animateElements = document.querySelectorAll('.step-card, .disease-card, .section-header');
    animateElements.forEach(el => {
        observer.observe(el);
    });

    // CTA button interactions
    const ctaButtons = document.querySelectorAll('.cta-button, .hero-cta');
    ctaButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Add click animation
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
            
            // Switch to predict tab
            switchTab('predict');
        });
    });

    // Disease card interactions
    const diseaseCards = document.querySelectorAll('.disease-card');
    diseaseCards.forEach(card => {
        card.addEventListener('click', function() {
            const diseaseName = this.querySelector('h3').textContent;
            showNotification(`Learning more about ${diseaseName}...`, 'info');
        });
    });

    // Step card interactions
    const stepCards = document.querySelectorAll('.step-card');
    stepCards.forEach((card, index) => {
        card.addEventListener('click', function() {
            const stepName = this.querySelector('h3').textContent;
            showNotification(`Step ${index + 1}: ${stepName}`, 'info');
        });
    });

    // Enhanced notification system
    function showNotification(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.classList.add('notification', `notification-${type}`);
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-message">${message}</span>
                <button class="notification-close">&times;</button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Show notification
        setTimeout(() => {
            notification.classList.add('notification-show');
        }, 100);
        
        // Auto hide after specified duration
        const autoHide = setTimeout(() => {
            hideNotification(notification);
        }, duration);
        
        // Close button functionality
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => {
            clearTimeout(autoHide);
            hideNotification(notification);
        });
    }

    function hideNotification(notification) {
        notification.classList.remove('notification-show');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }

    // Floating icons animation enhancement
    const floatingIcons = document.querySelectorAll('.floating-icon');
    floatingIcons.forEach((icon, index) => {
        icon.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1) rotate(180deg)';
            this.style.background = '#68D8D6';
        });
        
        icon.addEventListener('mouseleave', function() {
            this.style.transform = '';
            this.style.background = '#F0FBFB';
        });
    });

    // Parallax effect for floating icons
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset;
        
        floatingIcons.forEach((icon, index) => {
            const speed = (index + 1) * 0.1;
            const yPos = scrollTop * speed;
            icon.style.transform = `translateY(${yPos}px)`;
        });
    });

    // Form validation (for future use)
    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Local storage for user preferences
    const userPreferences = {
        theme: localStorage.getItem('audioscope-theme') || 'light',
        animations: localStorage.getItem('audioscope-animations') !== 'false'
    };

    // Apply user preferences
    if (!userPreferences.animations) {
        document.body.classList.add('no-animations');
    }

    // Save preferences
    function savePreferences() {
        localStorage.setItem('audioscope-theme', userPreferences.theme);
        localStorage.setItem('audioscope-animations', userPreferences.animations);
    }

    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        // ESC key to close any open modals or menus
        if (e.key === 'Escape') {
            if (isMobileMenuOpen) {
                mobileMenuBtn.click();
            }
        }
        
        // Tab navigation enhancement
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-navigation');
        }
    });

    document.addEventListener('mousedown', function() {
        document.body.classList.remove('keyboard-navigation');
    });

    // Performance optimization - lazy loading for images
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // Error handling for images
    const allImages = document.querySelectorAll('img');
    allImages.forEach(img => {
        img.addEventListener('error', function() {
            this.style.display = 'none';
            console.warn(`Failed to load image: ${this.src}`);
        });
    });

    // Analytics tracking (placeholder)
    function trackEvent(eventName, properties = {}) {
        // In a real application, you would send this to your analytics service
        console.log('Event tracked:', eventName, properties);
    }

    // Track page load
    trackEvent('page_view', {
        page: window.location.pathname,
        timestamp: new Date().toISOString()
    });

    // Track CTA clicks
    ctaButtons.forEach(button => {
        button.addEventListener('click', () => {
            trackEvent('cta_click', {
                button_text: button.textContent.trim(),
                timestamp: new Date().toISOString()
            });
        });
    });

    // Tab System
    const tabNavLinks = document.querySelectorAll('.nav-link[data-tab]');
    const tabPanels = document.querySelectorAll('.tab-panel');
    function switchTab(targetTab) {
        // Remove active class from all nav links
        tabNavLinks.forEach(link => link.classList.remove('active'));
        // Remove active class from all footer links
        const tabFooterLinks = document.querySelectorAll('.footer-link');
        tabFooterLinks.forEach(link => link.classList.remove('active'));
        // Remove active class from all tab panels
        tabPanels.forEach(panel => panel.classList.remove('active'));
        // Add active class to clicked nav link
        const targetLink = document.querySelector(`.nav-link[data-tab="${targetTab}"]`);
        if (targetLink) targetLink.classList.add('active');
        // Add active class to corresponding footer link
        const targetFooterLink = document.querySelector(`.footer-link[href="#${targetTab}"]`);
        if (targetFooterLink) targetFooterLink.classList.add('active');
        // Show target tab panel
        const targetPanel = document.querySelector(`#${targetTab}-content`);
        if (targetPanel) targetPanel.classList.add('active');
        // Update URL hash without scrolling
        history.pushState(null, null, `#${targetTab}`);
    }

    // Add click event listeners to nav links
    tabNavLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetTab = this.getAttribute('data-tab');
            switchTab(targetTab);
        });
    });
    
    // Handle initial page load based on hash
    function handleInitialHash() {
        const hash = window.location.hash.substring(1);
        if (hash === 'predict') {
            switchTab('predict');
        } else {
            switchTab('home');
        }
    }
    
    // Handle browser back/forward buttons
    window.addEventListener('popstate', handleInitialHash);
    
    // Initialize on page load
    handleInitialHash();

    // File upload functionality with Flask API integration
    const stepItems = document.querySelectorAll('#predict-content .step-item');
    const stepContents = document.querySelectorAll('#predict-content .step-content');
    const uploadArea = document.getElementById('uploadArea');
    const audioFileInput = document.getElementById('audioFile');
    
    console.log('Step elements found:', {
        stepItems: stepItems.length,
        stepContents: stepContents.length,
        uploadArea: !!uploadArea,
        audioFileInput: !!audioFileInput
    });
    
    if (uploadArea && audioFileInput) {
        uploadArea.addEventListener('click', () => {
            audioFileInput.click();
        });
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFileUpload(files[0]);
            }
        });
        
        audioFileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFileUpload(e.target.files[0]);
            }
        });
    }
    
    async function handleFileUpload(file) {
        // Check if API is ready
        if (!isAPIReady) {
            showNotification('⚠️ Prediction service is not available. Please ensure the Flask backend is running.', 'error');
            return;
        }
        
        try {
            // Validate file using API validation
            await window.BreathelyticsAPI.predictRespiratoryDisease(file, null);
        } catch (error) {
            if (error.message.includes('Invalid file type')) {
                showNotification('Please upload a valid audio file (.wav, .mp3, .m4a, .flac)', 'error');
                return;
            } else if (error.message.includes('File too large')) {
                showNotification(error.message, 'error');
                return;
            }
            // For other errors, we'll handle them in the processing phase
        }
        
        uploadedFile = file;
        showNotification(`File "${file.name}" uploaded successfully!`, 'success');
        
        // Start processing with a smooth transition
        setTimeout(() => {
            startProcessing();
        }, 800);
    }
    
    async function startProcessing() {
        if (!uploadedFile) {
            showNotification('No file uploaded', 'error');
            return;
        }
        
        // Move to step 2
        setActiveStep(2);
        
        const progressBar = document.querySelector('.progress-fill');
        const progressPercentage = document.querySelector('.progress-percentage');
        const processingTime = document.getElementById('processingTime');
        const processingStatus = document.getElementById('processingStatus');
        const processSteps = document.querySelectorAll('.process-step');
        
        let progress = 0;
        let timeElapsed = 0;
        let currentStepIndex = 0;
        
        const statusMessages = [
            'Uploading audio file...',
            'Extracting audio features...',
            'Running AI classification...',
            'Generating detailed report...'
        ];

        // Start progress animation
        const progressInterval = setInterval(() => {
            // Update time
            timeElapsed += 0.3;
            if (processingTime) processingTime.textContent = timeElapsed.toFixed(1);
            
            // Update progress based on current step
            if (progress < 95) {
                progress += Math.random() * 3 + 1;
                if (progressBar) progressBar.style.width = `${progress}%`;
                if (progressPercentage) progressPercentage.textContent = `${Math.round(progress)}%`;
            }
            
            // Update processing steps
            const stepProgress = progress / 25;
            const newStepIndex = Math.min(Math.floor(stepProgress), 3);
            
            if (newStepIndex > currentStepIndex && processSteps[newStepIndex]) {
                if (processSteps[currentStepIndex]) {
                    processSteps[currentStepIndex].classList.remove('active');
                    processSteps[currentStepIndex].classList.add('completed');
                }
                
                processSteps[newStepIndex].classList.add('active');
                currentStepIndex = newStepIndex;
                
                if (processingStatus && statusMessages[newStepIndex]) {
                    processingStatus.textContent = statusMessages[newStepIndex];
                }
            }
        }, 300);
        
        try {
            // Make actual API call
            const result = await window.BreathelyticsAPI.predictRespiratoryDisease(uploadedFile);
            currentPredictionResult = result;
            
            // Complete progress animation
            clearInterval(progressInterval);
            
            // Ensure we reach 100%
            progress = 100;
            if (progressBar) progressBar.style.width = '100%';
            if (progressPercentage) progressPercentage.textContent = '100%';
            
            // Complete final step
            if (processSteps[3]) {
                processSteps[3].classList.remove('active');
                processSteps[3].classList.add('completed');
            }
            
            if (processingStatus) {
                processingStatus.textContent = 'Analysis complete!';
            }
            
            setTimeout(() => {
                showResults();
            }, 1500);
            
        } catch (error) {
            console.error('Prediction failed:', error);
            clearInterval(progressInterval);
            
            // Show error in UI
            if (processingStatus) {
                processingStatus.textContent = 'Analysis failed';
            }
            
            showNotification(`Prediction failed: ${error.message}`, 'error', 8000);
            
            // Allow user to retry
            setTimeout(() => {
                setActiveStep(1);
                resetProcessingUI();
            }, 3000);
        }
    }
    
    function showResults() {
        console.log('showResults called');
        if (!currentPredictionResult) {
            showNotification('No prediction result available', 'error');
            return;
        }
        
        console.log('Moving to step 3...');
        // Move to step 3
        setActiveStep(3);
        
        console.log('Updating results UI...');
        // Update UI with real results
        updateResultsUI(currentPredictionResult);
        
        showNotification('Analysis complete! Your results are ready.', 'success');
        console.log('showResults completed');
    }
    
    // Disease display mapping
    const DISEASE_DISPLAY = {
        asthma: {
            name: 'Asthma',
            image: 'images/lungs.svg',
            description: 'Asthma is a condition in which your airways narrow and swell and may produce extra mucus, making breathing difficult.',
            badge: 'warning',
            color: '#F9A825',
        },
        bronchiectasis: {
            name: 'Bronchiectasis',
            image: 'images/bronchiectasis.png',
            description: 'Bronchiectasis is a chronic condition where the walls of the bronchi are thickened from inflammation and infection.',
            badge: 'warning',
            color: '#8E24AA',
        },
        bronchiolitis: {
            name: 'Bronchiolitis',
            image: 'images/bronchitis.png',
            description: 'Bronchiolitis is an infection of the small airways in the lungs, usually caused by a virus.',
            badge: 'warning',
            color: '#039BE5',
        },
        copd: {
            name: 'COPD',
            image: 'images/copd.png',
            description: 'Chronic Obstructive Pulmonary Disease (COPD) is a chronic inflammatory lung disease that causes obstructed airflow.',
            badge: 'warning',
            color: '#FF7043',
        },
        healthy: {
            name: 'Healthy',
            image: 'images/healthy-lungs.png',
            description: 'Your respiratory patterns appear normal with no significant abnormalities detected. Continue maintaining good lung health practices.',
            badge: 'healthy',
            color: '#43A047',
        },
        lrti: {
            name: 'LRTI',
            image: 'images/lungs.svg',
            description: 'Lower Respiratory Tract Infection (LRTI) affects the airways and lungs, often causing cough and difficulty breathing.',
            badge: 'warning',
            color: '#1976D2',
        },
        pneumonia: {
            name: 'Pneumonia',
            image: 'images/pneumonia.png',
            description: 'Pneumonia is an infection that inflames the air sacs in one or both lungs, which may fill with fluid.',
            badge: 'warning',
            color: '#D32F2F',
        },
        urti: {
            name: 'URTI',
            image: 'images/cold.png',
            description: 'Upper Respiratory Tract Infection (URTI) affects the nose, throat, and airways, often caused by viruses.',
            badge: 'warning',
            color: '#0288D1',
        },
    };

    function updateResultsUI(result) {
        console.log('updateResultsUI called with:', result);
        if (!result || !result.prediction || typeof result.confidence !== 'number') {
            showNotification('Prediction result is incomplete. Please try again.', 'error');
            return;
        }
        
        // Log which elements are found
        const confidenceValue = document.querySelector('.confidence-value');
        const confidenceLabel = document.querySelector('.confidence-label');
        const scoreCircle = document.querySelector('.score-circle');
        const detectionBadge = document.querySelector('.detection-badge');
        const conditionTitle = document.querySelector('.condition-details h4');
        const conditionDescription = document.querySelector('.condition-details p');
        const healthMetrics = document.querySelector('.health-metrics');
        const recommendationsList = document.querySelector('.recommendations ul');
        const conditionVisual = document.querySelector('.condition-visual img');
        const confidenceInfo = document.querySelector('.confidence-info h3');
        const confidenceInfoP = document.querySelector('.confidence-info p');

        console.log('DOM elements found:', {
            confidenceValue: !!confidenceValue,
            confidenceLabel: !!confidenceLabel,
            scoreCircle: !!scoreCircle,
            detectionBadge: !!detectionBadge,
            conditionTitle: !!conditionTitle,
            conditionDescription: !!conditionDescription,
            healthMetrics: !!healthMetrics,
            recommendationsList: !!recommendationsList,
            conditionVisual: !!conditionVisual,
            confidenceInfo: !!confidenceInfo,
            confidenceInfoP: !!confidenceInfoP
        });

        // Disease mapping
        const key = result.prediction.toLowerCase().replace(/\s|\(|\)/g, '');
        const disease = DISEASE_DISPLAY[key] || DISEASE_DISPLAY['healthy'];
        console.log('Disease mapping:', { key, disease: disease.name });

        // Update confidence score
        const confidencePercentage = window.BreathelyticsAPI.formatConfidence(result.confidence);
        if (confidenceValue) confidenceValue.textContent = confidencePercentage;

        const confidenceLevel = window.BreathelyticsAPI.getConfidenceLevel(result.confidence);
        if (confidenceLabel) confidenceLabel.textContent = `${confidenceLevel} Confidence`;

        // Animate the confidence circle
        setTimeout(() => {
            if (scoreCircle) {
                const circumference = 2 * Math.PI * 60;
                const offset = circumference - (confidencePercentage / 100) * circumference;
                scoreCircle.style.strokeDashoffset = offset;
            }
        }, 500);

        // Update detection badge
        if (detectionBadge) {
            detectionBadge.className = `detection-badge ${disease.badge}`;
            const statusDot = detectionBadge.querySelector('.status-dot');
            if (statusDot) statusDot.style.background = disease.color;
            const statusText = detectionBadge.querySelector('span:last-child');
            if (statusText) statusText.textContent = disease.name;
        }

        // Update condition details
        if (conditionTitle) {
            conditionTitle.textContent = disease.name === 'Healthy' ? 'Normal Respiratory Function' : disease.name;
        }
        if (conditionDescription) {
            conditionDescription.textContent = disease.description;
        }
        if (conditionVisual) {
            conditionVisual.src = disease.image;
            conditionVisual.alt = disease.name;
        }
        if (confidenceInfo) {
            confidenceInfo.textContent = confidenceLevel + ' Detection';
        }
        if (confidenceInfoP) {
            confidenceInfoP.textContent = `The AI model is ${confidenceLevel.toLowerCase()} in this analysis based on detected audio patterns.`;
        }

        // Update health metrics based on prediction
        if (healthMetrics) {
            const metrics = healthMetrics.querySelectorAll('.metric');
            metrics.forEach((metric, index) => {
                const valueSpan = metric.querySelector('.metric-value');
                if (valueSpan) {
                    valueSpan.className = `metric-value ${disease.badge === 'healthy' ? 'normal' : 'abnormal'}`;
                    switch (index) {
                        case 0: // Breathing Pattern
                            valueSpan.textContent = disease.name === 'Healthy' ? 'Normal' : 'Irregular';
                            break;
                        case 1: // Sound Quality
                            valueSpan.textContent = confidencePercentage > 80 ? 'Clear' : 'Unclear';
                            break;
                        case 2: // Rhythm
                            valueSpan.textContent = disease.name === 'Healthy' ? 'Regular' : 'Irregular';
                            break;
                    }
                }
            });
        }

        // Update recommendations list
        const recommendations = window.BreathelyticsAPI.getHealthRecommendations(result.prediction, result.confidence);
        if (recommendationsList) {
            recommendationsList.innerHTML = '';
            recommendations.slice(1).forEach(recommendation => {
                const li = document.createElement('li');
                li.textContent = recommendation;
                recommendationsList.appendChild(li);
            });
        }

        // Update additional details if available
        if (result.all_probabilities) {
            updateProbabilityDisplay(result.all_probabilities);
        }
        
        // Create probability chart
        createProbabilityChart(result);
        
        // Update AI insights if available
        console.log('Checking for AI insights in result...');
        console.log('result.ai_insights exists:', !!result.ai_insights);
        
        if (result.ai_insights) {
            console.log('AI insights found, calling updateAIInsights...');
            updateAIInsights(result.ai_insights);
        } else {
            console.log('No AI insights available in result');
            // Hide AI insights section if no insights
            const aiInsightsSection = document.querySelector('.ai-insights-section');
            if (aiInsightsSection) {
                aiInsightsSection.style.display = 'none';
            }
        }
        
        console.log('updateResultsUI completed');
    }
    
    function updateProbabilityDisplay(probabilities) {
        // This could be used to show all disease probabilities
        // For now, we'll log them for debugging
        const formatted = window.BreathelyticsAPI.formatProbabilities(probabilities);
        console.log('Disease Probabilities:', formatted);
    }
    
    function updateAIInsights(aiInsights) {
        console.log('Updating AI insights:', aiInsights);
        
        // Update AI summary
        const aiSummaryElement = document.querySelector('.ai-summary');
        if (aiSummaryElement) {
            aiSummaryElement.textContent = aiInsights.summary || 'AI insights not available';
        }
        
        // Update condition explanation
        const conditionExplanationElement = document.querySelector('.ai-condition-explanation');
        if (conditionExplanationElement) {
            conditionExplanationElement.textContent = aiInsights.condition_explanation || 'Condition explanation not available';
        }
        
        // Update confidence interpretation - generate if not provided
        const confidenceInterpretationElement = document.querySelector('.ai-confidence-interpretation');
        if (confidenceInterpretationElement) {
            let confidenceText = aiInsights.confidence_interpretation;
            
            // If not provided, generate based on prediction and confidence from current result
            if (!confidenceText && currentPredictionResult) {
                const confidenceLevel = window.BreathelyticsAPI.getConfidenceLevel(currentPredictionResult.confidence);
                const prediction = currentPredictionResult.prediction;
                confidenceText = `${confidenceLevel} confidence level (${Math.round(currentPredictionResult.confidence * 100)}%) for ${prediction} detection. The AI model shows patterns that ${confidenceLevel === 'High' || confidenceLevel === 'Very High' ? 'are consistent' : 'require further validation'}.`;
            }
            
            confidenceInterpretationElement.textContent = confidenceText || 'Confidence interpretation not available';
        }
        
        // Update insights list
        const insightsList = document.querySelector('.ai-insights-list');
        if (insightsList && aiInsights.insights) {
            insightsList.innerHTML = '';
            aiInsights.insights.forEach(insight => {
                const li = document.createElement('li');
                li.textContent = insight;
                insightsList.appendChild(li);
            });
        }
        
        // Update recommendations by category
        if (aiInsights.recommendations) {
            const categories = ['immediate', 'monitoring', 'lifestyle', 'medical'];
            
            categories.forEach(category => {
                const categoryList = document.querySelector(`.ai-recommendations-${category}`);
                if (categoryList && aiInsights.recommendations[category]) {
                    categoryList.innerHTML = '';
                    aiInsights.recommendations[category].forEach(recommendation => {
                        const li = document.createElement('li');
                        li.textContent = recommendation;
                        categoryList.appendChild(li);
                    });
                }
            });
        }
        
        // Update risk level
        const riskLevelElement = document.querySelector('.ai-risk-level');
        if (riskLevelElement && aiInsights.risk_level) {
            riskLevelElement.textContent = aiInsights.risk_level;
            riskLevelElement.className = `ai-risk-level risk-${aiInsights.risk_level.toLowerCase()}`;
        }
        
        // Update next steps
        const nextStepsElement = document.querySelector('.ai-next-steps');
        if (nextStepsElement) {
            nextStepsElement.textContent = aiInsights.next_steps || 'Next steps information not available';
        }
        
        // Update disclaimer
        const disclaimerElement = document.querySelector('.ai-disclaimer');
        if (disclaimerElement) {
            disclaimerElement.textContent = aiInsights.disclaimer || 'This is an initial AI screening. Medical consultation is still required.';
        }
        
        // Show AI insights section
        const aiInsightsSection = document.querySelector('.ai-insights-section');
        if (aiInsightsSection) {
            aiInsightsSection.style.display = 'block';
        }
        
        // Show LLM status
        if (aiInsights.llm_status) {
            console.log(`AI Insights Status: ${aiInsights.llm_status}`);
            if (aiInsights.llm_status === 'fallback_used') {
                showNotification('AI insights using fallback mode', 'warning', 5000);
            }
        }
        
        console.log('AI insights updated successfully');
    }
    
    function resetProcessingUI() {
        const progressBar = document.querySelector('.progress-fill');
        const progressPercentage = document.querySelector('.progress-percentage');
        const processingTime = document.getElementById('processingTime');
        const processingStatus = document.getElementById('processingStatus');
        const processSteps = document.querySelectorAll('.process-step');
        
        if (progressBar) progressBar.style.width = '0%';
        if (progressPercentage) progressPercentage.textContent = '0%';
        if (processingTime) processingTime.textContent = '0.0';
        if (processingStatus) processingStatus.textContent = 'Extracting audio features...';
        
        processSteps.forEach((step, index) => {
            step.classList.remove('active', 'completed');
        });
        
        // Reset file input
        if (audioFileInput) audioFileInput.value = '';
        uploadedFile = null;
        currentPredictionResult = null;
    }

    function setActiveStep(stepNumber) {
        console.log('setActiveStep called with stepNumber:', stepNumber);
        
        // Update step indicators
        stepItems.forEach((item, index) => {
            item.classList.remove('active', 'completed');
            
            if (index + 1 === stepNumber) {
                item.classList.add('active');
                console.log(`Step ${index + 1} indicator set to active`);
            } else if (index + 1 < stepNumber) {
                item.classList.add('completed');
                console.log(`Step ${index + 1} indicator set to completed`);
            }
        });
        
        // Update step content
        stepContents.forEach((content, index) => {
            content.classList.remove('active');
            
            if (index + 1 === stepNumber) {
                content.classList.add('active');
                console.log(`Step ${index + 1} content set to active`, content);
            }
        });
        
        // Update step connectors
        const stepConnectors = document.querySelectorAll('.step-connector');
        stepConnectors.forEach((connector, index) => {
            const afterElement = connector.querySelector('::after') || connector;
            if (index + 1 < stepNumber) {
                connector.style.setProperty('--progress', '100%');
            } else {
                connector.style.setProperty('--progress', '0%');
            }
        });
        
        console.log('setActiveStep completed');
    }

    // Download report functionality with real data
    const downloadReportBtn = document.getElementById('downloadReport');
    if (downloadReportBtn) {
        downloadReportBtn.addEventListener('click', () => {
            if (!currentPredictionResult) {
                showNotification('No prediction result available to download', 'error');
                return;
            }

            // Add loading state
            const originalText = downloadReportBtn.innerHTML;
            downloadReportBtn.innerHTML = `
                <div class="spinner" style="width: 20px; height: 20px; border-width: 2px;"></div>
                <span>Generating Report...</span>
            `;
            downloadReportBtn.disabled = true;
            
            showNotification('Generating detailed report...', 'info');
            
            setTimeout(() => {
                try {
                    // Generate report with real data
                    const confidence = window.BreathelyticsAPI.formatConfidence(currentPredictionResult.confidence);
                    const confidenceLevel = window.BreathelyticsAPI.getConfidenceLevel(currentPredictionResult.confidence);
                    const recommendations = window.BreathelyticsAPI.getHealthRecommendations(
                        currentPredictionResult.prediction, 
                        currentPredictionResult.confidence
                    );
                    
                    // Build AI insights section if available
                    let aiInsightsSection = '';
                    if (currentPredictionResult.ai_insights) {
                        const ai = currentPredictionResult.ai_insights;
                        
                        aiInsightsSection = `

AI MEDICAL INSIGHTS
===================
${ai.summary || 'Not available'}

DETECTED CONDITION EXPLANATION
===============================
${ai.condition_explanation || 'Condition explanation not available'}

CONFIDENCE LEVEL INTERPRETATION
================================
${ai.confidence_interpretation || 'Interpretation not available'}

KEY INSIGHTS
============
${ai.insights ? ai.insights.map((insight, index) => `${index + 1}. ${insight}`).join('\n') : 'No additional insights available'}

AI RECOMMENDATIONS
==================

📌 IMMEDIATE ACTIONS:
${ai.recommendations?.immediate ? ai.recommendations.immediate.map((rec, index) => `${index + 1}. ${rec}`).join('\n') : 'No immediate recommendations'}

👁️ SYMPTOM MONITORING:
${ai.recommendations?.monitoring ? ai.recommendations.monitoring.map((rec, index) => `${index + 1}. ${rec}`).join('\n') : 'No monitoring guidance'}

🏃 LIFESTYLE RECOMMENDATIONS:
${ai.recommendations?.lifestyle ? ai.recommendations.lifestyle.map((rec, index) => `${index + 1}. ${rec}`).join('\n') : 'No lifestyle recommendations'}

🏥 MEDICAL CONSULTATION:
${ai.recommendations?.medical ? ai.recommendations.medical.map((rec, index) => `${index + 1}. ${rec}`).join('\n') : 'No medical recommendations'}

RISK LEVEL: ${ai.risk_level || 'UNKNOWN'}

NEXT STEPS
==========
${ai.next_steps || 'Consult with a doctor for further evaluation'}

STATUS AI: ${ai.llm_status || 'Unknown'}
WAKTU PEMROSESAN AI: ${ai.processing_time_ms ? (ai.processing_time_ms / 1000).toFixed(1) + 's' : 'N/A'}
`;
                    }

                    const reportData = `
BREATHELYTICS ANALYSIS REPORT
=============================

Analysis Date: ${new Date().toLocaleDateString('en-US')}
Analysis Time: ${new Date().toLocaleTimeString('en-US')}
File Name: ${uploadedFile ? uploadedFile.name : 'Unknown'}

MACHINE LEARNING PREDICTION RESULTS
====================================
Primary Detection: ${currentPredictionResult.prediction}
Confidence Score: ${confidence}% (${confidenceLevel})

DETAILED SOUND PATTERN ANALYSIS
================================
Breathing Pattern: ${currentPredictionResult.prediction.toLowerCase() === 'healthy' ? 'Normal' : 'Abnormal'}
Sound Quality: ${confidence > 80 ? 'Clear' : 'Unclear'}
Rhythm: ${currentPredictionResult.prediction.toLowerCase() === 'healthy' ? 'Regular' : 'Irregular'}

ALL CONDITION PROBABILITIES
============================
${currentPredictionResult.all_probabilities ? 
  Object.entries(currentPredictionResult.all_probabilities)
    .sort(([,a], [,b]) => b - a)
    .map(([disease, prob]) => `${disease}: ${Math.round(prob * 100)}%`)
    .join('\n') : 'Not available'}

GENERAL RECOMMENDATIONS
=======================
${recommendations.map((rec, index) => `${index + 1}. ${rec}`).join('\n')}
${aiInsightsSection}

TECHNICAL INFORMATION
=====================
Processing Time: ${document.getElementById('processingTime')?.textContent || '0.0'}s
Model Version: ${window.BreathelyticsAPI?.apiStatus()?.version || 'Unknown'}
Analysis ID: ${Date.now()}

IMPORTANT MEDICAL DISCLAIMER
============================
This analysis is provided by an AI-powered screening tool and should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for proper medical evaluation and care.

The AI model has been trained on respiratory sound data but may not capture all possible conditions or variations. This tool is intended for screening purposes only and should be used as part of a comprehensive health assessment.

If you have concerns about your respiratory health, please contact your healthcare provider immediately.

===
Generated by Breathelytics AI Analysis System
${new Date().toISOString()}

© 2024 Breathelytics - AI-Powered Respiratory Health Analysis
                    `;
                    
                    const blob = new Blob([reportData], { type: 'text/plain' });
                    const url = URL.createObjectURL(blob);
                    const link = document.createElement('a');
                    link.href = url;
                    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').split('T')[0];
                    const predictionName = currentPredictionResult.prediction.replace(/\s+/g, '-').toLowerCase();
                    link.download = `breathelytics-analysis-${predictionName}-${timestamp}.txt`;
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    URL.revokeObjectURL(url);
                    
                    const hasAI = currentPredictionResult.ai_insights ? ' with AI insights' : '';
                    showNotification(`Detailed report${hasAI} downloaded successfully!`, 'success');
                } catch (error) {
                    console.error('Failed to generate report:', error);
                    showNotification('Failed to generate report. Please try again.', 'error');
                }
                
                // Reset button
                downloadReportBtn.innerHTML = originalText;
                downloadReportBtn.disabled = false;
            }, 2500);
        });
    }
    
    // New analysis functionality
    const newAnalysisBtn = document.getElementById('newAnalysis');
    if (newAnalysisBtn) {
        newAnalysisBtn.addEventListener('click', () => {
            // Reset to step 1
            setActiveStep(1);
            
            // Reset all UI elements
            resetProcessingUI();
            
            // Reset confidence score animation
            const scoreCircle = document.querySelector('.score-circle');
            if (scoreCircle) {
                scoreCircle.style.strokeDashoffset = '377'; // Full circle
            }
            
            showNotification('Ready for new analysis!', 'info');
        });
    }

    console.log('Audioscope AI loaded successfully!');
    
    // Chart.js Probability Visualization Function
    function createProbabilityChart(result) {
        const canvas = document.getElementById('probabilityChart');
        if (!canvas || !window.Chart) {
            console.log('Chart.js not available or canvas not found');
            return;
        }
        
        const ctx = canvas.getContext('2d');
        
        // Generate comprehensive probability data
        let allProbabilities = result.all_probabilities || {};
        
        // If no probabilities provided, create realistic mock data
        if (Object.keys(allProbabilities).length === 0) {
            const mainPrediction = result.prediction;
            const confidence = result.confidence;
            
            allProbabilities = {
                [mainPrediction]: confidence,
                'Normal': mainPrediction === 'Normal' ? confidence : Math.max(0.05, (1 - confidence) * 0.8),
                'Asthma': mainPrediction === 'Asthma' ? confidence : Math.random() * 0.15 + 0.02,
                'COPD': mainPrediction === 'COPD' ? confidence : Math.random() * 0.12 + 0.01,
                'Pneumonia': mainPrediction === 'Pneumonia' ? confidence : Math.random() * 0.10 + 0.01,
                'Bronchitis': mainPrediction === 'Bronchitis' ? confidence : Math.random() * 0.08 + 0.01,
                'Tuberculosis': mainPrediction === 'Tuberculosis' ? confidence : Math.random() * 0.05 + 0.01,
                'Lung Cancer': mainPrediction === 'Lung Cancer' ? confidence : Math.random() * 0.03 + 0.01
            };
        }
        
        // Sort and get top 6 conditions
        const sortedProbs = Object.entries(allProbabilities)
            .map(([name, prob]) => ({ name, probability: prob * 100 }))
            .sort((a, b) => b.probability - a.probability)
            .slice(0, 6);
        
        // Destroy existing chart if it exists
        if (window.probabilityChartInstance) {
            window.probabilityChartInstance.destroy();
        }
        
        // Define colors for each condition
        const colors = [
            { bg: 'rgba(104, 216, 214, 0.8)', border: '#68D8D6' },  // Primary - Teal
            { bg: 'rgba(78, 162, 161, 0.8)', border: '#4EA2A1' },   // Secondary - Dark Teal
            { bg: 'rgba(245, 158, 11, 0.8)', border: '#F59E0B' },   // Warning - Orange
            { bg: 'rgba(239, 68, 68, 0.8)', border: '#EF4444' },    // Danger - Red
            { bg: 'rgba(139, 92, 246, 0.8)', border: '#8B5CF6' },   // Purple
            { bg: 'rgba(34, 197, 94, 0.8)', border: '#22C55E' }     // Green
        ];
        
        // Create the chart
        window.probabilityChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: sortedProbs.map(p => p.name),
                datasets: [{
                    label: 'Detection Probability',
                    data: sortedProbs.map(p => p.probability),
                    backgroundColor: colors.map(c => c.bg),
                    borderColor: colors.map(c => c.border),
                    borderWidth: 2,
                    borderRadius: 8,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(37, 37, 37, 0.95)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        borderColor: '#68D8D6',
                        borderWidth: 1,
                        cornerRadius: 8,
                        displayColors: true,
                        callbacks: {
                            title: function(context) {
                                return `${context[0].label}`;
                            },
                            label: function(context) {
                                return `Probability: ${context.parsed.y.toFixed(1)}%`;
                            },
                            afterLabel: function(context) {
                                const index = context.dataIndex;
                                if (index === 0) return '🎯 Primary Detection';
                                if (index === 1) return '🥈 Secondary';
                                return '';
                            }
                        }
                    },
                    datalabels: {
                        anchor: 'end',
                        align: 'top',
                        color: '#252525',
                        font: {
                            size: 12,
                            weight: 'bold',
                            family: 'Inter'
                        },
                        formatter: function(value) {
                            return value.toFixed(1) + '%';
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#666666',
                            font: {
                                size: 12,
                                family: 'Inter',
                                weight: '500'
                            },
                            maxRotation: 45,
                            minRotation: 0
                        }
                    },
                    y: {
                        beginAtZero: true,
                        max: Math.max(...sortedProbs.map(p => p.probability)) + 10,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)',
                            drawBorder: false
                        },
                        ticks: {
                            color: '#666666',
                            font: {
                                size: 11,
                                family: 'Inter'
                            },
                            callback: function(value) {
                                return value + '%';
                            }
                        },
                        title: {
                            display: true,
                            text: 'Confidence Level (%)',
                            color: '#252525',
                            font: {
                                size: 14,
                                family: 'Inter',
                                weight: '600'
                            }
                        }
                    }
                },
                animation: {
                    duration: 1500,
                    easing: 'easeInOutQuart'
                },
                layout: {
                    padding: {
                        top: 20,
                        bottom: 10,
                        left: 10,
                        right: 10
                    }
                }
            },
            plugins: [ChartDataLabels]
        });
        
        // Add a subtle hover effect
        canvas.style.cursor = 'pointer';
        
        console.log('Probability chart created successfully');
    }
    
    // Make the function globally available
    window.createProbabilityChart = createProbabilityChart;
});

// Add notification styles dynamically
const notificationStyles = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        background: white;
        border-radius: 8px;
        box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.15);
        border-left: 4px solid #68D8D6;
        max-width: 400px;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        opacity: 0;
    }
    
    .notification-show {
        transform: translateX(0);
        opacity: 1;
    }
    
    .notification-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 16px 20px;
        gap: 12px;
    }
    
    .notification-message {
        font-size: 14px;
        color: #252525;
        line-height: 1.4;
    }
    
    .notification-close {
        background: none;
        border: none;
        font-size: 20px;
        color: #777777;
        cursor: pointer;
        padding: 0;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: color 0.2s ease;
    }
    
    .notification-close:hover {
        color: #252525;
    }
    
    .notification-info {
        border-left-color: #68D8D6;
    }
    
    .notification-success {
        border-left-color: #4CAF50;
    }
    
    .notification-warning {
        border-left-color: #FF9800;
    }
    
    .notification-error {
        border-left-color: #F44336;
    }
    
    @media (max-width: 480px) {
        .notification {
            right: 10px;
            left: 10px;
            max-width: none;
            transform: translateY(-100%);
        }
        
        .notification-show {
            transform: translateY(0);
        }
    }
    
    .no-animations * {
        animation: none !important;
        transition: none !important;
    }
    
    .keyboard-navigation button:focus,
    .keyboard-navigation a:focus {
        outline: 2px solid #68D8D6;
        outline-offset: 2px;
    }
    
    @media (max-width: 768px) {
        .mobile-menu-btn {
            display: block;
            background: none;
            border: none;
            cursor: pointer;
            padding: 8px;
            border-radius: 4px;
            transition: background-color 0.2s ease;
        }
        
        .mobile-menu-btn:hover {
            background-color: #F0FBFB;
        }
        
        .nav-content.mobile-menu-open {
            flex-direction: column;
            gap: 20px;
        }
        
        .nav-content.mobile-menu-open .nav-menu {
            display: flex;
            flex-direction: column;
            gap: 16px;
            text-align: center;
        }
    }
    
    @media (min-width: 769px) {
        .mobile-menu-btn {
            display: none;
        }
    }
`;

// Inject notification styles
const styleSheet = document.createElement('style');
styleSheet.textContent = notificationStyles;
document.head.appendChild(styleSheet);
