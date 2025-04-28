class DriverTracker {
    constructor(map, token) {
        this.map = map;
        this.token = token;
        this.socket = null;
        this.marker = null;
        this.rideId = null;
    }

    connect() {
        // Connect to WebSocket server
        this.socket = io();

        // Handle connection events
        this.socket.on('connect', () => {
            console.log('Connected to WebSocket server');
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from WebSocket server');
        });

        this.socket.on('error', (data) => {
            console.error('WebSocket error:', data.message);
        });

        // Handle location updates
        this.socket.on('location_update', (data) => {
            this.updateDriverLocation(data.location);
        });
    }

    startTracking(rideId) {
        this.rideId = rideId;
        
        // Join the ride room
        this.socket.emit('join_ride', {
            token: this.token,
            ride_id: rideId
        });

        // Create marker if it doesn't exist
        if (!this.marker) {
            // Create a DOM element for the marker
            const el = document.createElement('div');
            el.className = 'marker';
            el.style.backgroundImage = 'url(/static/images/taxi-marker.png)';
            el.style.width = '32px';
            el.style.height = '32px';
            el.style.backgroundSize = '100%';

            // Add marker to map
            this.marker = new mapboxgl.Marker(el)
                .setLngLat([0, 0])
                .addTo(this.map);
        }
    }

    stopTracking() {
        if (this.rideId) {
            this.socket.emit('leave_ride', {
                ride_id: this.rideId
            });
            this.rideId = null;

            // Remove marker from map
            if (this.marker) {
                this.marker.remove();
                this.marker = null;
            }
        }
    }

    updateDriverLocation(location) {
        if (this.marker) {
            // Update marker position
            this.marker.setLngLat([location.lon, location.lat]);

            // Center map on marker
            this.map.easeTo({
                center: [location.lon, location.lat],
                duration: 1000
            });
        }
    }
}

// For driver app
class DriverLocationUpdater {
    constructor(token) {
        this.token = token;
        this.socket = null;
        this.rideId = null;
        this.watchId = null;
    }

    connect() {
        this.socket = io();

        this.socket.on('connect', () => {
            console.log('Connected to WebSocket server');
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from WebSocket server');
        });

        this.socket.on('error', (data) => {
            console.error('WebSocket error:', data.message);
        });
    }

    startUpdating(rideId) {
        this.rideId = rideId;
        
        // Join the ride room
        this.socket.emit('join_ride', {
            token: this.token,
            ride_id: rideId
        });

        // Start watching position
        this.watchId = navigator.geolocation.watchPosition(
            (position) => {
                const location = {
                    lat: position.coords.latitude,
                    lon: position.coords.longitude
                };

                // Send location update
                this.socket.emit('driver_location_update', {
                    token: this.token,
                    ride_id: this.rideId,
                    location: location
                });
            },
            (error) => {
                console.error('Geolocation error:', error);
            },
            {
                enableHighAccuracy: true,
                maximumAge: 0,
                timeout: 5000
            }
        );
    }

    stopUpdating() {
        if (this.watchId) {
            navigator.geolocation.clearWatch(this.watchId);
            this.watchId = null;
        }

        if (this.rideId) {
            this.socket.emit('leave_ride', {
                ride_id: this.rideId
            });
            this.rideId = null;
        }
    }
}

// Initialize Mapbox
mapboxgl.accessToken = 'pk.eyJ1Ijoic3V1ZGhpIiwiYSI6ImNtOWs0cW9vMDBpdmwybXM2c21ramNmZTQifQ.xsTF7EaOpYKwX4VaVMNgCQ';
const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [0, 0],
    zoom: 2
});

// Add navigation controls
map.addControl(new mapboxgl.NavigationControl());

// Initialize driver tracker
const tracker = new DriverTracker(map, localStorage.getItem('token'));
tracker.connect();

// Handle map clicks
map.on('click', (e) => {
    const lngLat = e.lngLat;
    const pickupLat = document.getElementById('pickupLat');
    const pickupLon = document.getElementById('pickupLon');
    const dropoffLat = document.getElementById('dropoffLat');
    const dropoffLon = document.getElementById('dropoffLon');

    if (!pickupLat.value || !pickupLon.value) {
        pickupLat.value = lngLat.lat.toFixed(6);
        pickupLon.value = lngLat.lng.toFixed(6);
    } else {
        dropoffLat.value = lngLat.lat.toFixed(6);
        dropoffLon.value = lngLat.lng.toFixed(6);
    }
}); 