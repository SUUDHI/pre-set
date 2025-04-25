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

// Format datetime for display
function formatDateTime(isoString) {
    if (!isoString) return 'Immediate';
    const date = new Date(isoString);
    return date.toLocaleString();
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

                // Format driver info
                const driverInfo = ride.DriverID ? `
                    <div class="driver-info">
                        <span class="driver-name">${ride.DriverName}</span>
                        <span class="driver-phone">${ride.DriverPhone}</span>
                    </div>
                ` : '';

                // Format pickup time
                const pickupTimeDisplay = formatDateTime(ride.PickupTime);
                
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
                            <div class="pickup-time">
                                Pickup: ${pickupTimeDisplay}
                            </div>
                        </td>
                        <td>${ride.VehicleType || 'Standard'}</td>
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
            throw new Error(data.error || 'Failed to load rides');
        }
    } catch (error) {
        console.error('Error loading rides:', error);
        tableBody.innerHTML = `
            <tr>
                <td colspan="8" style="text-align: center; padding: 20px;">
                    Failed to load ride history. Please try again later.
                </td>
            </tr>
        `;
    }
}

// Load vehicle types
async function loadVehicleTypes() {
    try {
        const response = await fetch('http://localhost:5000/driver/vehicle-types');
        const data = await response.json();
        
        if (response.ok && data) {
            const vehicleTypeSelect = document.getElementById('vehicleType');
            vehicleTypeSelect.innerHTML = data.map(type => `
                <option value="${type.id}">${type.name} - ${type.description} (₹${type.baseRate} base + ₹${type.pricePerKm}/km)</option>
            `).join('');
        } else {
            throw new Error(data.error || 'Failed to load vehicle types');
        }
    } catch (error) {
        console.error('Error loading vehicle types:', error);
        alert('Failed to load vehicle types. Please refresh the page.');
    }
}

// Book a new ride
document.getElementById('bookingForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        pickup_lat: parseFloat(document.getElementById('pickupLat').value),
        pickup_lon: parseFloat(document.getElementById('pickupLon').value),
        dropoff_lat: parseFloat(document.getElementById('dropoffLat').value),
        dropoff_lon: parseFloat(document.getElementById('dropoffLon').value),
        vehicle_type_id: parseInt(document.getElementById('vehicleType').value)
    };

    // Add pickup time if specified
    const pickupTimeInput = document.getElementById('pickupTime').value;
    if (pickupTimeInput) {
        // Convert local datetime to ISO string
        const pickupDate = new Date(pickupTimeInput);
        formData.pickup_time = pickupDate.toISOString();
    }

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
        
        if (response.ok && data.ride_id) {
            alert('Ride booked successfully!');
            e.target.reset();
            await loadRideHistory(); // Wait for ride history to reload
        } else {
            alert(data.error || 'Failed to book ride. Please try again.');
            console.error('Booking error:', data);
        }
    } catch (error) {
        console.error('Error booking ride:', error);
        alert('An error occurred while booking the ride. Please try again.');
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

// Load vehicle types on page load
loadVehicleTypes();

// Refresh ride history every 30 seconds
setInterval(loadRideHistory, 30000); 