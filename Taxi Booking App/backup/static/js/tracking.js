// Export the DriverTracker class
class DriverTracker {
    constructor(map, token) {
        this.map = map;
        this.token = token;
        this.socket = null;
        this.marker = null;
        this.rideId = null;
        this.pickupMarker = null;
        this.dropoffMarker = null;
        this.route = null;
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

        // Create driver marker if it doesn't exist
        if (!this.marker) {
            const el = document.createElement('div');
            el.className = 'marker driver-marker';
            el.style.backgroundImage = 'url(/static/images/taxi-marker.svg)';
            el.style.width = '32px';
            el.style.height = '32px';
            el.style.backgroundSize = 'cover';

            this.marker = new mapboxgl.Marker(el)
                .setLngLat([0, 0])
                .addTo(this.map);
        }
    }

    showRideLocations(data) {
        console.log('Showing ride locations:', data); // Debug log

        // Remove existing markers and route
        if (this.pickupMarker) {
            console.log('Removing existing pickup marker');
            this.pickupMarker.remove();
        }
        if (this.dropoffMarker) {
            console.log('Removing existing dropoff marker');
            this.dropoffMarker.remove();
        }
        if (this.route && this.map.getLayer('route')) {
            console.log('Removing existing route');
            this.map.removeLayer('route');
            this.map.removeSource('route');
        }

        // Create pickup marker
        const pickupEl = document.createElement('div');
        pickupEl.className = 'marker pickup-marker';
        pickupEl.style.backgroundImage = 'url(/static/images/pickup-marker.svg)';
        pickupEl.style.width = '24px';
        pickupEl.style.height = '24px';
        pickupEl.style.backgroundSize = 'cover';

        console.log('Creating pickup marker at:', [data.pickup_lon, data.pickup_lat]);
        this.pickupMarker = new mapboxgl.Marker(pickupEl)
            .setLngLat([data.pickup_lon, data.pickup_lat])
            .addTo(this.map);

        // Create dropoff marker
        const dropoffEl = document.createElement('div');
        dropoffEl.className = 'marker dropoff-marker';
        dropoffEl.style.backgroundImage = 'url(/static/images/dropoff-marker.svg)';
        dropoffEl.style.width = '24px';
        dropoffEl.style.height = '24px';
        dropoffEl.style.backgroundSize = 'cover';

        console.log('Creating dropoff marker at:', [data.dropoff_lon, data.dropoff_lat]);
        this.dropoffMarker = new mapboxgl.Marker(dropoffEl)
            .setLngLat([data.dropoff_lon, data.dropoff_lat])
            .addTo(this.map);

        // Add route between pickup and dropoff
        this.addRoute(data.pickup_lon, data.pickup_lat, data.dropoff_lon, data.dropoff_lat);

        // Fit map to show all markers with padding
        const bounds = new mapboxgl.LngLatBounds()
            .extend([data.pickup_lon, data.pickup_lat])
            .extend([data.dropoff_lon, data.dropoff_lat]);

        console.log('Fitting map to bounds:', bounds);
        this.map.fitBounds(bounds, { 
            padding: 100,
            maxZoom: 15
        });
    }

    addRoute(startLon, startLat, endLon, endLat) {
        console.log('Adding route between:', 
            [startLon, startLat], 'and', [endLon, endLat]);

        // Get route from Mapbox Directions API
        fetch(`https://api.mapbox.com/directions/v5/mapbox/driving/${startLon},${startLat};${endLon},${endLat}?geometries=geojson&access_token=${mapboxgl.accessToken}`)
            .then(response => response.json())
            .then(data => {
                if (data.routes && data.routes[0]) {
                    const route = data.routes[0].geometry;
                    console.log('Route data received:', route);

                    // Remove existing route if it exists
                    if (this.map.getLayer('route')) {
                        this.map.removeLayer('route');
                    }
                    if (this.map.getSource('route')) {
                        this.map.removeSource('route');
                    }

                    // Add the route to the map
                    this.map.addSource('route', {
                        type: 'geojson',
                        data: {
                            type: 'Feature',
                            properties: {},
                            geometry: route
                        }
                    });

                    this.map.addLayer({
                        id: 'route',
                        type: 'line',
                        source: 'route',
                        layout: {
                            'line-join': 'round',
                            'line-cap': 'round'
                        },
                        paint: {
                            'line-color': '#3bb2d0',
                            'line-width': 4
                        }
                    });

                    console.log('Route added to map');
                } else {
                    console.error('No route found in response:', data);
                }
            })
            .catch(error => {
                console.error('Error fetching route:', error);
            });
    }

    stopTracking() {
        if (this.rideId) {
            this.socket.emit('leave_ride', {
                ride_id: this.rideId
            });
            this.rideId = null;

            // Remove all markers and route
            if (this.marker) this.marker.remove();
            if (this.pickupMarker) this.pickupMarker.remove();
            if (this.dropoffMarker) this.dropoffMarker.remove();
            if (this.route && this.map.getLayer('route')) {
                this.map.removeLayer('route');
                this.map.removeSource('route');
            }
            
            this.marker = null;
            this.pickupMarker = null;
            this.dropoffMarker = null;
            this.route = null;
        }
    }

    updateDriverLocation(location) {
        if (this.marker) {
            // Update marker position
            this.marker.setLngLat([location.lon, location.lat]);

            // Center map on marker with smooth animation
            this.map.easeTo({
                center: [location.lon, location.lat],
                duration: 1000
            });
        }
    }
}

// Export the DriverLocationUpdater class
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

// Remove the map initialization code and only export the classes
window.DriverTracker = DriverTracker;
window.DriverLocationUpdater = DriverLocationUpdater; 