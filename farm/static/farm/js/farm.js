/**
 * Farm Module - Main JavaScript
 * Handles interactive functionality for the farm management system
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-refresh weather data every 10 minutes
    if (document.querySelector('.weather-dashboard')) {
        setInterval(function() {
            const location = document.querySelector('input[name="location"]')?.value;
            if (location) {
                fetchWeatherData(location);
            }
        }, 600000); // 10 minutes
    }

    // Handle form submissions with loading state
    const forms = document.querySelectorAll('.farm-form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
            }
        });
    });
});

/**
 * Fetch weather data via AJAX
 * @param {string} location - Location to fetch weather for
 */
function fetchWeatherData(location) {
    const weatherContainer = document.querySelector('.weather-container');
    if (!weatherContainer) return;

    // Show loading state
    weatherContainer.innerHTML = `
        <div class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2">Updating weather data...</p>
        </div>
    `;

    // Make AJAX request
    fetch(`/farm/weather/?location=${encodeURIComponent(location)}`)
        .then(response => response.text())
        .then(html => {
            // This will refresh the whole page with new data
            document.documentElement.innerHTML = html;
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
            weatherContainer.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Failed to update weather data. Please try again later.
                </div>
                ${weatherContainer.innerHTML}
            `;
        });
}

/**
 * Format date to local string
 * @param {string} dateString - ISO date string
 * @returns {string} Formatted date
 */
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleString(undefined, options);
}

// Export functions for use in other files if needed
window.FarmModule = {
    fetchWeatherData,
    formatDate
};
