// Initialize Mapbox
import { FARE_CONSTANTS } from './config.js';

mapboxgl.accessToken = 'YOUR_MAPBOX_ACCESS_TOKEN'; // Replace with your Mapbox token

let map;
let pickupMarker;
let dropoffMarker;
let directions;
let geocoder;

function initMap(center) {
    // Initialize map
    map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v12',
        center: [center.lng, center.lat],
        zoom: 15
    });

    // Add navigation controls
    map.addControl(new mapboxgl.NavigationControl());

    // Initialize geocoder
    geocoder = new MapboxGeocoder({
        accessToken: mapboxgl.accessToken,
        mapboxgl: mapboxgl,
        marker: false
    });

    // Add geocoder to the map
    map.addControl(geocoder);

    // Initialize pickup and dropoff markers
    pickupMarker = new mapboxgl.Marker({
        color: '#4CAF50',
        draggable: true
    });

    dropoffMarker = new mapboxgl.Marker({
        color: '#f44336',
        draggable: true
    });

    // Add event listeners for marker dragging
    pickupMarker.on('dragend', () => {
        updatePickupLocation(pickupMarker.getLngLat());
    });

    dropoffMarker.on('dragend', () => {
        updateDropoffLocation(dropoffMarker.getLngLat());
    });

    // Add geocoder result handlers
    geocoder.on('result', (e) => {
        const result = e.result;
        const inputId = document.activeElement.id;

        if (inputId === 'pickup-location') {
            updatePickupLocation(result.center);
        } else if (inputId === 'dropoff-location') {
            updateDropoffLocation(result.center);
        }
    });

    // Get user's current location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                
                map.setCenter([userLocation.lng, userLocation.lat]);
                
                // Set pickup location to user's current location
                const pickupInput = document.getElementById('pickup-location');
                if (pickupInput) {
                    // Reverse geocode to get address
                    fetch(`https://api.mapbox.com/geocoding/v5/mapbox.places/${userLocation.lng},${userLocation.lat}.json?access_token=${mapboxgl.accessToken}`)
                        .then(response => response.json())
                        .then(data => {
                            if (data.features && data.features[0]) {
                                pickupInput.value = data.features[0].place_name;
                                updatePickupLocation(userLocation);
                            }
                        });
                }
            },
            (error) => {
                console.error('Error getting location:', error);
            }
        );
    }
}

function updatePickupLocation(location) {
    pickupMarker.setLngLat([location.lng, location.lat]).addTo(map);
    calculateRoute();
}

function updateDropoffLocation(location) {
    dropoffMarker.setLngLat([location.lng, location.lat]).addTo(map);
    calculateRoute();
}

function calculateRoute() {
    if (!pickupMarker || !dropoffMarker) return;

    const pickup = pickupMarker.getLngLat();
    const dropoff = dropoffMarker.getLngLat();

    // Remove existing route if any
    if (directions) {
        directions.remove();
    }

    // Calculate route using Mapbox Directions API
    fetch(`https://api.mapbox.com/directions/v5/mapbox/driving/${pickup.lng},${pickup.lat};${dropoff.lng},${dropoff.lat}?geometries=geojson&access_token=${mapboxgl.accessToken}`)
        .then(response => response.json())
        .then(data => {
            if (data.routes && data.routes[0]) {
                const route = data.routes[0];
                
                // Add route to map
                directions = new mapboxgl.Popup({ offset: 25 })
                    .setLngLat([pickup.lng, pickup.lat])
                    .setHTML(`<div class="route-info">
                        <p>Distance: ${(route.distance / 1000).toFixed(1)} km</p>
                        <p>Duration: ${Math.round(route.duration / 60)} min</p>
                    </div>`)
                    .addTo(map);

                // Calculate estimated fare
                const distance = route.distance / 1000; // in kilometers
                const duration = route.duration / 60; // in minutes
                
                // Calculate fare using constants from config.js
                const estimatedFare = FARE_CONSTANTS.BASE_FARE + 
                    (distance * FARE_CONSTANTS.RATE_PER_KM) + 
                    (duration * FARE_CONSTANTS.PER_MINUTE_RATE);
                
                // Update fare display
                const fareElement = document.querySelector('.estimated-fare .amount');
                if (fareElement) {
                    fareElement.textContent = `$${estimatedFare.toFixed(2)}`;
                }
            }
        });
}

function updateLocation(location) {
    if (map) {
        map.setCenter([location.longitude, location.latitude]);
        if (pickupMarker) {
            pickupMarker.setLngLat([location.longitude, location.latitude]);
        }
    }
}

// Export functions for use in other modules
export { initMap, updatePickupLocation, updateDropoffLocation, updateLocation }; 