window.onload = function () {
    //cookies
    const cookieBox = document.querySelector(".cookie-box");
    const cookieBtn = document.querySelector(".cookie-btn");

    const showCookie = () => {
        const cookieSeen = localStorage.getItem("cookie");

        if (!cookieSeen) {
            cookieBox.classList.remove("hide");
        }
    };

    const handleCookieBox = () => {
        localStorage.setItem("cookie", "true");
        cookieBox.classList.add("hide");
    };

    cookieBtn.addEventListener("click", handleCookieBox);
    showCookie();

    // navbar

    const navMobile = document.querySelector(".nav-links");
    const navBtn = document.querySelector(".hamburger");
    const navTxt = document.querySelector(".hamburger-text")
    const logoBtn = document.querySelector(".nav__logo");
    const allNavItems = document.querySelectorAll(".menu-close");

    const showDropdown = function (event) {
        const targ = event.target;
        const drp = document.getElementsByClassName("nav__dropdown");
        for (let i = 0; i < drp.length; i++) {
            if (
                drp[i].previousElementSibling === targ ||
                drp[i].previousElementSibling.children[0] === targ
            ) {
                drp[i].classList.toggle("show");
                drp[i].previousElementSibling.classList.toggle("active");
            } else {
                drp[i].classList.remove("show");
                drp[i].previousElementSibling.classList.remove("active");
            }
        }
    };

    window.addEventListener("click", showDropdown)

    const closeNav = () => {
        navBtn.classList.remove("is-active");
        navMobile.classList.remove("nav-links--active");
    };

    allNavItems.forEach((item) => {
        item.addEventListener("click", closeNav);
    });

    logoBtn.addEventListener("click", closeNav);

    const handleNav = () => {
        navBtn.classList.toggle("is-active");
        navMobile.classList.toggle("nav-links--active");
        if (navBtn.classList.contains("is-active")){
            navTxt.textContent = "Zamknij"
        } else {
            navTxt.textContent = "Menu";
        }
    };

    navBtn.addEventListener("click", handleNav);

    //gallery
    const galleryItems = document.querySelectorAll(".gallery__item");
    const galleryAddClass = () => {
        for (let i = 1; i <= galleryItems.length; i++) {
            const item = galleryItems[i - 1];
            item.classList.add("gallery__item--" + i);
        }
    };

    galleryAddClass();

};
