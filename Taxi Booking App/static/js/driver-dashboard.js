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

            rideList.innerHTML = rides.map(ride => {
                // Format the coordinates to be more readable
                const pickupCoords = `${parseFloat(ride.PickupLat).toFixed(6)}, ${parseFloat(ride.PickupLon).toFixed(6)}`;
                const dropoffCoords = `${parseFloat(ride.DropoffLat).toFixed(6)}, ${parseFloat(ride.DropoffLon).toFixed(6)}`;
                
                // Format the status for display
                const status = ride.Status.toLowerCase();
                
                // Format the fare
                const fare = parseFloat(ride.Fare).toFixed(2);
                
                // Format the date
                const requestDate = new Date(ride.RequestedAt).toLocaleString('en-IN', {
                    day: '2-digit',
                    month: 'short',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                    hour12: true
                });

                return `
                    <div class="ride-card">
                        <div class="ride-header">
                            <div class="ride-title">
                                <span class="ride-number">Ride #${ride.RideID}</span>
                                <span class="status-badge status-${status}">
                                    ${status}
                                </span>
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
            }).join('');
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
            loadRideRequests(); // Reload the ride list
        } else {
            alert(data.error || 'Failed to accept ride');
        }
    } catch (error) {
        console.error('Error accepting ride:', error);
        alert('An error occurred while accepting the ride');
    }
}

// Update driver location
document.getElementById('locationForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        latitude: parseFloat(document.getElementById('latitude').value),
        longitude: parseFloat(document.getElementById('longitude').value)
    };

    try {
        const response = await fetch('/driver/location', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        
        if (response.ok) {
            alert('Location updated successfully');
        } else {
            alert(data.error || 'Failed to update location');
        }
    } catch (error) {
        alert('An error occurred while updating location');
    }
});

// Update driver status
document.getElementById('driverStatus').addEventListener('change', async (e) => {
    const status = e.target.value;

    try {
        const response = await fetch('/driver/status', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ status })
        });

        const data = await response.json();
        
        if (response.ok) {
            alert('Status updated successfully');
        } else {
            alert(data.error || 'Failed to update status');
        }
    } catch (error) {
        console.error('Error updating status:', error);
        alert('An error occurred while updating status');
    }
});

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
            document.getElementById('driverStatus').value = data.status.toLowerCase();
        }
    } catch (error) {
        console.error('Error loading driver status:', error);
    }
}

// Load initial data
document.addEventListener('DOMContentLoaded', () => {
    // Display user email
    const userEmail = localStorage.getItem('userEmail');
    if (userEmail) {
        document.getElementById('userEmail').textContent = userEmail;
    }

    // Load driver status
    loadDriverStatus();

    // Load ride requests
    loadRideRequests();
    
    // Set up periodic refresh of ride requests
    setInterval(loadRideRequests, 30000); // Refresh every 30 seconds
}); 