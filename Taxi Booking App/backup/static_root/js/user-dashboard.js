let currentRideId = null;
let selectedReason = '';
let map = null;
let tracker = null;

// Initialize map and tracker
function initializeMap() {
    if (!map) {  // Only initialize if map doesn't exist
        console.log('Initializing map...');
        mapboxgl.accessToken = 'pk.eyJ1Ijoic3V1ZGhpIiwiYSI6ImNtOWs0cW9vMDBpdmwybXM2c21ramNmZTQifQ.xsTF7EaOpYKwX4VaVMNgCQ';
        map = new mapboxgl.Map({
            container: 'map',
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [0, 0],
            zoom: 2
        });

        // Add navigation controls
        map.addControl(new mapboxgl.NavigationControl());

        // Handle map clicks for booking
        map.on('click', (e) => {
            const lngLat = e.lngLat;
            const pickupLat = document.getElementById('pickupLat');
            const pickupLon = document.getElementById('pickupLon');
            const dropoffLat = document.getElementById('dropoffLat');
            const dropoffLon = document.getElementById('dropoffLon');

            if (pickupLat && pickupLon && dropoffLat && dropoffLon) {
                if (!pickupLat.value || !pickupLon.value) {
                    pickupLat.value = lngLat.lat.toFixed(6);
                    pickupLon.value = lngLat.lng.toFixed(6);
                } else {
                    dropoffLat.value = lngLat.lat.toFixed(6);
                    dropoffLon.value = lngLat.lng.toFixed(6);
                }
            }
        });

        // Initialize driver tracker after map is loaded
        map.on('load', () => {
            console.log('Map loaded, initializing tracker');
            tracker = new DriverTracker(map, localStorage.getItem('token'));
            tracker.connect();
            checkActiveRide();
        });
    }
}

// Check for active ride
async function checkActiveRide() {
    try {
        console.log('Checking for active ride...');
        const response = await fetch('/ride/active', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Active ride data:', data);
        
        if (data.ride) {
            currentRideId = data.ride.RideID;
            updateRideStatus(data.ride);
            if (tracker && map.loaded()) {
                console.log('Starting ride tracking with coordinates:', {
                    pickup: [data.ride.PickupLon, data.ride.PickupLat],
                    dropoff: [data.ride.DropoffLon, data.ride.DropoffLat]
                });
                
                // Create a ride details object in the format expected by the tracker
                const rideDetails = {
                    pickup_lat: parseFloat(data.ride.PickupLat),
                    pickup_lon: parseFloat(data.ride.PickupLon),
                    dropoff_lat: parseFloat(data.ride.DropoffLat),
                    dropoff_lon: parseFloat(data.ride.DropoffLon)
                };

                // Make sure we have valid coordinates
                if (isNaN(rideDetails.pickup_lat) || isNaN(rideDetails.pickup_lon) ||
                    isNaN(rideDetails.dropoff_lat) || isNaN(rideDetails.dropoff_lon)) {
                    console.error('Invalid coordinates in ride data:', rideDetails);
                    return;
                }

                console.log('Showing ride locations with details:', rideDetails);
                tracker.startTracking(currentRideId);
                tracker.showRideLocations(rideDetails);
            } else {
                console.log('Tracker not initialized or map not loaded yet');
                // If map is not loaded, wait and try again
                if (!map.loaded()) {
                    map.once('load', () => checkActiveRide());
                }
            }
        } else {
            console.log('No active ride found');
            if (tracker) {
                tracker.stopTracking();
            }
        }
    } catch (error) {
        console.error('Error checking active ride:', error);
    }
}

// Update ride status display
function updateRideStatus(ride) {
    try {
        const statusElement = document.getElementById('ride-status');
        const driverInfoElement = document.getElementById('driver-info');
        const etaInfoElement = document.getElementById('eta-info');

        if (!statusElement || !driverInfoElement || !etaInfoElement) {
            console.error('Status display elements not found');
            return;
        }

        if (ride) {
            console.log('Updating ride status display:', ride);
            statusElement.textContent = `Status: ${ride.Status || 'Unknown'}`;
            if (ride.DriverName) {
                driverInfoElement.textContent = `Driver: ${ride.DriverName} (${ride.DriverPhone || 'No phone'})`;
            } else {
                driverInfoElement.textContent = 'Waiting for driver...';
            }
            if (ride.ETA) {
                etaInfoElement.textContent = `ETA: ${ride.ETA}`;
            } else {
                etaInfoElement.textContent = '';
            }
        } else {
            statusElement.textContent = 'No active ride';
            driverInfoElement.textContent = '';
            etaInfoElement.textContent = '';
        }
    } catch (error) {
        console.error('Error updating ride status:', error);
    }
}

// Format currency
function formatCurrency(amount) {
    return '₹' + (Number(amount) || 0).toFixed(2);
}

// Format coordinates to 6 decimal places
function formatCoordinate(coord) {
    return Number(coord).toFixed(6);
}

// Format location for display
function formatLocation(lat, lon) {
    return `${formatCoordinate(lat)}, ${formatCoordinate(lon)}`;
}

// Format datetime for display
function formatDateTime(dateStr) {
    if (!dateStr) return '🕒 Immediate';
    const date = new Date(dateStr);
    return '🕒 ' + date.toLocaleString('en-IN', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });
}

// Load ride history
async function loadRideHistory() {
    try {
        const response = await fetch('/ride/history', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Ride history data:', data); // Debug log
        
        const tableBody = document.getElementById('ridesTableBody');
        
        if (data.rides && data.rides.length > 0) {
            tableBody.innerHTML = data.rides.map(ride => {
                console.log('Processing ride:', ride); // Debug log
                
                // Format fees with null checks
                const fareDisplay = formatCurrency(ride.Fare);
                const cancellationFeeDisplay = formatCurrency(ride.CancellationFee);

                // Format driver info with null checks
                const driverInfo = (ride.DriverID && ride.DriverName) ? `
                    <div class="driver-info">
                        <span class="driver-name">${ride.DriverName}</span>
                        <span class="driver-phone">${ride.DriverPhone || 'N/A'}</span>
                    </div>
                ` : '';

                // Format pickup time with null check
                const pickupTimeDisplay = formatDateTime(ride.PickupTime);
                
                // Format coordinates
                const pickupLocation = formatLocation(ride.PickupLat, ride.PickupLon);
                const dropoffLocation = formatLocation(ride.DropoffLat, ride.DropoffLon);
                
                // Get status and ensure it's lowercase for CSS classes
                const statusText = ride.Status || 'Unknown';
                const statusClass = statusText.toLowerCase();
                
                return `
                    <tr id="ride-${ride.RideID}">
                        <td>#${ride.RideID}</td>
                        <td>
                            <span class="status-badge status-${statusClass}">
                                ${statusText}
                            </span>
                            <div class="pickup-time">
                                ${pickupTimeDisplay}
                            </div>
                        </td>
                        <td>${ride.VehicleType || 'Standard'}</td>
                        <td>${pickupLocation}</td>
                        <td>${dropoffLocation}</td>
                        <td>${fareDisplay}</td>
                        <td>${cancellationFeeDisplay}</td>
                        <td>
                            ${statusText.toLowerCase() === 'requested' ? `
                                <div class="action-container">
                                    <button onclick="toggleCancelForm(${ride.RideID})" class="btn-danger">
                                        Cancel Ride
                                    </button>
                                    <div id="cancel-form-${ride.RideID}" class="cancel-form" style="display: none;">
                                        <div class="cancel-modal">
                                            <div class="modal-header">
                                                <h3>Cancel Ride</h3>
                                                <button class="close-button" onclick="toggleCancelForm(${ride.RideID})">&times;</button>
                                            </div>
                                            <div class="modal-body">
                                                <p>Please select a reason for cancellation:</p>
                                                <div class="cancellation-reasons">
                                                    <label class="reason-option">
                                                        <input type="radio" name="reason-${ride.RideID}" value="Changed my plans">
                                                        Changed my plans
                                                    </label>
                                                    <label class="reason-option">
                                                        <input type="radio" name="reason-${ride.RideID}" value="Driver taking too long">
                                                        Driver taking too long
                                                    </label>
                                                    <label class="reason-option">
                                                        <input type="radio" name="reason-${ride.RideID}" value="Booked by mistake">
                                                        Booked by mistake
                                                    </label>
                                                    <label class="reason-option">
                                                        <input type="radio" name="reason-${ride.RideID}" value="Wrong location entered">
                                                        Wrong location entered
                                                    </label>
                                                    <label class="reason-option">
                                                        <input type="radio" name="reason-${ride.RideID}" value="Other">
                                                        Other
                                                    </label>
                                                </div>
                                            </div>
                                            <div class="modal-footer">
                                                <button class="btn-confirm" onclick="confirmCancellation(${ride.RideID})">
                                                    Confirm Cancellation
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ` : statusText.toLowerCase() === 'accepted' ? `
                                <div class="driver-assigned">
                                    <span class="status-badge status-accepted">Driver Assigned</span>
                                    ${driverInfo}
                                </div>
                            ` : ''}
                        </td>
                    </tr>
                `;
            }).join('');
        } else {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="8" class="error-message">
                        No ride history available. Book a ride to get started!
                    </td>
                </tr>
            `;
        }
    } catch (error) {
        console.error('Error loading ride history:', error);
        const tableBody = document.getElementById('ridesTableBody');
        tableBody.innerHTML = `
            <tr>
                <td colspan="8" class="error-message">
                    Failed to load ride history. Please try again later. Error: ${error.message}
                </td>
            </tr>
        `;
    }
}

function toggleCancelForm(rideId) {
    const form = document.getElementById(`cancel-form-${rideId}`);
    if (form) {
        form.style.display = form.style.display === 'none' ? 'block' : 'none';
    }
}

function createCancelForm(rideId) {
    return `
        <div id="cancel-form-${rideId}" class="cancel-form" style="display: none;">
            <div class="cancel-modal">
                <div class="modal-header">
                    <h3>Cancel Ride</h3>
                    <button class="close-button" onclick="toggleCancelForm(${rideId})">&times;</button>
                </div>
                <div class="modal-body">
                    <p>Please select a reason for cancellation:</p>
                    <div class="cancellation-reasons">
                        <label class="reason-option">
                            <input type="radio" name="reason-${rideId}" value="Changed my plans">
                            Changed my plans
                        </label>
                        <label class="reason-option">
                            <input type="radio" name="reason-${rideId}" value="Driver taking too long">
                            Driver taking too long
                        </label>
                        <label class="reason-option">
                            <input type="radio" name="reason-${rideId}" value="Booked by mistake">
                            Booked by mistake
                        </label>
                        <label class="reason-option">
                            <input type="radio" name="reason-${rideId}" value="Wrong location entered">
                            Wrong location entered
                        </label>
                        <label class="reason-option">
                            <input type="radio" name="reason-${rideId}" value="Other">
                            Other
                        </label>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn-confirm" onclick="confirmCancellation(${rideId})">
                        Confirm Cancellation
                    </button>
                </div>
            </div>
        </div>
    `;
}

async function confirmCancellation(rideId) {
    const selectedReason = document.querySelector(`input[name="reason-${rideId}"]:checked`);
    
    if (!selectedReason) {
        alert('Please select a cancellation reason');
        return;
    }

    try {
        const response = await fetch(`/ride/${rideId}/cancel`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                cancellation_reason: selectedReason.value
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to cancel ride');
        }

        const data = await response.json();
        alert('Ride cancelled successfully');
        toggleCancelForm(rideId); // Hide the cancellation form
        loadRideHistory(); // Refresh ride history
    } catch (error) {
        console.error('Error cancelling ride:', error);
        alert(error.message || 'Failed to cancel ride. Please try again.');
    }
}

// Load user email
async function loadUserEmail() {
    try {
        const response = await fetch('/auth/user-info', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const data = await response.json();
        document.getElementById('userEmail').textContent = data.email;
    } catch (error) {
        console.error('Error loading user info:', error);
    }
}

// Load vehicle types
async function loadVehicleTypes() {
    try {
        const response = await fetch('/driver/vehicle-types');
        const data = await response.json();
        
        if (response.ok && data) {
            const vehicleTypeSelect = document.getElementById('vehicleType');
            vehicleTypeSelect.innerHTML = data.map(type => `
                <option value="${type.id}">${type.name} - ${type.description}</option>
            `).join('');
        } else {
            throw new Error(data.error || 'Failed to load vehicle types');
        }
    } catch (error) {
        console.error('Error loading vehicle types:', error);
        alert('Failed to load vehicle types. Please refresh the page.');
    }
}

// Logout function
function logout() {
    localStorage.removeItem('token');
    window.location.href = '/';
}

// Initialize everything when the page loads
document.addEventListener('DOMContentLoaded', () => {
    initializeMap();
    loadRideHistory();
    loadUserEmail();
    loadVehicleTypes();
    
    // Handle booking form submission
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        bookingForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = {
                pickup_lat: document.getElementById('pickupLat').value,
                pickup_lon: document.getElementById('pickupLon').value,
                dropoff_lat: document.getElementById('dropoffLat').value,
                dropoff_lon: document.getElementById('dropoffLon').value,
                vehicle_type_id: document.getElementById('vehicleType').value,
                pickup_time: document.getElementById('pickupTime').value || null
            };

            try {
                const response = await fetch('/ride/request', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    },
                    body: JSON.stringify(formData)
                });
                const data = await response.json();
                if (response.ok) {
                    alert('Ride booked successfully!');
                    // Clear form fields
                    document.getElementById('pickupLat').value = '';
                    document.getElementById('pickupLon').value = '';
                    document.getElementById('dropoffLat').value = '';
                    document.getElementById('dropoffLon').value = '';
                    document.getElementById('pickupTime').value = '';
                    // Reset vehicle type to first option
                    const vehicleTypeSelect = document.getElementById('vehicleType');
                    if (vehicleTypeSelect.options.length > 0) {
                        vehicleTypeSelect.selectedIndex = 0;
                    }
                    // Refresh ride history and check active ride
                    loadRideHistory();
                    checkActiveRide();
                } else {
                    alert(data.error || 'Failed to book ride');
                }
            } catch (error) {
                console.error('Error booking ride:', error);
                alert('Failed to book ride');
            }
        });
    }

    // Check for active ride every 30 seconds
    setInterval(checkActiveRide, 30000);
    
    // Refresh ride history every 30 seconds
    setInterval(loadRideHistory, 30000);
}); 