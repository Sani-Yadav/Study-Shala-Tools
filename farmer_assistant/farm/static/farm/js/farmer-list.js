/**
 * Farmer List Page JavaScript
 * Contains functionality specific to the farmer list page
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeDeleteButtons();
    initializeWeatherModals();
    initializeTooltips();
});

/**
 * Initialize delete confirmation for farmer records
 */
function initializeDeleteButtons() {
    const deleteButtons = document.querySelectorAll('.delete-farmer');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('क्या आप वाकई इस किसान को हटाना चाहते हैं?')) {
                e.preventDefault();
            }
        });
    });
}

/**
 * Initialize weather modals for each farmer
 */
function initializeWeatherModals() {
    // Add any weather modal specific initialization here
    const weatherButtons = document.querySelectorAll('[data-bs-toggle="modal"]');
    
    weatherButtons.forEach(button => {
        button.addEventListener('click', function() {
            const farmerId = this.getAttribute('data-farmer-id');
            // You can add code here to fetch and display weather data
            // for the specific farmer's location
        });
    });
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Show loading state on a button
 * @param {HTMLElement} button - The button element
 */
function showLoading(button) {
    if (!button) return;
    
    const originalHTML = button.innerHTML;
    button.setAttribute('data-original-html', originalHTML);
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>लोड हो रहा है...';
}

/**
 * Hide loading state on a button
 * @param {HTMLElement} button - The button element
 */
function hideLoading(button) {
    if (!button) return;
    
    const originalHTML = button.getAttribute('data-original-html');
    if (originalHTML) {
        button.innerHTML = originalHTML;
    }
    button.disabled = false;
}

/**
 * Refresh weather data for a specific farmer
 * @param {string} farmerId - The ID of the farmer
 */
function refreshWeatherData(farmerId) {
    const refreshButton = document.querySelector(`#refresh-weather-${farmerId}`);
    if (refreshButton) {
        showLoading(refreshButton);
        
        // Simulate API call
        setTimeout(() => {
            console.log(`Refreshing weather data for farmer ${farmerId}`);
            hideLoading(refreshButton);
            showToast('मौसम डेटा अपडेट किया गया', 'success');
        }, 1000);
    }
}

/**
 * Show a toast notification
 * @param {string} message - The message to display
 * @param {string} type - The type of notification (success, danger, warning, info)
 */
function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) return;
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;

    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();

    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}
