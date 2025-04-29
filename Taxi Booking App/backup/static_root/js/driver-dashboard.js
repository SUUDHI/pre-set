// Load ride requests
async function loadRideRequests() {
    try {
        const response = await fetch('/driver/rides/requested', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        const data = await response.json();
        const rideList = document.getElementById('requestsTableBody');
        
        if (response.ok) {
            // Check if data is an array (direct response) or has a rides property
            const rides = Array.isArray(data) ? data : (data.rides || []);
            
            if (rides.length === 0) {
                rideList.innerHTML = '<div class="no-rides">No ride requests available</div>';
                return;
            }

            rideList.innerHTML = rides.map(ride => createRideCard(ride)).join('');
        } else {
            console.error('Error response:', data);
            rideList.innerHTML = '<div class="error-message">Failed to load ride requests</div>';
        }
    } catch (error) {
        console.error('Error loading ride requests:', error);
        const rideList = document.getElementById('requestsTableBody');
        rideList.innerHTML = '<div class="error-message">Error loading ride requests</div>';
    }
}

// Create a ride card HTML
function createRideCard(ride) {
    const pickupCoords = formatCoordinates(ride.PickupLat, ride.PickupLon);
    const dropoffCoords = formatCoordinates(ride.DropoffLat, ride.DropoffLon);
    const status = (ride.Status || '').toLowerCase();
    const fare = formatCurrency(ride.Fare);
    const requestDate = formatDateTime(ride.RequestedAt);

    return `
        <div class="ride-card">
            <div class="ride-header">
                <div class="ride-title">
                    <span class="ride-number">Ride #${ride.RideID}</span>
                    <span class="status-badge status-${status}">${status}</span>
                </div>
                <div class="ride-actions">
                    ${getActionButtons(ride)}
                </div>
            </div>
            <div class="ride-details">
                <div class="location-info">
                    <i class="fas fa-map-marker-alt pickup-icon"></i>
                    <div class="location-text">
                        <span class="location-label">Pickup:</span>
                        <span class="coordinates">${pickupCoords}</span>
                    </div>
                </div>
                <div class="location-info">
                    <i class="fas fa-flag-checkered dropoff-icon"></i>
                    <div class="location-text">
                        <span class="location-label">Dropoff:</span>
                        <span class="coordinates">${dropoffCoords}</span>
                    </div>
                </div>
                <div class="ride-meta">
                    <div class="fare-info">
                        <i class="fas fa-rupee-sign"></i>
                        <span class="fare-label">Fare:</span>
                        <span class="fare-amount">₹${fare}</span>
                    </div>
                    <div class="time-info">
                        <i class="far fa-clock"></i>
                        <span class="time-label">Requested:</span>
                        <span class="request-time">${requestDate}</span>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Format coordinates
function formatCoordinates(lat, lon) {
    return `${parseFloat(lat).toFixed(6)}, ${parseFloat(lon).toFixed(6)}`;
}

// Format currency
function formatCurrency(amount) {
    return parseFloat(amount).toFixed(2);
}

// Format datetime
function formatDateTime(dateStr) {
    return new Date(dateStr).toLocaleString('en-IN', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });
}

// Get action buttons based on ride status
function getActionButtons(ride) {
    const status = (ride.Status || '').toUpperCase();
    switch (status) {
        case 'REQUESTED':
            return `
                <button onclick="acceptRide(${ride.RideID})" class="btn-primary accept-btn">
                    <i class="fas fa-check"></i> Accept Ride
                </button>
            `;
        case 'ACCEPTED':
            return `
                <button onclick="startRide(${ride.RideID})" class="btn-secondary">
                    <i class="fas fa-play"></i> Start Ride
                </button>
            `;
        case 'IN_PROGRESS':
            return `
                <button onclick="completeRide(${ride.RideID})" class="btn-success">
                    <i class="fas fa-flag-checkered"></i> Complete Ride
                </button>
            `;
        default:
            return '';
    }
}

// Accept a ride
async function acceptRide(rideId) {
    try {
        const response = await fetch(`/driver/rides/${rideId}/accept`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        const data = await response.json();
        
        if (response.ok) {
            alert('Ride accepted successfully');
            loadRideRequests();
        } else {
            throw new Error(data.error || 'Failed to accept ride');
        }
    } catch (error) {
        console.error('Error accepting ride:', error);
        alert(error.message);
    }
}

// Handle location form submission
const locationForm = document.getElementById('locationForm');
if (locationForm) {
    locationForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const latitudeInput = document.getElementById('latitude');
        const longitudeInput = document.getElementById('longitude');

        if (!latitudeInput.value || !longitudeInput.value) {
            alert('Please enter both latitude and longitude');
            return;
        }

        try {
            const response = await fetch('/driver/location', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({
                    latitude: parseFloat(latitudeInput.value),
                    longitude: parseFloat(longitudeInput.value)
                })
            });

            const data = await response.json();
            
            if (response.ok) {
                alert(data.message || 'Location updated successfully');
                // Clear form inputs explicitly
                latitudeInput.value = '';
                longitudeInput.value = '';
            } else {
                throw new Error(data.error || 'Failed to update location');
            }
        } catch (error) {
            console.error('Error updating location:', error);
            alert(error.message);
        }
    });
}

// Handle status changes
const statusSelect = document.getElementById('driverStatus');
if (statusSelect) {
    statusSelect.addEventListener('change', async (e) => {
        const newStatus = e.target.value;
        const previousStatus = e.target.dataset.previousValue || 'offline';

        try {
            const response = await fetch('/driver/status', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ status: newStatus })
            });

            const data = await response.json();

            if (response.ok) {
                e.target.dataset.previousValue = newStatus;
            } else {
                e.target.value = previousStatus;
                throw new Error(data.error || 'Failed to update status');
            }
        } catch (error) {
            console.error('Error updating status:', error);
            alert(error.message);
            e.target.value = previousStatus;
        }
    });
}

// Fetch driver's current status
async function loadDriverStatus() {
    try {
        const response = await fetch('/driver/status', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        const data = await response.json();
        
        if (response.ok && data.status) {
            const statusSelect = document.getElementById('driverStatus');
            if (statusSelect) {
                statusSelect.value = data.status.toLowerCase();
                statusSelect.dataset.previousValue = data.status.toLowerCase();
            }
        } else if (response.status === 401) {
            alert('Session expired. Please login again.');
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Error loading driver status:', error);
    }
}

// Initialize everything when the page loads
document.addEventListener('DOMContentLoaded', () => {
    // Display user email
    const userEmail = localStorage.getItem('userEmail');
    if (userEmail) {
        const userEmailElement = document.getElementById('userEmail');
        if (userEmailElement) {
            userEmailElement.textContent = userEmail;
        }
    }

    // Load driver status
    loadDriverStatus();

    // Load ride requests
    loadRideRequests();
    
    // Set up periodic refresh of ride requests
    setInterval(loadRideRequests, 30000); // Refresh every 30 seconds
}); 