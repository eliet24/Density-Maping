document.addEventListener('DOMContentLoaded', function () {
    var map = L.map('map').setView([51.505, -0.09], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Fetch grid data from the server
    fetch('/grid')
        .then(response => response.json())
        .then(data => {
            // Example: Adding markers based on grid data
            data.forEach(item => {
                L.marker([item.y, item.x]).addTo(map)
                    .bindPopup(`Value: ${item.value}`);
            });
        });
});
