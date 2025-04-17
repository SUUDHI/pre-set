import { authAPI, utils } from './api.js';

document.addEventListener('DOMContentLoaded', () => {
    // Tab switching
    const tabButtons = document.querySelectorAll('.tab-btn');
    const authForms = document.querySelectorAll('.auth-form');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tab = button.dataset.tab;
            
            // Update active tab button
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Show corresponding form
            authForms.forEach(form => {
                form.classList.remove('active');
                if (form.id === `${tab}-form`) {
                    form.classList.add('active');
                }
            });
        });
    });

    // Login form submission
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;

            if (!utils.validateEmail(email)) {
                utils.showError('Please enter a valid email address');
                return;
            }

            try {
                const response = await authAPI.login(email, password);
                
                if (response.token) {
                    localStorage.setItem('token', response.token);
                    localStorage.setItem('user', JSON.stringify(response.user));
                    if (response.role === 'driver') {
                        window.location.href = '/driver/dashboard';
                    } else {
                        window.location.href = '/dashboard';
                    }
                } else {
                    utils.showError(response.message || 'Login failed');
                }
            } catch (error) {
                utils.showError('An error occurred during login');
            }
        });
    }

    // Register form submission
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const name = document.getElementById('register-name').value;
            const email = document.getElementById('register-email').value;
            const phone = document.getElementById('register-phone').value;
            const password = document.getElementById('register-password').value;
            const birth = document.getElementById('register-birth').value;
            const gender = document.getElementById('register-gender').value;
            const role = document.getElementById('register-role').value;

            // Validate all required fields
            if (!name || !email || !phone || !password || !birth || !gender || !role) {
                utils.showError('Please fill in all required fields');
                return;
            }

            // Validate phone number format (10 digits)
            if (!/^\d{10}$/.test(phone)) {
                utils.showError('Phone number must be exactly 10 digits');
                return;
            }

            // Validate email format
            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
                utils.showError('Please enter a valid email address');
                return;
            }

            // Validate password length
            if (password.length < 8) {
                utils.showError('Password must be at least 8 characters long');
                return;
            }

            const userData = {
                name,
                email,
                phone,
                password,
                birth,
                gender,
                role
            };

            // Add driver-specific fields if registering as a driver
            if (role === 'driver') {
                const licenseNumber = document.getElementById('license-number').value;
                const licensePlate = document.getElementById('license-plate').value;
                const vehicleType = document.getElementById('vehicle-type').value;

                if (!licenseNumber || !licensePlate || !vehicleType) {
                    utils.showError('Please fill in all driver-specific fields');
                    return;
                }

                userData.licenseNumber = licenseNumber;
                userData.licensePlate = licensePlate;
                userData.vehicleType = vehicleType;
            }

            try {
                console.log('Attempting registration with data:', userData);
                const response = await authAPI.register(userData);
                console.log('Registration response:', response);

                if (response.success) {
                    utils.showSuccess('Registration successful! Please login.');
                    // Clear form
                    document.getElementById('registerForm').reset();
                    // Switch to login tab
                    document.querySelector('.tab-btn[data-tab="login"]').click();
                } else {
                    utils.showError(response.message || 'Registration failed');
                }
            } catch (error) {
                console.error('Registration error:', error);
                utils.showError(error.message || 'An error occurred during registration');
            }
        });

        // Show/hide driver fields based on role selection
        const roleSelect = document.getElementById('register-role');
        const driverFields = document.getElementById('driver-fields');

        if (roleSelect && driverFields) {
            roleSelect.addEventListener('change', () => {
                if (roleSelect.value === 'driver') {
                    driverFields.classList.remove('hidden');
                } else {
                    driverFields.classList.add('hidden');
                }
            });
        }
    }

    // Logout functionality
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async () => {
            try {
                await authAPI.logout();
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                window.location.href = '/';
            } catch (error) {
                utils.showError('An error occurred during logout');
            }
        });
    }

    // Check authentication status
    const checkAuth = () => {
        const token = localStorage.getItem('token');
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        
        if (token && user.id) {
            // User is logged in
            const authSection = document.getElementById('auth-section');
            const rideSection = document.getElementById('ride-section');
            
            if (authSection) authSection.classList.remove('active');
            if (rideSection) rideSection.classList.add('active');
            
            // Update user info in header
            const userName = document.getElementById('user-name');
            if (userName) {
                userName.textContent = user.name;
            }
        } else {
            // User is not logged in
            const authSection = document.getElementById('auth-section');
            const rideSection = document.getElementById('ride-section');
            
            if (authSection) authSection.classList.add('active');
            if (rideSection) rideSection.classList.remove('active');
        }
    };

    // Initial auth check
    checkAuth();

    // Form validation
    function validatePhone(phone) {
        const phoneRegex = /^\+?1?\d{9,15}$/;
        return phoneRegex.test(phone);
    }
    
    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    function validatePassword(password) {
        return password.length >= 8;
    }
    
    // Add input validation listeners
    document.getElementById('registerPhone').addEventListener('input', function(e) {
        if (!validatePhone(e.target.value)) {
            e.target.setCustomValidity('Please enter a valid phone number');
        } else {
            e.target.setCustomValidity('');
        }
    });
    
    document.getElementById('registerEmail').addEventListener('input', function(e) {
        if (!validateEmail(e.target.value)) {
            e.target.setCustomValidity('Please enter a valid email address');
        } else {
            e.target.setCustomValidity('');
        }
    });
    
    document.getElementById('registerPassword').addEventListener('input', function(e) {
        if (!validatePassword(e.target.value)) {
            e.target.setCustomValidity('Password must be at least 8 characters long');
        } else {
            e.target.setCustomValidity('');
        }
    });
}); 