// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Add active class to current nav link
    const currentLocation = location.href;
    const menuItems = document.querySelectorAll('.nav-link');
    const menuLength = menuItems.length;
    for (let i = 0; i < menuLength; i++) {
        if (menuItems[i].href === currentLocation) {
            menuItems[i].classList.add('active');
            menuItems[i].setAttribute('aria-current', 'page');
        }
    }

    // Handle file input labels
    const fileInputs = document.querySelectorAll('.custom-file-input');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            const fileName = e.target.files[0] ? e.target.files[0].name : 'Choose file';
            const label = this.nextElementSibling;
            if (label) {
                label.textContent = fileName;
            }
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});

// Utility function to show loading state on buttons
function setButtonLoading(button, isLoading) {
    if (isLoading) {
        button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
        button.disabled = true;
    } else {
        button.innerHTML = button.getAttribute('data-original-text');
        button.disabled = false;
    }
}

// Handle form submissions with loading state
document.addEventListener('submit', function(e) {
    const form = e.target;
    const submitButton = form.querySelector('button[type="submit"]');
    
    if (submitButton) {
        // Save original button text
        if (!submitButton.getAttribute('data-original-text')) {
            submitButton.setAttribute('data-original-text', submitButton.innerHTML);
        }
        
        // Set loading state
        setButtonLoading(submitButton, true);
        
        // Re-enable button after form submission is complete
        form.addEventListener('ajax:complete', function() {
            setButtonLoading(submitButton, false);
        });
    }
});
