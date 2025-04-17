import { driverAPI, utils } from './api.js';
import { initMap, updateLocation } from './map.js';

class DriverDashboard {
    constructor() {
        this.currentRide = null;
        this.isOnline = false;
        this.locationInterval = null;
        this.initializeEventListeners();
        this.loadDriverProfile();
        this.initMap();
    }

    initializeEventListeners() {
        // Navigation
        document.querySelectorAll('.driver-menu a').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const section = e.target.closest('a').dataset.section;
                this.showSection(section);
            });
        });

        // Status toggle
        document.getElementById('toggle-status').addEventListener('click', () => {
            this.toggleStatus();
        });

        // Ride actions
        document.getElementById('accept-ride').addEventListener('click', () => {
            this.acceptRide();
        });

        document.getElementById('start-ride').addEventListener('click', () => {
            this.startRide();
        });

        document.getElementById('complete-ride').addEventListener('click', () => {
            this.completeRide();
        });

        // Profile form
        document.getElementById('profile-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.updateProfile();
        });

        // History filter
        document.getElementById('history-filter').addEventListener('change', () => {
            this.loadRideHistory();
        });
    }

    async loadDriverProfile() {
        try {
            const profile = await driverAPI.getProfile();
            this.updateProfileUI(profile);
        } catch (error) {
            utils.showError('Failed to load profile');
        }
    }

    updateProfileUI(profile) {
        document.getElementById('driver-name').textContent = profile.name;
        document.getElementById('driver-rating').textContent = profile.rating.toFixed(1);
        document.getElementById('total-rides').textContent = profile.totalRides;

        // Update profile form
        document.getElementById('profile-name').value = profile.name;
        document.getElementById('profile-email').value = profile.email;
        document.getElementById('profile-phone').value = profile.phone;
        document.getElementById('profile-license').value = profile.licensePlate;
    }

    async toggleStatus() {
        try {
            const newStatus = !this.isOnline ? 'available' : 'offline';
            await driverAPI.updateStatus(newStatus);
            this.isOnline = !this.isOnline;
            this.updateStatusUI();
            
            if (this.isOnline) {
                this.startLocationTracking();
            } else {
                this.stopLocationTracking();
            }
        } catch (error) {
            utils.showError('Failed to update status');
        }
    }

    updateStatusUI() {
        const statusElement = document.getElementById('driver-status');
        const toggleButton = document.getElementById('toggle-status');
        
        if (this.isOnline) {
            statusElement.className = 'driver-status status-available';
            statusElement.querySelector('.status-text').textContent = 'Available';
            toggleButton.innerHTML = '<i class="fas fa-power-off"></i><span>Go Offline</span>';
        } else {
            statusElement.className = 'driver-status status-offline';
            statusElement.querySelector('.status-text').textContent = 'Offline';
            toggleButton.innerHTML = '<i class="fas fa-power-off"></i><span>Go Online</span>';
        }
    }

    startLocationTracking() {
        this.locationInterval = setInterval(() => {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        const location = {
                            latitude: position.coords.latitude,
                            longitude: position.coords.longitude
                        };
                        driverAPI.updateLocation(location);
                        updateLocation(location);
                    },
                    (error) => {
                        console.error('Error getting location:', error);
                    }
                );
            }
        }, 5000); // Update every 5 seconds
    }

    stopLocationTracking() {
        if (this.locationInterval) {
            clearInterval(this.locationInterval);
            this.locationInterval = null;
        }
    }

    async acceptRide() {
        try {
            await driverAPI.acceptRide(this.currentRide.id);
            this.updateRideUI();
        } catch (error) {
            utils.showError('Failed to accept ride');
        }
    }

    async startRide() {
        try {
            await driverAPI.startRide(this.currentRide.id);
            this.updateRideUI();
        } catch (error) {
            utils.showError('Failed to start ride');
        }
    }

    async completeRide() {
        try {
            await driverAPI.completeRide(this.currentRide.id);
            this.currentRide = null;
            this.updateRideUI();
            this.loadEarnings();
        } catch (error) {
            utils.showError('Failed to complete ride');
        }
    }

    updateRideUI() {
        const noRideElement = document.getElementById('no-ride');
        const activeRideElement = document.getElementById('active-ride');
        
        if (!this.currentRide) {
            noRideElement.classList.remove('hidden');
            activeRideElement.classList.add('hidden');
            return;
        }

        noRideElement.classList.add('hidden');
        activeRideElement.classList.remove('hidden');

        // Update ride details
        document.getElementById('ride-id').textContent = this.currentRide.id;
        document.getElementById('ride-status').textContent = this.currentRide.status;
        document.getElementById('pickup-address').textContent = this.currentRide.pickupAddress;
        document.getElementById('dropoff-address').textContent = this.currentRide.dropoffAddress;
        document.getElementById('passenger-name').textContent = this.currentRide.passengerName;
        document.getElementById('passenger-phone').textContent = this.currentRide.passengerPhone;
        document.getElementById('ride-fare').textContent = utils.formatCurrency(this.currentRide.fare);

        // Update action buttons
        const acceptButton = document.getElementById('accept-ride');
        const startButton = document.getElementById('start-ride');
        const completeButton = document.getElementById('complete-ride');

        acceptButton.disabled = this.currentRide.status !== 'pending';
        startButton.disabled = this.currentRide.status !== 'accepted';
        completeButton.disabled = this.currentRide.status !== 'in_progress';
    }

    async loadEarnings() {
        try {
            const earnings = await driverAPI.getEarnings();
            this.updateEarningsUI(earnings);
        } catch (error) {
            utils.showError('Failed to load earnings');
        }
    }

    updateEarningsUI(earnings) {
        document.getElementById('today-earnings').textContent = utils.formatCurrency(earnings.today);
        document.getElementById('week-earnings').textContent = utils.formatCurrency(earnings.week);
        document.getElementById('month-earnings').textContent = utils.formatCurrency(earnings.month);
        document.getElementById('total-earnings').textContent = utils.formatCurrency(earnings.total);

        // Update chart
        this.updateEarningsChart(earnings.history);
    }

    updateEarningsChart(history) {
        const ctx = document.getElementById('earningsChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: history.map(item => item.date),
                datasets: [{
                    label: 'Daily Earnings',
                    data: history.map(item => item.amount),
                    borderColor: '#4CAF50',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    async loadRideHistory() {
        try {
            const filter = document.getElementById('history-filter').value;
            const history = await driverAPI.getRideHistory(filter);
            this.updateHistoryUI(history);
        } catch (error) {
            utils.showError('Failed to load ride history');
        }
    }

    updateHistoryUI(history) {
        const historyList = document.getElementById('ride-history');
        historyList.innerHTML = history.map(ride => `
            <div class="history-item">
                <div class="history-header">
                    <span class="ride-id">Ride #${ride.id}</span>
                    <span class="ride-date">${utils.formatDate(ride.date)}</span>
                </div>
                <div class="history-details">
                    <div class="history-location">
                        <i class="fas fa-map-marker-alt pickup"></i>
                        <span>${ride.pickupAddress}</span>
                    </div>
                    <div class="history-location">
                        <i class="fas fa-map-marker-alt dropoff"></i>
                        <span>${ride.dropoffAddress}</span>
                    </div>
                </div>
                <div class="history-footer">
                    <span class="ride-fare">${utils.formatCurrency(ride.fare)}</span>
                    <span class="ride-status ${ride.status}">${ride.status}</span>
                </div>
            </div>
        `).join('');
    }

    async updateProfile() {
        const profileData = {
            name: document.getElementById('profile-name').value,
            email: document.getElementById('profile-email').value,
            phone: document.getElementById('profile-phone').value,
            licensePlate: document.getElementById('profile-license').value,
            password: document.getElementById('profile-password').value
        };

        try {
            await driverAPI.updateProfile(profileData);
            utils.showSuccess('Profile updated successfully');
            this.loadDriverProfile();
        } catch (error) {
            utils.showError('Failed to update profile');
        }
    }

    showSection(sectionId) {
        // Update active menu item
        document.querySelectorAll('.driver-menu a').forEach(link => {
            link.classList.remove('active');
            if (link.dataset.section === sectionId) {
                link.classList.add('active');
            }
        });

        // Show selected section
        document.querySelectorAll('.dashboard-section').forEach(section => {
            section.classList.remove('active');
            if (section.id === sectionId) {
                section.classList.add('active');
            }
        });

        // Load section data
        switch (sectionId) {
            case 'earnings':
                this.loadEarnings();
                break;
            case 'history':
                this.loadRideHistory();
                break;
        }
    }

    initMap() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const location = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude
                    };
                    initMap(location);
                },
                (error) => {
                    console.error('Error getting location:', error);
                    initMap({ lat: 0, lng: 0 }); // Default location
                }
            );
        } else {
            initMap({ lat: 0, lng: 0 }); // Default location
        }
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.driverDashboard = new DriverDashboard();
}); 