// Load ride requests
async function loadRideRequests() {
    try {
        // Load both requested rides and assigned rides
        const [requestedResponse, assignedResponse] = await Promise.all([
            fetch('/driver/rides/requested', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            }),
            fetch('/driver/rides/assigned', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            })
        ]);

        const requestedData = await requestedResponse.json();
        const assignedData = await assignedResponse.json();
        const rideList = document.getElementById('requestsTableBody');
        
        // Combine and sort rides
        const rides = [
            ...(Array.isArray(requestedData) ? requestedData : (requestedData.rides || [])),
            ...(Array.isArray(assignedData) ? assignedData : (assignedData.rides || []))
        ].sort((a, b) => new Date(b.RequestedAt) - new Date(a.RequestedAt));
        
        if (rides.length === 0) {
            rideList.innerHTML = '<div class="no-rides">No rides available</div>';
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

            // Get user details section if ride is assigned
            const userDetails = ride.UserName ? `
                <div class="user-details">
                    <i class="fas fa-user"></i>
                    <span class="user-name">${ride.UserName}</span>
                    ${ride.UserPhone ? `<a href="tel:${ride.UserPhone}" class="user-phone"><i class="fas fa-phone"></i> ${ride.UserPhone}</a>` : ''}
                </div>
            ` : '';

            return `
                <div class="ride-card ${status}-status">
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
                    ${userDetails}
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
    } catch (error) {
        console.error('Error loading rides:', error);
        const rideList = document.getElementById('requestsTableBody');
        rideList.innerHTML = '<div class="error-message">Error loading rides</div>';
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
                <div class="button-group">
                    <button onclick="startRide(${ride.RideID})" class="btn-secondary">
                        <i class="fas fa-play"></i> Start Ride
                    </button>
                    <button onclick="cancelRide(${ride.RideID})" class="btn-danger">
                        <i class="fas fa-times"></i> Cancel
                    </button>
                </div>
            `;
        case 'IN_PROGRESS':
            return `
                <div class="button-group">
                    <button onclick="completeRide(${ride.RideID})" class="btn-success">
                        <i class="fas fa-flag-checkered"></i> Complete Ride
                    </button>
                    <button onclick="cancelRide(${ride.RideID})" class="btn-danger">
                        <i class="fas fa-times"></i> Cancel
                    </button>
                </div>
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
    const token = localStorage.getItem('token');

    if (!token) {
        alert('Please login again');
        window.location.href = '/';
        return;
    }

    try {
        const response = await fetch('/driver/status', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ status })
        });

        const data = await response.json();
        
        if (response.ok) {
            alert('Status updated successfully');
        } else {
            if (response.status === 401) {
                alert('Session expired. Please login again.');
                window.location.href = '/';
            } else {
                alert(data.error || 'Failed to update status');
            }
        }
    } catch (error) {
        console.error('Error updating status:', error);
        alert('An error occurred while updating status');
    }
});

// Fetch driver's current status
async function loadDriverStatus() {
    const token = localStorage.getItem('token');
    
    if (!token) {
        console.error('No token found');
        return;
    }

    try {
        const response = await fetch('/driver/status', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();
        
        if (response.ok && data.status) {
            document.getElementById('driverStatus').value = data.status.toLowerCase();
        } else if (response.status === 401) {
            alert('Session expired. Please login again.');
            window.location.href = '/';
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

async function completeRide(rideId) {
    try {
        // Get current location
        const position = await getCurrentPosition();
        
        const response = await fetch(`/driver/rides/${rideId}/complete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                latitude: position.coords.latitude,
                longitude: position.coords.longitude
            })
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to complete ride');
        }

        // Show success message
        showNotification('Ride completed successfully', 'success');
        
        // Update driver status to available
        await updateDriverStatus('available');
        
        // Refresh the ride requests list
        await loadRideRequests();
        
    } catch (error) {
        console.error('Error completing ride:', error);
        showNotification(error.message, 'error');
    }
}

// Helper function to get current position
function getCurrentPosition() {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            reject(new Error('Geolocation is not supported by your browser'));
            return;
        }
        
        navigator.geolocation.getCurrentPosition(resolve, reject, {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0
        });
    });
}

// Add cancel ride function
async function cancelRide(rideId) {
    // Ask for confirmation before cancelling
    if (!confirm('Are you sure you want to cancel this ride?')) {
        return;
    }

    try {
        const response = await fetch(`/driver/rides/${rideId}/cancel`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to cancel ride');
        }

        // Show success message
        showNotification('Ride cancelled successfully', 'success');
        
        // Update driver status to available
        await updateDriverStatus('available');
        
        // Refresh the ride requests list
        await loadRideRequests();
        
    } catch (error) {
        console.error('Error cancelling ride:', error);
        showNotification(error.message, 'error');
    }
}

// Add notification function
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    // Style the notification
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.padding = '15px 25px';
    notification.style.borderRadius = '4px';
    notification.style.animation = 'slideIn 0.5s ease-in-out';
    notification.style.zIndex = '1000';
    
    // Set background color based on type
    switch(type) {
        case 'success':
            notification.style.backgroundColor = '#28a745';
            notification.style.color = 'white';
            break;
        case 'error':
            notification.style.backgroundColor = '#dc3545';
            notification.style.color = 'white';
            break;
        default:
            notification.style.backgroundColor = '#17a2b8';
            notification.style.color = 'white';
    }
    
    // Add to document
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.5s ease-in-out';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 500);
    }, 3000);
}

// Add CSS animation for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Add start ride function
async function startRide(rideId) {
    try {
        const response = await fetch(`/driver/rides/${rideId}/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to start ride');
        }

        // Show success message
        showNotification('Ride started successfully', 'success');
        
        // Refresh the ride requests list
        await loadRideRequests();
        
    } catch (error) {
        console.error('Error starting ride:', error);
        showNotification(error.message, 'error');
    }
} 