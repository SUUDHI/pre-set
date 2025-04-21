// Load ride history
async function loadRideHistory() {
    try {
        const response = await fetch('http://localhost:5000/ride/history', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        const data = await response.json();
        const tableBody = document.getElementById('ridesTableBody');
        
        if (response.ok && data.rides) {
            tableBody.innerHTML = data.rides.map(ride => `
                <tr>
                    <td>${ride.RideID}</td>
                    <td>
                        <span class="status-badge status-${ride.Status.toLowerCase()}">
                            ${ride.Status}
                        </span>
                    </td>
                    <td>${ride.PickupLat}, ${ride.PickupLon}</td>
                    <td>${ride.DropoffLat}, ${ride.DropoffLon}</td>
                    <td>₹${ride.Fare}</td>
                    <td>
                        ${ride.Status === 'REQUESTED' ? `
                            <button onclick="cancelRide(${ride.RideID})" class="btn-secondary btn-danger">
                                Cancel
                            </button>
                        ` : ''}
                    </td>
                </tr>
            `).join('');
        } else {
            throw new Error(data.error || 'Failed to load rides');
        }
    } catch (error) {
        console.error('Error loading rides:', error);
    }
}

// Book a new ride
document.getElementById('bookingForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        pickup_lat: parseFloat(document.getElementById('pickupLat').value),
        pickup_lon: parseFloat(document.getElementById('pickupLon').value),
        dropoff_lat: parseFloat(document.getElementById('dropoffLat').value),
        dropoff_lon: parseFloat(document.getElementById('dropoffLon').value)
    };

    try {
        const response = await fetch('http://localhost:5000/ride/request', {
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
            e.target.reset();
            loadRideHistory();
        } else {
            alert(data.error || 'Failed to book ride');
        }
    } catch (error) {
        alert('An error occurred while booking the ride');
    }
});

// Cancel a ride
async function cancelRide(rideId) {
    if (!confirm('Are you sure you want to cancel this ride?')) {
        return;
    }

    try {
        const response = await fetch(`http://localhost:5000/ride/${rideId}/cancel`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                cancellation_reason: 'Cancelled by user'
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            alert('Ride cancelled successfully');
            loadRideHistory();
        } else {
            alert(data.error || 'Failed to cancel ride');
        }
    } catch (error) {
        alert('An error occurred while cancelling the ride');
    }
}

// Load ride history on page load
loadRideHistory();

// Refresh ride history every 30 seconds
setInterval(loadRideHistory, 30000); 