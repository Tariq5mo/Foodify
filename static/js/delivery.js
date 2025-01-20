// Initialize globals
let map;
let marker;
let searchBox;

// TomTom API key
const API_KEY = "gTnO8GY8uqFMsvsF9yz3wZdxMFWBR0kJ";

document.addEventListener('DOMContentLoaded', () => {
    const locationPrompt = document.getElementById('locationPrompt');
    const mapSection = document.getElementById('mapSection');

    // Handle stored location choice
    document.getElementById('useStoredLocation').addEventListener('click', () => {
        window.location.href = '/payment';
    });

    document.getElementById('selectNewLocation').addEventListener('click', () => {
        locationPrompt.style.display = 'none';
        mapSection.style.display = 'block';
        initializeMap();
    });

    // Initialize map
    function initializeMap() {
        try {
            map = tt.map({
                key: API_KEY,
                container: 'map',
                center: [31.2357, 30.0444], // Cairo coordinates
                zoom: 13,
                interactive: true // Ensure map is interactive
            });

            // Add search box with improved configuration
            try {
                const searchBoxService = new tt.services.fuzzySearch({
                    key: API_KEY,
                    idleTimePress: 100,  // Reduced for faster response
                    language: 'en-GB',
                    radius: 50000, // 50km radius
                    limit: 5  // Number of suggestions
                });

                // Create SearchBox with enhanced configuration
                searchBox = new tt.plugins.SearchBox(tt.services.fuzzySearch, {
                    minNumberOfCharacters: 2,
                    searchOptions: {
                        key: API_KEY,
                        language: 'en-GB'
                    },
                    autocompleteOptions: {
                        key: API_KEY,
                        language: 'en-GB'
                    },
                    labels: {
                        placeholder: 'Search for a location'
                    }
                });

                // Add SearchBox to map
                map.addControl(searchBox, 'top-left');

                // Handle result selection
                searchBox.on('tomtom.searchbox.resultselected', function(event) {
                    const result = event.data.result;
                    if (result.position) {
                        const coords = [result.position.lng, result.position.lat];
                        map.flyTo({
                            center: coords,
                            zoom: 15
                        });
                        placeMarker(coords);
                        getAddress({
                            lng: result.position.lng,
                            lat: result.position.lat
                        });
                    }
                });

                // Handle enter key press
                searchBox.getSearchBox().addEventListener('keyup', function(e) {
                    if (e.key === 'Enter') {
                        const searchQuery = e.target.value;
                        if (searchQuery.length >= 2) {
                            searchLocation(searchQuery);
                        }
                    }
                });

            } catch (error) {
                console.error('SearchBox initialization error:', error);
                showError(error);
            }

            // Add marker on map click
            map.on('click', (e) => {
                // TomTom click event provides coordinates in {lng, lat} format
                const clickedPoint = e.lngLat;
                placeMarker(clickedPoint);
                getAddress(clickedPoint);
            });
        } catch (error) {
            console.error('Map initialization error:', error);
            showError(error);
        }
    }

    // Handle geolocation
    document.getElementById('geolocateMe').addEventListener('click', () => {
        if (!navigator.geolocation) {
            showError('Geolocation is not supported by your browser');
            return;
        }

        navigator.geolocation.getCurrentPosition(
            position => {
                const coords = {
                    lng: position.coords.longitude,
                    lat: position.coords.latitude
                };
                map.flyTo({
                    center: [coords.lng, coords.lat],
                    zoom: 15
                });
                placeMarker([coords.lng, coords.lat]);
                getAddress(coords);
            },
            error => {
                handleLocationError(error);
            }
        );
    });

    // Form submission
    document.getElementById('locationForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!marker) {
            showError('Please select a location on the map');
            return;
        }

        try {
            const response = await fetch('/api/v1/location/save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    lat: marker.getLngLat().lat,
                    lng: marker.getLngLat().lng,
                    address: document.getElementById('address').value,
                    instructions: document.getElementById('instructions').value
                })
            });

            if (response.ok) {
                window.location.href = '/payment';
            } else {
                throw new Error('Failed to save location');
            }
        } catch (error) {
            showError(error.message);
        }
    });
});

function placeMarker(lngLat) {
    if (marker) marker.remove();

    // Handle both array and object formats of coordinates
    let coordinates;
    if (Array.isArray(lngLat)) {
        coordinates = lngLat;
    } else if (lngLat.lng && lngLat.lat) {
        coordinates = [lngLat.lng, lngLat.lat];
    } else {
        coordinates = [lngLat[0], lngLat[1]];
    }

    marker = new tt.Marker()
        .setLngLat(coordinates)
        .addTo(map);
}

function getAddress(coords) {
    tt.services.reverseGeocode({
        key: API_KEY,
        position: coords
    })
    .then(response => {
        if (response.addresses && response.addresses.length > 0) {
            document.getElementById('address').value = response.addresses[0].address.freeformAddress;
        }
    })
    .catch(error => {
        showError('Could not fetch address');
        console.error(error);
    });
}

function handleLocationError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            showError('Please allow location access to use this feature');
            break;
        case error.POSITION_UNAVAILABLE:
            showError('Location information unavailable');
            break;
        case error.TIMEOUT:
            showError('Location request timed out');
            break;
        default:
            showError('An unknown error occurred');
            break;
    }
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    document.querySelector('.delivery-container').prepend(errorDiv);
    setTimeout(() => errorDiv.remove(), 5000);
}

<<<<<<< HEAD
// Add this new function to handle manual searches
async function searchLocation(query) {
    try {
        const response = await tt.services.fuzzySearch({
            key: API_KEY,
            query: query,
            language: 'en-GB',
            limit: 1
        }).go();

        if (response.results && response.results.length > 0) {
            const result = response.results[0];
            const coords = [result.position.lng, result.position.lat];

            map.flyTo({
                center: coords,
                zoom: 15
            });

            placeMarker(coords);
            getAddress({
                lng: result.position.lng,
                lat: result.position.lat
            });
        } else {
            showError('Location not found');
        }
    } catch (error) {
        console.error('Search error:', error);
        showError('Failed to search location');
    }
}
=======
document.getElementById('delivery-form').addEventListener('submit', (e) => {
    e.preventDefault();

    if (!validateDeliveryForm()) return;

    // Save delivery info
    const deliveryDetails = {
        address: document.getElementById('address-input').value,
        contactName: document.getElementById('contact-name').value,
        phone: document.getElementById('phone').value,
        instructions: document.getElementById('instructions').value,
        location: marker ? {
            lat: marker.getPosition().lat(),
            lng: marker.getPosition().lng()
        } : null
    };

    // Store and navigate
    localStorage.setItem('deliveryDetails', JSON.stringify(deliveryDetails));
    window.location.href = 'payment.html';
}); 

>>>>>>> 071639e9a35a8e0fbfaf210325a8d9b6902e7f4a
