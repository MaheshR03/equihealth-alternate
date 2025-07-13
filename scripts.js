document.addEventListener("DOMContentLoaded", function() {
    console.log("EquiHealth JavaScript loaded successfully");
    
    // Initialize all enhancements
    initializeNavbarEnhancements();
    initializeFormEnhancements();
    initializeFileUploadEnhancements();
    initializeFlashMessageEnhancements();
    initializePageTransitions();
    initializeAccessibilityFeatures();
});

// Enhanced Navigation Bar Interactions
function initializeNavbarEnhancements() {
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        // Add smooth hover effects
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px)';
            this.style.boxShadow = '0 6px 20px rgba(255, 255, 255, 0.2)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
        
        // Add active state for current page
        if (link.href === window.location.href) {
            link.style.background = 'rgba(255, 255, 255, 0.3)';
            link.style.fontWeight = '600';
        }
    });
}

// Enhanced Form Interactions
function initializeFormEnhancements() {
    const forms = document.querySelectorAll('form');
    const inputs = document.querySelectorAll('input[type="email"], input[type="password"], input[type="text"]');
    
    // Add real-time validation feedback
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.style.borderColor = 'rgba(255, 255, 255, 0.8)';
            this.style.transform = 'scale(1.02)';
        });
        
        input.addEventListener('blur', function() {
            this.style.borderColor = 'rgba(255, 255, 255, 0.3)';
            this.style.transform = 'scale(1)';
            validateInput(this);
        });
        
        input.addEventListener('input', function() {
            clearValidationMessage(this);
        });
    });
    
    // Enhanced form submission
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = 'Processing...';
                submitBtn.style.opacity = '0.7';
                submitBtn.disabled = true;
            }
        });
    });
}

// File Upload Enhancements
function initializeFileUploadEnhancements() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        // Create upload area
        const uploadArea = createUploadArea(input);
        
        // Add drag and drop functionality
        uploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.style.background = 'rgba(76, 175, 80, 0.2)';
            this.style.borderColor = 'rgba(76, 175, 80, 0.8)';
        });
        
        uploadArea.addEventListener('dragleave', function(e) {
            this.style.background = 'rgba(255, 255, 255, 0.1)';
            this.style.borderColor = 'rgba(255, 255, 255, 0.3)';
        });
        
        uploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                input.files = files;
                showFileInfo(files[0], uploadArea);
            }
        });
        
        // Handle file selection
        input.addEventListener('change', function() {
            if (this.files.length > 0) {
                showFileInfo(this.files[0], uploadArea);
            }
        });
    });
}

// Flash Message Enhancements
function initializeFlashMessageEnhancements() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        // Add close button
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '×';
        closeBtn.style.cssText = `
            position: absolute;
            top: 5px;
            right: 10px;
            background: none;
            border: none;
            color: inherit;
            font-size: 20px;
            cursor: pointer;
            opacity: 0.7;
        `;
        
        message.style.position = 'relative';
        message.appendChild(closeBtn);
        
        closeBtn.addEventListener('click', function() {
            message.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => message.remove(), 300);
        });
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (message.parentNode) {
                message.style.animation = 'slideOutRight 0.3s ease';
                setTimeout(() => message.remove(), 300);
            }
        }, 5000);
    });
}

// Page Transition Enhancements
function initializePageTransitions() {
    // Add loading indicator for navigation
    const navLinks = document.querySelectorAll('nav a:not(.logout-btn)');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.href !== window.location.href) {
                showLoadingIndicator();
            }
        });
    });
}

// Accessibility Enhancements
function initializeAccessibilityFeatures() {
    // Add keyboard navigation support
    document.addEventListener('keydown', function(e) {
        // Escape key to close flash messages
        if (e.key === 'Escape') {
            const flashMessages = document.querySelectorAll('.flash-message');
            flashMessages.forEach(msg => msg.remove());
        }
        
        // Alt + H for home navigation
        if (e.altKey && e.key === 'h') {
            e.preventDefault();
            window.location.href = '/';
        }
    });
    
    // Add focus indicators
    const focusableElements = document.querySelectorAll('a, button, input, select, textarea');
    focusableElements.forEach(element => {
        element.addEventListener('focus', function() {
            this.style.outline = '2px solid rgba(255, 255, 255, 0.8)';
            this.style.outlineOffset = '2px';
        });
        
        element.addEventListener('blur', function() {
            this.style.outline = 'none';
        });
    });
}

// Helper Functions
function validateInput(input) {
    const value = input.value.trim();
    let isValid = true;
    let message = '';
    
    if (input.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            message = 'Please enter a valid email address';
        }
    }
    
    if (input.type === 'password' && value) {
        if (value.length < 6) {
            isValid = false;
            message = 'Password must be at least 6 characters';
        }
    }
    
    if (!isValid) {
        showValidationMessage(input, message);
    }
}

function showValidationMessage(input, message) {
    clearValidationMessage(input);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'validation-error';
    errorDiv.textContent = message;
    errorDiv.style.cssText = `
        color: #ff6b6b;
        font-size: 12px;
        margin-top: 5px;
        animation: fadeIn 0.3s ease;
    `;
    
    input.parentNode.appendChild(errorDiv);
    input.style.borderColor = '#ff6b6b';
}

function clearValidationMessage(input) {
    const existingError = input.parentNode.querySelector('.validation-error');
    if (existingError) {
        existingError.remove();
    }
    input.style.borderColor = 'rgba(255, 255, 255, 0.3)';
}

function createUploadArea(input) {
    const uploadArea = document.createElement('div');
    uploadArea.style.cssText = `
        border: 2px dashed rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
        background: rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        cursor: pointer;
    `;
    
    uploadArea.innerHTML = `
        <p style="color: white; margin: 0;">
            <strong>Drag & drop your CSV file here</strong><br>
            <small>or click to browse</small>
        </p>
    `;
    
    uploadArea.addEventListener('click', () => input.click());
    input.parentNode.insertBefore(uploadArea, input);
    input.style.display = 'none';
    
    return uploadArea;
}

function showFileInfo(file, uploadArea) {
    uploadArea.innerHTML = `
        <p style="color: white; margin: 0;">
            <strong>📄 ${file.name}</strong><br>
            <small>${(file.size / 1024).toFixed(1)} KB</small>
        </p>
    `;
    uploadArea.style.background = 'rgba(76, 175, 80, 0.2)';
    uploadArea.style.borderColor = 'rgba(76, 175, 80, 0.8)';
}

function showLoadingIndicator() {
    const loader = document.createElement('div');
    loader.id = 'page-loader';
    loader.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    `;
    
    loader.innerHTML = `
        <div style="color: white; text-align: center;">
            <div style="border: 4px solid rgba(255,255,255,0.3); border-radius: 50%; border-top: 4px solid white; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto 10px;"></div>
            <p>Loading...</p>
        </div>
    `;
    
    document.body.appendChild(loader);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);
