document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('mediaDownloadForm');
    if (!form) return;

    // Create and append alert container
    const alertContainer = document.createElement('div');
    alertContainer.className = 'alert-container position-fixed top-0 end-0 p-3';
    alertContainer.style.zIndex = '1100';
    document.body.appendChild(alertContainer);

    // Show alert function
    function showAlert(message, type = 'success') {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.role = 'alert';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        alertContainer.appendChild(alert);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 150);
        }, 5000);
    }

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        const submitButton = form.querySelector('button[type="submit"]');
        const urlInput = form.querySelector('input[name="url"]');
        const originalButtonText = submitButton.innerHTML;
        
        // Validate URL
        const url = urlInput.value.trim();
        if (!url) {
            showAlert('Please enter a valid URL', 'danger');
            urlInput.focus();
            return;
        }
        
        // Show loading state
        submitButton.disabled = true;
        submitButton.innerHTML = `
            <span class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
            Downloading...
        `;
        
        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'Failed to process your request');
            }
            
            if (data.status === 'success') {
                // Create download link and trigger it
                const link = document.createElement('a');
                link.href = data.download_url;
                link.download = data.filename || 'downloaded_media';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                
                showAlert('Download started successfully!', 'success');
            } else {
                throw new Error(data.message || 'Failed to download media');
            }
        } catch (error) {
            console.error('Error:', error);
            showAlert(error.message || 'An error occurred while processing your request', 'danger');
        } finally {
            // Reset button state
            submitButton.disabled = false;
            submitButton.innerHTML = originalButtonText;
            form.reset();
        }
    });
});
