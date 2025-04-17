import { rideAPI } from './api.js';
import { initMap, updatePickupLocation, updateDropoffLocation } from './map.js';

class RideManager {
    constructor() {
        this.currentRide = null;
        this.rideStatusInterval = null;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        const requestRideForm = document.getElementById('request-ride-form');
        if (requestRideForm) {
            requestRideForm.addEventListener('submit', this.handleRideRequest.bind(this));
        }

        const cancelRideBtn = document.getElementById('cancel-ride-btn');
        if (cancelRideBtn) {
            cancelRideBtn.addEventListener('click', this.handleRideCancellation.bind(this));
        }
    }

    async handleRideRequest(event) {
        event.preventDefault();
        
        const pickupLocation = document.getElementById('pickup-location').value;
        const dropoffLocation = document.getElementById('dropoff-location').value;
        
        if (!pickupLocation || !dropoffLocation) {
            utils.showError('Please select both pickup and dropoff locations');
            return;
        }

        try {
            const response = await rideAPI.requestRide({
                pickupLocation,
                dropoffLocation
            });

            if (response.success) {
                this.currentRide = response.ride;
                this.updateRideStatusUI();
                this.startRideStatusPolling();
                utils.showSuccess('Ride requested successfully!');
            }
        } catch (error) {
            utils.showError(error.message || 'Failed to request ride');
        }
    }

    async handleRideCancellation() {
        if (!this.currentRide) return;

        try {
            const response = await rideAPI.cancelRide(this.currentRide.id);
            
            if (response.success) {
                this.stopRideStatusPolling();
                this.currentRide = null;
                this.resetRideUI();
                utils.showSuccess('Ride cancelled successfully');
            }
        } catch (error) {
            utils.showError(error.message || 'Failed to cancel ride');
        }
    }

    startRideStatusPolling() {
        this.stopRideStatusPolling(); // Clear any existing interval
        
        this.rideStatusInterval = setInterval(async () => {
            if (!this.currentRide) return;
            
            try {
                const response = await rideAPI.getRideStatus(this.currentRide.id);
                if (response.success) {
                    this.currentRide = response.ride;
                    this.updateRideStatusUI();
                    
                    // Stop polling if ride is completed or cancelled
                    if (['completed', 'cancelled'].includes(this.currentRide.status)) {
                        this.stopRideStatusPolling();
                    }
                }
            } catch (error) {
                console.error('Error polling ride status:', error);
            }
        }, 5000); // Poll every 5 seconds
    }

    stopRideStatusPolling() {
        if (this.rideStatusInterval) {
            clearInterval(this.rideStatusInterval);
            this.rideStatusInterval = null;
        }
    }

    updateRideStatusUI() {
        if (!this.currentRide) return;

        const statusElement = document.getElementById('ride-status');
        const driverInfoElement = document.getElementById('driver-info');
        const cancelButton = document.getElementById('cancel-ride-btn');
        
        if (statusElement) {
            statusElement.textContent = this.currentRide.status.toUpperCase();
            statusElement.className = `status-${this.currentRide.status}`;
        }

        if (driverInfoElement && this.currentRide.driver) {
            driverInfoElement.innerHTML = `
                <div class="driver-avatar">
                    <img src="${this.currentRide.driver.avatar || 'default-avatar.png'}" alt="Driver">
                </div>
                <div class="driver-details">
                    <h3>${this.currentRide.driver.name}</h3>
                    <p>${this.currentRide.driver.licensePlate}</p>
                    <div class="driver-rating">
                        <span class="stars">${'★'.repeat(Math.round(this.currentRide.driver.rating))}</span>
                        <span>(${this.currentRide.driver.totalRides} rides)</span>
                    </div>
                </div>
            `;
        }

        if (cancelButton) {
            cancelButton.disabled = !['requested', 'accepted'].includes(this.currentRide.status);
        }
    }

    resetRideUI() {
        const statusElement = document.getElementById('ride-status');
        const driverInfoElement = document.getElementById('driver-info');
        const cancelButton = document.getElementById('cancel-ride-btn');
        
        if (statusElement) statusElement.textContent = '';
        if (driverInfoElement) driverInfoElement.innerHTML = '';
        if (cancelButton) cancelButton.disabled = true;
    }
}

// Initialize ride manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.rideManager = new RideManager();
    initMap();
}); 