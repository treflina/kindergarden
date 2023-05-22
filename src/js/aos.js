//animations

if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    AOS.init({
        startEvent: "DOMContentLoaded",
        offset: 120,
        easing: "ease-out",
        once: false,
    });
} else {
    AOS.init({
        disable: true,
    });
}
