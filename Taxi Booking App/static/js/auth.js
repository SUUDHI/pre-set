// Form toggle functionality
function toggleAuth(type) {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const loginBtn = document.querySelector('.toggle-btn:nth-child(1)');
    const registerBtn = document.querySelector('.toggle-btn:nth-child(2)');
    
    if (type === 'login') {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
        loginBtn.classList.add('active');
        registerBtn.classList.remove('active');
    } else {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
        loginBtn.classList.remove('active');
        registerBtn.classList.add('active');
    }
    
    // Clear error message
    document.getElementById('error-message').textContent = '';
}

// Clear registration form
function clearRegistrationForm() {
    // Clear common fields
    document.getElementById('reg-name').value = '';
    document.getElementById('reg-email').value = '';
    document.getElementById('reg-phone').value = '';
    document.getElementById('reg-password').value = '';
    document.getElementById('reg-confirm-password').value = '';
    document.getElementById('reg-birth').value = '';
    document.getElementById('reg-gender').value = '';
    document.getElementById('reg-role').value = 'user';

    // Clear driver-specific fields
    document.getElementById('reg-license').value = '';
    document.getElementById('reg-plate').value = '';
    document.getElementById('reg-vehicle-type').value = '';

    // Hide driver fields
    document.getElementById('driver-fields').style.display = 'none';
}

// Toggle driver-specific fields
function toggleRegistrationFields() {
    const role = document.getElementById('reg-role').value;
    const driverFields = document.getElementById('driver-fields');
    const driverInputs = document.querySelectorAll('.driver-field');
    
    if (role === 'driver') {
        driverFields.style.display = 'block';
        driverInputs.forEach(input => {
            input.required = true;
            input.disabled = false;
        });
    } else {
        driverFields.style.display = 'none';
        driverInputs.forEach(input => {
            input.required = false;
            input.disabled = true;
            input.value = ''; // Clear the values
        });
    }
}

// Handle login form submission
if (document.getElementById('loginForm')) {
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        const role = document.getElementById('login-role').value;
        
        try {
            const response = await fetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password, role })
            });

            const data = await response.json();
            
            if (response.ok) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('role', role);
                localStorage.setItem('email', email);
                
                // Redirect based on role
                if (role === 'driver') {
                    window.location.href = '/driver-dashboard';
                } else {
                    window.location.href = '/user-dashboard';
                }
            } else {
                document.getElementById('error-message').textContent = data.error || 'Login failed';
            }
        } catch (error) {
            document.getElementById('error-message').textContent = 'An error occurred during login';
        }
    });
}

// Handle registration form submission
if (document.getElementById('registerForm')) {
    document.getElementById('registerForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Validate password match
        const password = document.getElementById('reg-password').value;
        const confirmPassword = document.getElementById('reg-confirm-password').value;
        
        if (password !== confirmPassword) {
            document.getElementById('error-message').textContent = 'Passwords do not match';
            return;
        }
        
        // Gather form data
        const formData = {
            role: document.getElementById('reg-role').value,
            name: document.getElementById('reg-name').value,
            email: document.getElementById('reg-email').value,
            phone: document.getElementById('reg-phone').value,
            password: password,
            birth: document.getElementById('reg-birth').value,
            gender: document.getElementById('reg-gender').value.toLowerCase()
        };
        
        // Add driver-specific fields if role is driver
        if (formData.role === 'driver') {
            const vehicleType = document.getElementById('reg-vehicle-type').value;
            const licensePlate = document.getElementById('reg-plate').value;
            const licenseNumber = document.getElementById('reg-license').value;
            
            // Validate driver-specific fields
            if (!vehicleType || !licensePlate || !licenseNumber) {
                document.getElementById('error-message').textContent = 'Please fill in all driver-specific fields';
                return;
            }
            
            formData.vehicleTypeId = parseInt(vehicleType);
            formData.licensePlate = licensePlate;
            formData.licenseNumber = licenseNumber;
        }
        
        try {
            const response = await fetch('/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();
            
            if (response.ok) {
                // Clear the form
                clearRegistrationForm();
                
                // Show success message and switch to login form
                document.getElementById('error-message').textContent = 'Registration successful! Please login.';
                document.getElementById('error-message').style.color = 'green';
                setTimeout(() => toggleAuth('login'), 2000);
            } else {
                document.getElementById('error-message').textContent = data.error || 'Registration failed';
                document.getElementById('error-message').style.color = 'red';
            }
        } catch (error) {
            document.getElementById('error-message').textContent = 'An error occurred during registration';
            document.getElementById('error-message').style.color = 'red';
        }
    });
}

// Check if user is logged in
function checkAuth() {
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');
    const currentPage = window.location.pathname;
    
    // Don't redirect if already on home page
    if (currentPage === '/') {
        return;
    }
    
    if (!token) {
        window.location.href = '/';
        return;
    }

    // Redirect if on wrong dashboard
    if (role === 'user' && currentPage.includes('driver')) {
        window.location.href = '/user-dashboard';
    } else if (role === 'driver' && currentPage.includes('user')) {
        window.location.href = '/driver-dashboard';
    }
}

// Handle logout
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('email');
    window.location.href = '/';
}

// Display user email in dashboard
function displayUserEmail() {
    const email = localStorage.getItem('email');
    const userEmailElement = document.getElementById('userEmail') || document.getElementById('driverEmail');
    if (userEmailElement && email) {
        userEmailElement.textContent = email;
    }
}

// Run on page load
if (!window.location.pathname.includes('index')) {
    checkAuth();
    displayUserEmail();
} 