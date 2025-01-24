// Initialize globals
let map;
let marker;
let searchBox;
let isOnline = navigator.onLine;
let API_KEY;

// Move initializeMap function definition before it's called
function initializeMap() {
    if (!isOnline || !API_KEY) {
        showError('No internet connection or missing API key');
        return;
    }

    try {
        map = tt.map({
            key: API_KEY,
            container: "map",
            center: [31.2357, 30.0444], // Cairo coordinates
            zoom: 13,
            interactive: true,
        });

        // Add loading error handler
        map.on('error', (e) => {
            showError('Failed to load map. Please check your internet connection.');
        });

        try {
            // Create SearchBox directly with services instance
            searchBox = new tt.plugins.SearchBox(tt.services, {
                minNumberOfCharacters: 3,
                showSearchButton: true,
                placeholder: "Search location...",
                searchOptions: {
                    key: API_KEY,
                    language: "en-GB",
                },
            });

            // Add SearchBox to map
            map.addControl(searchBox, "top-left");

            // Handle result selection
            searchBox.on("tomtom.searchbox.resultselected", function (event) {
                const result = event.data.result;
                if (result.position) {
                    const coords = [result.position.lng, result.position.lat];
                    map.flyTo({
                        center: coords,
                        zoom: 15,
                    });
                    placeMarker(coords);
                    getAddress({
                        lng: result.position.lng,
                        lat: result.position.lat,
                    });
                }
            });
        } catch (error) {
            console.error("SearchBox initialization error:", error);
            showError("Failed to initialize search");
        }

        // Add marker on map click
        map.on("click", (e) => {
            // TomTom click event provides coordinates in {lng, lat} format
            const clickedPoint = e.lngLat;
            placeMarker(clickedPoint);
            getAddress(clickedPoint);
        });
    } catch (error) {
        console.error("Map initialization error:", error);
        showError('Failed to initialize map');
    }
}

async function fetchApiKey() {
    try {
        console.log('Fetching API key...');
        const response = await fetch('/api/v1/config');
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Config data received:', data);
        
        if (!data.TOMTOM_API_KEY) {
            throw new Error('API key not found in response');
        }
        
        API_KEY = data.TOMTOM_API_KEY;
        initializeMap();
    } catch (error) {
        console.error("Error fetching API key:", error);
        showError('Failed to load configuration: ' + error.message);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    fetchApiKey();  // Get API key first
  const locationPrompt = document.getElementById("locationPrompt");
  const mapSection = document.getElementById("mapSection");

  // Handle stored location choice
  document.getElementById("useStoredLocation").addEventListener("click", () => {
    window.location.href = "/payment";
  });

  document.getElementById("selectNewLocation").addEventListener("click", () => {
    locationPrompt.style.display = "none";
    mapSection.style.display = "block";
    initializeMap();
  });

  // Handle geolocation
  document.getElementById("geolocateMe").addEventListener("click", () => {
    if (!navigator.geolocation) {
      showError("Geolocation is not supported by your browser");
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const coords = {
          lng: position.coords.longitude,
          lat: position.coords.latitude,
        };
        map.flyTo({
          center: [coords.lng, coords.lat],
          zoom: 15,
        });
        placeMarker([coords.lng, coords.lat]);
        getAddress(coords);
      },
      (error) => {
        handleLocationError(error);
      }
    );
  });

  // Form submission
  document.getElementById("locationForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!marker) {
        showError("Please select a location on the map");
        return;
    }

    const countryCode = document.getElementById("country-code").value;
    const phoneNumber = document.getElementById("phone").value;
    const fullPhone = countryCode + phoneNumber;

    // Validate phone number based on country code
    const phoneRegex = {
        // Middle East & North Africa
        '+20': /^\+20[0-9]{10}$/, // Egypt
        '+966': /^\+966[0-9]{9}$/, // Saudi Arabia
        '+971': /^\+971[0-9]{9}$/, // UAE
        '+974': /^\+974[0-9]{8}$/, // Qatar
        '+965': /^\+965[0-9]{8}$/, // Kuwait
        '+968': /^\+968[0-9]{8}$/, // Oman
        '+973': /^\+973[0-9]{8}$/, // Bahrain
        '+962': /^\+962[0-9]{9}$/, // Jordan
        '+961': /^\+961[0-9]{8}$/, // Lebanon
        '+963': /^\+963[0-9]{9}$/, // Syria
        '+964': /^\+964[0-9]{10}$/, // Iraq
        '+216': /^\+216[0-9]{8}$/, // Tunisia
        '+213': /^\+213[0-9]{9}$/, // Algeria
        '+212': /^\+212[0-9]{9}$/, // Morocco
        '+218': /^\+218[0-9]{9}$/, // Libya
        '+249': /^\+249[0-9]{9}$/, // Sudan

        // Europe
        '+44': /^\+44[0-9]{10}$/, // UK
        '+33': /^\+33[0-9]{9}$/, // France
        '+49': /^\+49[0-9]{11}$/, // Germany
        '+39': /^\+39[0-9]{10}$/, // Italy
        '+34': /^\+34[0-9]{9}$/, // Spain

        // North America
        '+1': /^\+1[0-9]{10}$/, // USA/Canada

        // Asia
        '+86': /^\+86[0-9]{11}$/, // China
        '+91': /^\+91[0-9]{10}$/, // India
        '+81': /^\+81[0-9]{10}$/, // Japan
        '+82': /^\+82[0-9]{10}$/, // South Korea
    };

    if (!phoneRegex[countryCode].test(fullPhone)) {
        showError("Please enter a valid phone number for " +
                 countryCode + " (including country code)");
        return;
    }

    try {
        const response = await fetch("/api/v1/location/save", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                lat: marker.getLngLat().lat,
                lng: marker.getLngLat().lng,
                address: document.getElementById("address").value,
                phone: fullPhone,
                instructions: document.getElementById("instructions").value
            })
        });

        if (response.ok) {
            window.location.href = "/payment";
        } else {
            throw new Error("Failed to save location");
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

  marker = new tt.Marker().setLngLat(coordinates).addTo(map);
}

function getAddress(coords) {
  if (!navigator.onLine) {
    showError('No internet connection. Please check your connection and try again.');
    return;
  }

  tt.services
    .reverseGeocode({
      key: API_KEY,
      position: coords,
    })
    .then((response) => {
      if (response.addresses && response.addresses.length > 0) {
        document.getElementById("address").value =
          response.addresses[0].address.freeformAddress;
      }
    })
    .catch((error) => {
      showError('Could not fetch address. Please check your internet connection.');
      console.error(error);
    });
}

function handleLocationError(error) {
  switch (error.code) {
    case error.PERMISSION_DENIED:
      showError("Please allow location access to use this feature");
      break;
    case error.POSITION_UNAVAILABLE:
      showError("Location information unavailable");
      break;
    case error.TIMEOUT:
      showError("Location request timed out");
      break;
    default:
      showError("An unknown error occurred");
      break;
  }
}

// Add internet connectivity check
window.addEventListener('online', () => {
  isOnline = true;
  showError('Internet connection restored', 'success');
  // Reinitialize map if it wasn't initialized
  if (!map && document.getElementById('mapSection').style.display !== 'none') {
    initializeMap();
  }
});

window.addEventListener('offline', () => {
  isOnline = false;
  showError('No internet connection. Please check your connection and try again.', 'error');
});

// Update showError function to handle different types
function showError(message, type = 'error') {
  const existingError = document.querySelector('.error-message');
  if (existingError) {
    existingError.remove();
  }

  const errorDiv = document.createElement('div');
  errorDiv.className = `error-message ${type === 'success' ? 'success' : ''}`;
  errorDiv.textContent = message;

  document.body.appendChild(errorDiv);

  // Remove the message after 5 seconds unless it's a no-internet message
  if (message !== 'No internet connection. Please check your connection and try again.') {
    setTimeout(() => {
      if (errorDiv && errorDiv.parentNode) {
        errorDiv.remove();
      }
    }, 5000);
  }
}

// Add connection check to API calls
async function searchLocation(query) {
  if (!navigator.onLine) {
    showError('No internet connection. Please check your connection and try again.');
    return;
  }

  try {
    const response = await tt.services
      .fuzzySearch({
        key: API_KEY,
        query: query,
        language: "en-GB",
        limit: 1,
      })
      .go();

    if (response.results && response.results.length > 0) {
      const result = response.results[0];
      const coords = [result.position.lng, result.position.lat];

      map.flyTo({
        center: coords,
        zoom: 15,
      });

      placeMarker(coords);
      getAddress({
        lng: result.position.lng,
        lat: result.position.lat,
      });
    } else {
      showError("Location not found");
    }
  } catch (error) {
    console.error("Search error:", error);
    showError("Failed to search location. Please check your internet connection.");
  }
}
