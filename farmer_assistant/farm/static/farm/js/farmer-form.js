/**
 * Farmer Form JavaScript
 * Contains form validation and submission handling
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeFormValidation();
    initializeFormSubmissions();
});

/**
 * Initialize form validation
 */
function initializeFormValidation() {
    const form = document.querySelector('form.farmer-form');
    if (!form) return;

    // Phone number validation
    const phoneInput = form.querySelector('input[name="phone"]');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            const value = e.target.value.replace(/\D/g, '');
            e.target.value = value.slice(0, 10);
            
            // Validate phone number
            const isValid = /^[6-9]\d{9}$/.test(value);
            const feedback = e.target.nextElementSibling;
            
            if (value.length > 0) {
                if (isValid) {
                    e.target.classList.remove('is-invalid');
                    e.target.classList.add('is-valid');
                    if (feedback) feedback.textContent = '';
                } else {
                    e.target.classList.remove('is-valid');
                    e.target.classList.add('is-invalid');
                    if (feedback) {
                        feedback.textContent = 'कृपया मान्य फोन नंबर दर्ज करें';
                        feedback.className = 'invalid-feedback';
                    }
                }
            } else {
                e.target.classList.remove('is-valid', 'is-invalid');
                if (feedback) feedback.textContent = '';
            }
        });
    }

    // Form submission validation
    form.addEventListener('submit', function(e) {
        let isValid = true;
        
        // Check required fields
        const requiredFields = form.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.classList.add('is-invalid');
                
                const feedback = field.nextElementSibling;
                if (feedback && feedback.classList.contains('invalid-feedback')) {
                    feedback.textContent = 'यह फ़ील्ड आवश्यक है';
                }
            }
        });

        if (!isValid) {
            e.preventDefault();
            if (typeof showToast === 'function') {
                showToast('कृपया सभी आवश्यक फ़ील्ड भरें', 'error');
            }
        } else {
            // Disable submit button to prevent double submission
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                showLoading(submitButton);
            }
        }
    });
}

/**
 * Initialize form submission handling
 */
function initializeFormSubmissions() {
    // Add any additional form submission handling here
    // For example, AJAX form submission
    
    // Example: Handle file upload preview
    const fileInput = document.querySelector('input[type="file"]');
    const preview = document.getElementById('file-preview');
    
    if (fileInput && preview) {
        fileInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                }
                reader.readAsDataURL(file);
            }
        });
    }
}
