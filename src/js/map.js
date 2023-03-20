function initMap() {
    const turawa = { lat: 50.74109105338817, lng: 18.07653108465577 };
    const turawaCenter = { lat: 50.739435904958725, lng: 18.075503040289156 };
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: turawaCenter,
    });
    const marker = new google.maps.Marker({
        position: turawa,
        map: map,
    });
}

window.initMap = initMap;
