/**
 * Accounts App - Main JavaScript
 * Handles all interactive features for the accounts app
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeFormValidation();
    initializePasswordToggle();
    initializeAlerts();
});

/**
 * Initialize form validation
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('.account-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Toggle password visibility
 */
function initializePasswordToggle() {
    const passwordToggles = document.querySelectorAll('.password-toggle');
    
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const passwordField = this.previousElementSibling;
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            
            // Toggle icon
            this.querySelector('i').classList.toggle('fa-eye');
            this.querySelector('i').classList.toggle('fa-eye-slash');
        });
    });
}

/**
 * Auto-hide alerts after 5 seconds
 */
function initializeAlerts() {
    const alerts = document.querySelectorAll('.alert-dismissible');
    
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

/**
 * Show loading state on form submission
 * @param {HTMLElement} form - The form element
 */
function showFormLoading(form) {
    const submitButton = form.querySelector('button[type="submit"]');
    if (!submitButton) return;
    
    submitButton.disabled = true;
    submitButton.innerHTML = `
        <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
        Processing...
    `;
}

/**
 * Reset form loading state
 * @param {HTMLElement} form - The form element
 */
function resetFormLoading(form) {
    const submitButton = form.querySelector('button[type="submit"]');
    if (!submitButton) return;
    
    submitButton.disabled = false;
    submitButton.innerHTML = 'Submit';
}
