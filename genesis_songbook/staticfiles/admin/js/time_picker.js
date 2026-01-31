// Custom time picker for show times - 30 minute intervals from 9am
document.addEventListener('DOMContentLoaded', function() {
    // Find all datetime inputs
    const datetimeInputs = document.querySelectorAll('input[type="datetime-local"]');
    
    datetimeInputs.forEach(function(input) {
        // Set min time to 09:00 and step to 30 minutes
        if (input.name === 'date') {
            // Create time options for dropdown if browser doesn't support datetime-local properly
            input.addEventListener('focus', function() {
                // Ensure the time part defaults to 19:30 (7:30 PM) if empty
                if (!this.value) {
                    const today = new Date();
                    const defaultTime = new Date(today.getFullYear(), today.getMonth(), today.getDate(), 19, 30);
                    this.value = defaultTime.toISOString().slice(0, 16);
                }
            });
        }
    });
});