// Load ride requests
async function loadRideRequests() {
    try {
        const response = await fetch('http://localhost:5000/driver/rides/requested', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        const data = await response.json();
        const tableBody = document.getElementById('requestsTableBody');
        
        if (response.ok && data.rides) {
            tableBody.innerHTML = data.rides.map(ride => `
                <tr>
                    <td>${ride.RideID}</td>
                    <td>${ride.PickupLat}, ${ride.PickupLon}</td>
                    <td>${ride.DropoffLat}, ${ride.DropoffLon}</td>
                    <td>
                        <span class="status-badge status-${ride.Status.toLowerCase()}">
                            ${ride.Status}
                        </span>
                    </td>
                    <td>
                        ${getActionButtons(ride)}
                    </td>
                </tr>
            `).join('');
        } else {
            throw new Error(data.error || 'Failed to load ride requests');
        }
    } catch (error) {
        console.error('Error loading ride requests:', error);
    }
}

// Get action buttons based on ride status
function getActionButtons(ride) {
    switch (ride.Status) {
        case 'REQUESTED':
            return `
                <button onclick="acceptRide(${ride.RideID})" class="btn-secondary">
                    Accept
                </button>
            `;
        case 'ACCEPTED':
            return `
                <button onclick="startRide(${ride.RideID})" class="btn-secondary">
                    Start
                </button>
            `;
        case 'IN_PROGRESS':
            return `
                <button onclick="completeRide(${ride.RideID})" class="btn-secondary">
                    Complete
                </button>
            `;
        default:
            return '';
    }
}

// Accept a ride
async function acceptRide(rideId) {
    try {
        const response = await fetch(`http://localhost:5000/driver/rides/${rideId}/accept`, {
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
            alert(data.error || 'Failed to accept ride');
        }
    } catch (error) {
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
        const response = await fetch('http://localhost:5000/driver/location', {
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
        const response = await fetch('http://localhost:5000/driver/status', {
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
        alert('An error occurred while updating status');
    }
});

// Load ride requests on page load
loadRideRequests();

// Refresh ride requests every 30 seconds
setInterval(loadRideRequests, 30000); 