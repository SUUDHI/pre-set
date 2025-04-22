let currentRideId = null;
let selectedReason = null;

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
            tableBody.innerHTML = data.rides.map(ride => {
                // Convert status to uppercase for consistent comparison
                const status = ride.Status.toUpperCase();
                const isCancelled = status === 'CANCELLED';
                
                // Format fees
                const fareDisplay = formatCurrency(ride.Fare);
                const cancellationFeeDisplay = formatCurrency(ride.CancellationFee);
                
                return `
                    <tr>
                        <td>#${ride.RideID}</td>
                        <td>
                            <span class="status-badge status-${status.toLowerCase()}">
                                ${status}
                            </span>
                            ${isCancelled && ride.CancellationReason ? `
                                <div class="cancellation-reason">
                                    Reason: ${ride.CancellationReason}
                                </div>
                            ` : ''}
                        </td>
                        <td class="location-cell" title="${formatLocation(ride.PickupLat, ride.PickupLon)}">
                            ${formatLocation(ride.PickupLat, ride.PickupLon)}
                        </td>
                        <td class="location-cell" title="${formatLocation(ride.DropoffLat, ride.DropoffLon)}">
                            ${formatLocation(ride.DropoffLat, ride.DropoffLon)}
                        </td>
                        <td class="fee-cell ${isCancelled ? 'fee-cancelled' : 'fee-normal'}">
                            ${fareDisplay}
                        </td>
                        <td class="fee-cell ${isCancelled ? 'fee-cancelled' : ''}">
                            ${isCancelled ? cancellationFeeDisplay : '-'}
                        </td>
                        <td>
                            ${status === 'REQUESTED' ? `
                                <button onclick="showCancelModal(${ride.RideID})" class="btn-danger">
                                    Cancel Ride
                                </button>
                            ` : status === 'ACCEPTED' ? `
                                <span class="status-badge status-accepted">Driver Assigned</span>
                            ` : ''}
                        </td>
                    </tr>
                `;
            }).join('');
        } else {
            throw new Error(data.error || 'Failed to load rides');
        }
    } catch (error) {
        console.error('Error loading rides:', error);
        tableBody.innerHTML = `
            <tr>
                <td colspan="7" style="text-align: center; padding: 20px;">
                    Failed to load ride history. Please try again later.
                </td>
            </tr>
        `;
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

// Show cancel modal
function showCancelModal(rideId) {
    currentRideId = rideId;
    document.getElementById('cancelModal').style.display = 'block';
    // Reset selections
    selectedReason = null;
    document.querySelectorAll('.reason-item').forEach(item => item.classList.remove('selected'));
    document.getElementById('otherReasonGroup').style.display = 'none';
    document.getElementById('otherReason').value = '';
}

// Close cancel modal
function closeCancelModal() {
    document.getElementById('cancelModal').style.display = 'none';
    currentRideId = null;
    selectedReason = null;
}

// Select a reason
function selectReason(element, reason) {
    // Remove selected class from all items
    document.querySelectorAll('.reason-item').forEach(item => item.classList.remove('selected'));
    // Add selected class to clicked item
    element.classList.add('selected');
    selectedReason = reason;
    
    // Show/hide other reason input
    const otherReasonGroup = document.getElementById('otherReasonGroup');
    if (reason === 'Other') {
        otherReasonGroup.style.display = 'block';
    } else {
        otherReasonGroup.style.display = 'none';
    }
}

// Confirm cancellation
async function confirmCancellation() {
    if (!selectedReason) {
        alert('Please select a cancellation reason');
        return;
    }

    let finalReason = selectedReason;
    if (selectedReason === 'Other') {
        const otherReason = document.getElementById('otherReason').value.trim();
        if (!otherReason) {
            alert('Please specify the other reason');
            return;
        }
        finalReason = otherReason;
    }

    try {
        const response = await fetch(`http://localhost:5000/ride/${currentRideId}/cancel`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                cancellation_reason: finalReason
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            alert('Ride cancelled successfully');
            closeCancelModal();
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