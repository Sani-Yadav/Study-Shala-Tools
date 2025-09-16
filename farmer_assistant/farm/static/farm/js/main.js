/**
 * Main JavaScript file for common functionality
 * This file contains code that is used across multiple pages
 */

// Initialize when the document is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeTooltips();
    initializeModals();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    
    tooltipTriggerList.map(tooltipTriggerEl => 
        new bootstrap.Tooltip(tooltipTriggerEl)
    );
}

/**
 * Initialize Bootstrap modals
 */
function initializeModals() {
    // Initialize any modals that need special handling
    // Example: const myModal = new bootstrap.Modal(document.getElementById('myModal'));
}

// Show loading state on buttons
function showLoading(button) {
    if (!button) return;
    
    const originalText = button.innerHTML;
    button.setAttribute('data-original-text', originalText);
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
}

// Hide loading state on buttons
function hideLoading(button) {
    if (!button) return;
    
    const originalText = button.getAttribute('data-original-text');
    if (originalText) {
        button.innerHTML = originalText;
        button.disabled = false;
        button.removeAttribute('data-original-text');
    }
}
