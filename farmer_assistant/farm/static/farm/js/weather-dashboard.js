/**
 * Weather Dashboard JavaScript
 * Handles all interactive features for the weather dashboard
 */

document.addEventListener('DOMContentLoaded', function() {
    // Auto-refresh weather data every 10 minutes
    setTimeout(function() {
        window.location.reload();
    }, 10 * 60 * 1000);

    // Initialize weather dashboard functionality
    initWeatherDashboard();
});

function initWeatherDashboard() {
    console.log('Weather Dashboard initialized');
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Handle location input
    const locationInput = document.querySelector('.location-input');
    if (locationInput) {
        locationInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                const form = locationInput.closest('form');
                if (form) form.submit();
            }
        });
    }
    
    // Add click handlers for weather cards
    const weatherCards = document.querySelectorAll('.weather-card');
    weatherCards.forEach(card => {
        card.addEventListener('click', function() {
            // Toggle active state on click
            this.classList.toggle('active');
        });
    });
    
    // Initialize charts if any
    initWeatherCharts();
}

function initWeatherCharts() {
    // Initialize any weather charts here
    const chartElements = document.querySelectorAll('.weather-chart');
    if (chartElements.length > 0) {
        console.log('Initializing weather charts...');
        // Chart initialization code would go here
    }
}
