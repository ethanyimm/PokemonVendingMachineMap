// Global variables
let map;
let markers = [];
let allLocations = [];

// Initialize the application
async function initMap() {
    // Create map centered on US
    map = L.map('map').setView([39.8283, -98.5795], 4);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);
    
    // Load locations from API
    await loadLocations();
    
    // Add event listeners
    document.getElementById('searchInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchLocations();
        }
    });
}

// Load all locations from API
async function loadLocations() {
    try {
        const response = await fetch('http://localhost:8000/api/locations');
        allLocations = await response.json();
        
        // Update location count
        document.getElementById('locationCount').textContent = 
            `📍 ${allLocations.length} vending machines found across the US`;
        
        // Add all markers to map
        addMarkersToMap(allLocations);
        
        // Populate state filter
        populateStateFilter();
        
    } catch (error) {
        console.error('Error loading locations:', error);
        document.getElementById('locationCount').textContent = 
            'Error loading locations. Make sure the backend server is running.';
    }
}

// Add markers to the map
function addMarkersToMap(locations) {
    // Clear existing markers
    clearMarkers();
    
    // Create custom icon
    const pokemonIcon = L.icon({
        iconUrl: 'images/pokeballmarker.jpg',
        iconSize: [30, 30],
        iconAnchor: [15, 30],
        popupAnchor: [0, -30]
    });
    
    // Add each location as a marker
    locations.forEach(location => {
        if (location.latitude && location.longitude) {
            const marker = L.marker([location.latitude, location.longitude], {
                icon: pokemonIcon
            }).addTo(map);
            
            marker.bindPopup(`
                <div class="popup-content">
                    <h3>${location.name}</h3>
                    <p><strong>Address:</strong> ${location.address}</p>
                    <p><strong>City:</strong> ${location.city}, ${location.state}</p>
                    <p><strong>Type:</strong> ${location.type || 'Retail'}</p>
                </div>
            `);
            
            markers.push(marker);
        }
    });
}

// Clear all markers from map
function clearMarkers() {
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];
}

// Populate state dropdown filter
function populateStateFilter() {
    const stateFilter = document.getElementById('stateFilter');
    const states = [...new Set(allLocations.map(loc => loc.state))].sort();
    
    states.forEach(state => {
        const option = document.createElement('option');
        option.value = state;
        option.textContent = state;
        stateFilter.appendChild(option);
    });
}

// Search locations by text
function searchLocations() {
    const searchText = document.getElementById('searchInput').value.toLowerCase();
    
    if (!searchText) {
        addMarkersToMap(allLocations);
        return;
    }
    
    const filtered = allLocations.filter(location => 
        location.name.toLowerCase().includes(searchText) ||
        location.city.toLowerCase().includes(searchText) ||
        location.state.toLowerCase().includes(searchText) ||
        location.address.toLowerCase().includes(searchText)
    );
    
    addMarkersToMap(filtered);
    document.getElementById('locationCount').textContent = 
        `📍 ${filtered.length} machines found for "${searchText}"`;
}

// Filter by state
function filterByState() {
    const state = document.getElementById('stateFilter').value;
    
    if (!state) {
        addMarkersToMap(allLocations);
        document.getElementById('locationCount').textContent = 
            `📍 ${allLocations.length} vending machines found across the US`;
        return;
    }
    
    const filtered = allLocations.filter(location => location.state === state);
    addMarkersToMap(filtered);
    document.getElementById('locationCount').textContent = 
        `📍 ${filtered.length} machines found in ${state}`;
}

// Find nearby locations using geolocation
function findNearby() {
    if (!navigator.geolocation) {
        alert('Geolocation is not supported by your browser');
        return;
    }
    
    navigator.geolocation.getCurrentPosition(
        async (position) => {
            const { latitude, longitude } = position.coords;
            
            // Center map on user's location
            map.setView([latitude, longitude], 13);
            
            // Show user location marker
            const userMarker = L.marker([latitude, longitude])
                .addTo(map)
                .bindPopup('Your location')
                .openPopup();
            
            // Load nearby locations from API
            try {
                const response = await fetch(
                    `http://localhost:8000/api/locations/nearby?lat=${latitude}&lng=${longitude}&radius_km=50`
                );
                const nearbyLocations = await response.json();
                
                addMarkersToMap(nearbyLocations);
                document.getElementById('locationCount').textContent = 
                    `📍 ${nearbyLocations.length} machines near your location`;
                    
            } catch (error) {
                console.error('Error loading nearby locations:', error);
            }
        },
        (error) => {
            alert('Unable to get your location. Please enable location services.');
        }
    );
}

// Initialize the map when page loads
document.addEventListener('DOMContentLoaded', initMap);