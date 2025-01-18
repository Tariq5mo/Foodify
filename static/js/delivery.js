let map;
let marker;
let autocomplete;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: { lat: -34.397, lng: 150.644 }
    });

    // Initialize autocomplete
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('address-input')
    );

    autocomplete.addListener('place_changed', () => {
        const place = autocomplete.getPlace();
        if (!place.geometry) return;

        // Update map
        map.setCenter(place.geometry.location);
        setMarker(place.geometry.location);
    });
}

function getCurrentLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const pos = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                map.setCenter(pos);
                setMarker(pos);
                reverseGeocode(pos);
            },
            () => {
                alert("Error: The Geolocation service failed.");
            }
        );
    }
}

function setMarker(location) {
    if (marker) marker.setMap(null);
    marker = new google.maps.Marker({
        map: map,
        position: location,
        animation: google.maps.Animation.DROP
    });
}

document.getElementById('delivery-form').addEventListener('submit', (e) => {
    e.preventDefault();

    const deliveryDetails = {
        address: document.getElementById('address-input').value,
        contactName: document.getElementById('contact-name').value,
        phone: document.getElementById('phone').value,
        instructions: document.getElementById('instructions').value,
        deliveryTime: document.getElementById('delivery-slot').value,
        location: marker ? {
            lat: marker.getPosition().lat(),
            lng: marker.getPosition().lng()
        } : null
    };

    // Store delivery details
    localStorage.setItem('deliveryDetails', JSON.stringify(deliveryDetails));

    // Proceed to payment
    window.location.href = 'payment.html';
});

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

