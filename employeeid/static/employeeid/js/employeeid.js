/**
 * Employee ID Card Generator - Main JavaScript
 * Handles all interactive functionality for the employee ID card system
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Handle print functionality
    const printButtons = document.querySelectorAll('.print-btn, .id-card-print');
    printButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            printIDCard();
        });
    });

    // Handle delete confirmation
    const deleteForms = document.querySelectorAll('.delete-form');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm('Are you sure you want to delete this employee record? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // Handle image preview for file uploads
    const imageInput = document.getElementById('id_photo');
    if (imageInput) {
        const imagePreview = document.getElementById('image-preview');
        
        imageInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                    imagePreview.style.display = 'block';
                }
                
                reader.readAsDataURL(file);
            }
        });
    }

    // Handle form validation
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

// Utility function to format dates
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

// Bulk Upload Functionality
function initializeBulkUpload() {
    const downloadTemplate = document.getElementById('downloadTemplate');
    
    if (downloadTemplate) {
        downloadTemplate.addEventListener('click', handleTemplateDownload);
    }
}

function handleTemplateDownload(e) {
    if (e) e.preventDefault();
    
    // CSV header row
    const headers = [
        'full_name',
        'employee_id',
        'designation',
        'department',
        'company',
        'contact',
        'email',
        'join_date (YYYY-MM-DD)'
    ];
    
    // Create example data
    const example = [
        'John Doe',
        'EMP' + Math.floor(1000 + Math.random() * 9000),
        'Software Developer',
        'IT',
        'StudyShala',
        '1234567890',
        'example@studyshala.com',
        new Date().toISOString().split('T')[0]
    ];
    
    // Create CSV content
    let csvContent = 'data:text/csv;charset=utf-8,';
    csvContent += headers.join(',') + '\r\n';
    csvContent += example.join(',') + '\r\n';
    
    // Create download link
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', 'employee_import_template.csv');
    document.body.appendChild(link);
    
    // Trigger download
    link.click();
    document.body.removeChild(link);
}

// Initialize bulk upload when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Existing initialization code...
    
    // Initialize bulk upload if on bulk upload page
    if (document.getElementById('downloadTemplate')) {
        initializeBulkUpload();
    }
});

// ID Card Print Functionality
function printIDCard() {
    // Store the original body content and classes
    const originalContent = document.body.innerHTML;
    const originalClasses = document.body.className;
    
    // Get the ID card content
    const idCard = document.querySelector('.id-card');
    if (!idCard) {
        // If not on ID card page, try to open the print URL
        const printUrl = window.location.href.includes('?') 
            ? window.location.href + '&print=true'
            : window.location.href + '?print=true';
        window.open(printUrl, '_blank');
        return;
    }
    
    // Create print content
    const printContent = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Print ID Card</title>
            <style>
                @page { size: auto; margin: 0mm; }
                body { 
                    margin: 0; 
                    padding: 10px; 
                    display: flex; 
                    justify-content: center; 
                    align-items: center;
                    min-height: 100vh;
                    background: white !important;
                }
                .id-card {
                    transform: scale(1);
                    transform-origin: center;
                }
            </style>
        </head>
        <body>
            ${idCard.outerHTML}
            <script>
                // Auto-print and close
                window.onload = function() {
                    setTimeout(function() {
                        window.print();
                        setTimeout(window.close, 100);
                    }, 300);
                };
            </script>
        </body>
        </html>
    `;
    
    // Open print window
    const printWindow = window.open('', '_blank');
    printWindow.document.open();
    printWindow.document.write(printContent);
    printWindow.document.close();
}

// Export functions for use in other files if needed
window.EmployeeID = {
    formatDate: formatDate,
    handleTemplateDownload: handleTemplateDownload,
    printIDCard: printIDCard
};
