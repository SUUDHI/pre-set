document.addEventListener('DOMContentLoaded', () => {
    // Tab switching
    const tabs = document.querySelectorAll('.tab-btn');
    const forms = document.querySelectorAll('.auth-form');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs and forms
            tabs.forEach(t => t.classList.remove('active'));
            forms.forEach(f => f.classList.remove('active'));

            // Add active class to clicked tab and corresponding form
            tab.classList.add('active');
            const formType = tab.dataset.tab;
            document.querySelector(`.auth-form[data-type="${formType}"]`).classList.add('active');
        });
    });

    // Form submissions
    const userForm = document.getElementById('user-register-form');
    const driverForm = document.getElementById('driver-register-form');

    userForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await handleRegistration(userForm, 'user');
    });

    driverForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await handleRegistration(driverForm, 'driver');
    });
});

async function handleRegistration(form, type) {
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    // Validate passwords match
    if (data.password !== data.confirm_password) {
        showError('Passwords do not match');
        return;
    }

    // Remove confirm_password from data
    delete data.confirm_password;

    try {
        const response = await fetch(`/api/${type}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            showSuccess(result.message);
            // Redirect to login page after 2 seconds
            setTimeout(() => {
                window.location.href = '/login';
            }, 2000);
        } else {
            showError(result.error || 'Registration failed');
        }
    } catch (error) {
        showError('An error occurred during registration');
        console.error('Registration error:', error);
    }
}

function showError(message) {
    // Create or get error message element
    let errorElement = document.querySelector('.error-message');
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'error-message';
        document.querySelector('.auth-box').appendChild(errorElement);
    }

    errorElement.textContent = message;
    errorElement.style.display = 'block';

    // Hide error after 5 seconds
    setTimeout(() => {
        errorElement.style.display = 'none';
    }, 5000);
}

function showSuccess(message) {
    // Create or get success message element
    let successElement = document.querySelector('.success-message');
    if (!successElement) {
        successElement = document.createElement('div');
        successElement.className = 'success-message';
        document.querySelector('.auth-box').appendChild(successElement);
    }

    successElement.textContent = message;
    successElement.style.display = 'block';

    // Hide success after 5 seconds
    setTimeout(() => {
        successElement.style.display = 'none';
    }, 5000);
} 