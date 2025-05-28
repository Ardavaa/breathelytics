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
