// Audioscope AI - JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Mobile menu toggle
    const navbar = document.querySelector('.navbar');
    const navContent = document.querySelector('.nav-content');
    
    // Add mobile menu button
    const mobileMenuBtn = document.createElement('button');
    mobileMenuBtn.classList.add('mobile-menu-btn');
    mobileMenuBtn.innerHTML = `
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M3 12h18M3 6h18M3 18h18" stroke="#252525" stroke-width="2" stroke-linecap="round"/>
        </svg>
    `;
    
    // Mobile menu toggle functionality
    let isMobileMenuOpen = false;
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
            
            // Here you would typically navigate to the diagnosis page
            // For now, we'll just show an alert
            showNotification('Diagnosis feature coming soon!', 'info');
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

    // Notification system
    function showNotification(message, type = 'info') {
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
        
        // Auto hide after 3 seconds
        const autoHide = setTimeout(() => {
            hideNotification(notification);
        }, 3000);
        
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
    });    // Tab System
    const tabNavLinks = document.querySelectorAll('.nav-link[data-tab]');
    const tabPanels = document.querySelectorAll('.tab-panel');
      function switchTab(targetTab) {
        // Remove active class from all nav links
        tabNavLinks.forEach(link => link.classList.remove('active'));
        
        // Remove active class from all tab panels
        tabPanels.forEach(panel => panel.classList.remove('active'));
        
        // Add active class to clicked nav link
        const targetLink = document.querySelector(`[data-tab="${targetTab}"]`);
        if (targetLink) targetLink.classList.add('active');
        
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
      // Predict Page Functionality
    const uploadArea = document.getElementById('uploadArea');
    const audioFileInput = document.getElementById('audioFileInput');
    const uploadBrowseBtn = document.querySelector('.upload-browse');
    const stepItems = document.querySelectorAll('.step-item');
    const stepContents = document.querySelectorAll('.step-content-container .step-content');
    
    if (uploadArea && audioFileInput) {
        // File upload drag and drop
        uploadArea.addEventListener('click', () => {
            audioFileInput.click();
        });

        if (uploadBrowseBtn) {
            uploadBrowseBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                audioFileInput.click();
            });
        }
        
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
    
    function handleFileUpload(file) {
        // Validate file type
        const allowedTypes = ['audio/wav', 'audio/mp3', 'audio/mpeg', 'audio/m4a'];
        if (!allowedTypes.includes(file.type) && !file.name.match(/\.(wav|mp3|m4a)$/i)) {
            showNotification('Please upload a valid audio file (.wav, .mp3, .m4a)', 'error');
            return;
        }
        
        // Validate file size (max 10MB)
        if (file.size > 10 * 1024 * 1024) {
            showNotification('File size must be less than 10MB', 'error');
            return;
        }
        
        showNotification(`File "${file.name}" uploaded successfully!`, 'success');
        
        // Start processing with a smooth transition
        setTimeout(() => {
            startProcessing();
        }, 800);
    }
    
    function startProcessing() {
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
            'Extracting audio features...',
            'Analyzing frequency patterns...',
            'Running AI classification...',
            'Generating detailed report...'
        ];

        const progressInterval = setInterval(() => {
            progress += Math.random() * 8 + 2; // More controlled progress
            timeElapsed += 0.3;
            
            // Update progress visuals
            if (progress > 100) progress = 100;
            if (progressBar) progressBar.style.width = `${progress}%`;
            if (progressPercentage) progressPercentage.textContent = `${Math.round(progress)}%`;
            if (processingTime) processingTime.textContent = timeElapsed.toFixed(1);
            
            // Update processing steps
            const stepProgress = progress / 25; // Each step is 25% of progress
            const newStepIndex = Math.min(Math.floor(stepProgress), 3);
            
            if (newStepIndex > currentStepIndex && processSteps[newStepIndex]) {
                // Complete previous step
                if (processSteps[currentStepIndex]) {
                    processSteps[currentStepIndex].classList.remove('active');
                    processSteps[currentStepIndex].classList.add('completed');
                }
                
                // Activate new step
                processSteps[newStepIndex].classList.add('active');
                currentStepIndex = newStepIndex;
                
                // Update status message
                if (processingStatus && statusMessages[newStepIndex]) {
                    processingStatus.textContent = statusMessages[newStepIndex];
                }
            }
            
            if (progress >= 100) {
                clearInterval(progressInterval);
                
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
            }
        }, 300);
    }
    
    function showResults() {
        // Move to step 3
        setActiveStep(3);
        
        // Animate the confidence score
        setTimeout(() => {
            const scoreCircle = document.querySelector('.score-circle');
            if (scoreCircle) {
                const circumference = 2 * Math.PI * 60; // radius = 60
                const targetScore = 87; // 87% confidence
                const offset = circumference - (targetScore / 100) * circumference;
                
                scoreCircle.style.strokeDashoffset = offset;
            }
        }, 500);
        
        showNotification('Analysis complete! Your results are ready.', 'success');
    }
    
    function setActiveStep(stepNumber) {
        // Update step indicators
        stepItems.forEach((item, index) => {
            item.classList.remove('active', 'completed');
            
            if (index + 1 === stepNumber) {
                item.classList.add('active');
            } else if (index + 1 < stepNumber) {
                item.classList.add('completed');
            }
        });
        
        // Update step content
        stepContents.forEach((content, index) => {
            content.classList.remove('active');
            
            if (index + 1 === stepNumber) {
                content.classList.add('active');
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
    }
    
    // Download report functionality
    const downloadReportBtn = document.getElementById('downloadReport');
    if (downloadReportBtn) {
        downloadReportBtn.addEventListener('click', () => {
            // Add loading state
            const originalText = downloadReportBtn.innerHTML;
            downloadReportBtn.innerHTML = `
                <div class="spinner" style="width: 20px; height: 20px; border-width: 2px;"></div>
                <span>Generating Report...</span>
            `;
            downloadReportBtn.disabled = true;
            
            showNotification('Generating detailed report...', 'info');
            
            setTimeout(() => {
                // Create a mock PDF download
                const reportData = `
                    Breathelytics Analysis Report
                    ============================
                    
                    Analysis Date: ${new Date().toLocaleDateString()}
                    Confidence Score: 87%
                    
                    Results: Normal Respiratory Function
                    
                    Detailed Analysis:
                    - Breathing Pattern: Normal
                    - Sound Quality: Clear
                    - Rhythm: Regular
                    
                    Recommendations:
                    - Continue regular exercise
                    - Avoid pollutants and smoking
                    - Annual check-ups recommended
                `;
                
                const blob = new Blob([reportData], { type: 'text/plain' });
                const url = URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.download = `breathelytics-report-${new Date().toISOString().split('T')[0]}.txt`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(url);
                
                // Reset button
                downloadReportBtn.innerHTML = originalText;
                downloadReportBtn.disabled = false;
                
                showNotification('Report downloaded successfully!', 'success');
            }, 2500);
        });
    }
    
    // New analysis functionality
    const newAnalysisBtn = document.getElementById('newAnalysis');
    if (newAnalysisBtn) {
        newAnalysisBtn.addEventListener('click', () => {
            // Reset to step 1
            setActiveStep(1);
            
            // Reset file input
            if (audioFileInput) audioFileInput.value = '';
            
            // Reset progress bar
            const progressBar = document.querySelector('.progress-fill');
            const progressPercentage = document.querySelector('.progress-percentage');
            if (progressBar) progressBar.style.width = '0%';
            if (progressPercentage) progressPercentage.textContent = '0%';
            
            // Reset processing time
            const processingTime = document.getElementById('processingTime');
            if (processingTime) processingTime.textContent = '0.0';
            
            // Reset processing status
            const processingStatus = document.getElementById('processingStatus');
            if (processingStatus) processingStatus.textContent = 'Extracting audio features...';
            
            // Reset process steps
            const processSteps = document.querySelectorAll('.process-step');
            processSteps.forEach((step, index) => {
                step.classList.remove('active', 'completed');
                if (index === 0) {
                    step.classList.add('completed');
                } else if (index === 1) {
                    step.classList.add('active');
                }
            });
            
            // Reset confidence score animation
            const scoreCircle = document.querySelector('.score-circle');
            if (scoreCircle) {
                scoreCircle.style.strokeDashoffset = '377'; // Full circle
            }
            
            showNotification('Ready for new analysis!', 'info');
        });
    }
      // Update CTA buttons to switch to predict tab
    const allCtaButtons = document.querySelectorAll('.cta-button, .hero-cta');
    allCtaButtons.forEach(button => {
        button.removeEventListener('click', button.clickHandler); // Remove old handler
        
        button.clickHandler = function() {
            // Add click animation
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
            
            // Switch to predict tab
            switchTab('predict');
        };
        
        button.addEventListener('click', button.clickHandler);
    });

    console.log('Audioscope AI loaded successfully!');
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
