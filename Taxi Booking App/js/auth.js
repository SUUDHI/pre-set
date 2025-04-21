// Check if user is logged in
function checkAuth() {
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');
    
    if (!token) {
        window.location.href = '/index.html';
        return;
    }

    // Redirect if on wrong dashboard
    const currentPage = window.location.pathname;
    if (role === 'user' && currentPage.includes('driver')) {
        window.location.href = '/user-dashboard.html';
    } else if (role === 'driver' && currentPage.includes('user')) {
        window.location.href = '/driver-dashboard.html';
    }
}

// Handle login form submission
if (document.getElementById('loginForm')) {
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const role = document.getElementById('role').value;
        
        try {
            const response = await fetch('http://localhost:5000/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();
            
            if (response.ok) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('role', role);
                localStorage.setItem('email', email);
                
                // Redirect based on role
                if (role === 'driver') {
                    window.location.href = '/driver-dashboard.html';
                } else {
                    window.location.href = '/user-dashboard.html';
                }
            } else {
                document.getElementById('error-message').textContent = data.error || 'Login failed';
            }
        } catch (error) {
            document.getElementById('error-message').textContent = 'An error occurred during login';
        }
    });
}

// Handle logout
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('email');
    window.location.href = '/index.html';
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
if (!window.location.pathname.includes('index.html')) {
    checkAuth();
    displayUserEmail();
} 