const API_BASE_URL = 'http://127.0.0.1:5000';

class API {
    constructor() {
        this.token = localStorage.getItem('authToken');
    }

    async request(endpoint, options = {}) {
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        try {
            console.log(`Making request to: ${API_BASE_URL}${endpoint}`);
            console.log('Request options:', { ...options, headers });
            
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                ...options,
                headers
            });

            console.log('Response status:', response.status);
            const data = await response.json();
            console.log('Response data:', data);

            if (!response.ok) {
                throw new Error(data.message || 'API request failed');
            }

            return data;
        } catch (error) {
            console.error('API request error:', error);
            throw error;
        }
    }

    setToken(token) {
        this.token = token;
        localStorage.setItem('authToken', token);
    }

    clearToken() {
        this.token = null;
        localStorage.removeItem('authToken');
    }
}

export const authAPI = {
    async login(email, password) {
        return new API().request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
    },

    async register(userData) {
        return new API().request('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    },

    async logout() {
        const response = await new API().request('/auth/logout', {
            method: 'POST'
        });
        new API().clearToken();
        return response;
    }
};

export const rideAPI = {
    async requestRide(rideData) {
        return new API().request('/rides/request', {
            method: 'POST',
            body: JSON.stringify(rideData)
        });
    },

    async cancelRide(rideId) {
        return new API().request(`/rides/${rideId}/cancel`, {
            method: 'POST'
        });
    },

    async getRideStatus(rideId) {
        return new API().request(`/rides/${rideId}/status`);
    },

    async getRideHistory() {
        return new API().request('/rides/history');
    }
};

export const driverAPI = {
    async updateLocation(location) {
        return new API().request('/driver/location', {
            method: 'PUT',
            body: JSON.stringify(location)
        });
    },

    async updateStatus(status) {
        return new API().request('/driver/status', {
            method: 'PUT',
            body: JSON.stringify({ status })
        });
    },

    async getEarnings() {
        return new API().request('/driver/earnings');
    },

    async getCurrentRide() {
        return new API().request('/driver/current-ride');
    },

    async getRequestedRides() {
        return new API().request('/driver/rides/requested');
    }
};

export const userAPI = {
    async getProfile() {
        return new API().request('/user/profile');
    },

    async updateProfile(profileData) {
        return new API().request('/user/profile', {
            method: 'PUT',
            body: JSON.stringify(profileData)
        });
    },

    async updatePaymentMethod(paymentData) {
        return new API().request('/user/payment', {
            method: 'PUT',
            body: JSON.stringify(paymentData)
        });
    },

    register: async (userData) => {
        try {
            console.log('Sending registration request to:', `${API_BASE_URL}/auth/register`);
            console.log('Request data:', userData);
            
            const response = await fetch(`${API_BASE_URL}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            });

            const data = await response.json();
            console.log('Registration API response:', data);

            if (!response.ok) {
                throw new Error(data.message || 'Registration failed');
            }

            return data;
        } catch (error) {
            console.error('Registration API error:', error);
            throw error;
        }
    }
};

// Utility functions
const utils = {
    showError: (message) => {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'alert alert-danger';
        errorDiv.textContent = message;
        document.body.appendChild(errorDiv);
        setTimeout(() => errorDiv.remove(), 3000);
    },

    showSuccess: (message) => {
        const successDiv = document.createElement('div');
        successDiv.className = 'alert alert-success';
        successDiv.textContent = message;
        document.body.appendChild(successDiv);
        setTimeout(() => successDiv.remove(), 3000);
    },

    validateEmail: (email) => {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },

    validatePhone: (phone) => {
        const re = /^\+?[\d\s-]{10,}$/;
        return re.test(phone);
    },

    formatCurrency: (amount) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    },

    formatDate: (date) => {
        return new Date(date).toLocaleString();
    }
};

export { utils }; 