function initMap() {
    const turawa = { lat: 50.74109105338817, lng: 18.07653108465577 };
    const center = { lat: 50.740228564644724, lng: 18.075126082618077 };
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 16,
        center: center,
    });
    const marker = new google.maps.Marker({
        position: turawa,
        map: map,
    });
}

window.initMap = initMap;
