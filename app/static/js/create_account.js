/**
 * FitSystem - Create Account Script
 * Manages the multi-step registration form and validation
 */

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts
    setupAutoDismissAlerts();
    
    // Social login buttons (for future implementation)
    document.querySelectorAll('.btn-social').forEach(button => {
        button.addEventListener('click', function() {
            showAlert('Esta función estará disponible próximamente', 'info');
        });
    });
});

/**
 * Sets up auto-dismissing for existing alerts
 */
function setupAutoDismissAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 150);
        }, 5000);
    });
}

/**
 * Validates email format
 * @param {string} email - The email to validate
 * @returns {boolean} - True if email is valid
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Validates password strength
 * @param {string} password - The password to validate
 * @returns {object} - Validation result with status and message
 */
function validatePassword(password) {
    const result = {
        valid: true,
        criteria: {
            length: password.length >= 8,
            uppercase: /[A-Z]/.test(password),
            lowercase: /[a-z]/.test(password),
            number: /[0-9]/.test(password),
            special: /[!@#$%^&*()_\-+={}[\]|:;'"<>,.?/]/.test(password)
        },
        message: ""
    };
    
    // Check if all criteria are met
    result.valid = Object.values(result.criteria).every(criterion => criterion);
    
    // Generate message based on failed criteria
    if (!result.valid) {
        const messages = [];
        if (!result.criteria.length) messages.push("al menos 8 caracteres");
        if (!result.criteria.uppercase) messages.push("una letra mayúscula");
        if (!result.criteria.lowercase) messages.push("una letra minúscula");
        if (!result.criteria.number) messages.push("un número");
        if (!result.criteria.special) messages.push("un carácter especial");
        
        result.message = "La contraseña debe contener: " + messages.join(", ");
    }
    
    return result;
}

/**
 * Shows an alert message
 * @param {string} message - The message to display
 * @param {string} type - The alert type (success, danger, warning, info)
 */
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.flash-container');
    
    if (!alertContainer) return;
    
    const alertElement = document.createElement('div');
    alertElement.className = `alert alert-${type} alert-dismissible fade show`;
    alertElement.role = 'alert';
    alertElement.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    alertContainer.appendChild(alertElement);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alertElement.classList.remove('show');
        setTimeout(() => alertElement.remove(), 150);
    }, 5000);
}