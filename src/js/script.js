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

    const dropdownBtn = document.querySelectorAll(".nav-btn");
    const dropdown = document.querySelectorAll(".nav__dropdown");
    const hamburgerBtn = document.querySelector(".hamburger");
    const navTxt = document.querySelector(".hamburger-text");
    const navMenu = document.querySelector(".nav-links");
    const links = document.querySelectorAll("nav__dropdown-link");
    const allTargetNavItems = document.querySelectorAll(".menu-close");

    function setAriaExpandedFalse() {
        dropdownBtn.forEach((btn) =>
            btn.setAttribute("aria-expanded", "false")
        );
    }

    function closeDropdownMenu() {
        dropdown.forEach((drop) => {
            drop.classList.remove("show");
            drop.addEventListener("click", (e) => e.stopPropagation());
        });
    }

    function handleHamburger() {
        if (hamburgerBtn.classList.contains("is-active")) {
            navTxt.textContent = "Zamknij";
            hamburgerBtn.setAttribute("aria-expanded", "true");
        } else {
            navTxt.textContent = "Menu";
            hamburgerBtn.setAttribute("aria-expanded", "false");
        }
    }

    function toggleHamburger() {
        navMenu.classList.toggle("nav-links--active");
        hamburgerBtn.classList.toggle("is-active");
        handleHamburger();
    }

    const closeNav = () => {
        hamburgerBtn.classList.remove("is-active");
        navMenu.classList.remove("nav-links--active");
        handleHamburger();
    };

    dropdownBtn.forEach((btn) => {
        btn.addEventListener("click", function (e) {
            const dropdownIndex = e.currentTarget.dataset.dropdown;
            const dropdownElement = document.getElementById(dropdownIndex);

            dropdownElement.classList.toggle("show");
            dropdown.forEach((drop) => {
                if (drop.id !== btn.dataset["dropdown"]) {
                    drop.classList.remove("show");
                }
            });
            e.stopPropagation();
            btn.setAttribute(
                "aria-expanded",
                btn.getAttribute("aria-expanded") === "false" ? "true" : "false"
            );
        });
    });

    // close dropdown menu when the dropdown links are clicked
    links.forEach((link) =>
        link.addEventListener("click", () => {
            closeDropdownMenu();
            setAriaExpandedFalse();
            toggleHamburger();
        })
    );

    // close dropdown menu when you click on the document body
    document.documentElement.addEventListener("click", () => {
        closeDropdownMenu();
        setAriaExpandedFalse();
    });

    // close dropdown when the escape key is pressed
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
            closeDropdownMenu();
            setAriaExpandedFalse();
        }
    });

    // toggle hamburger menu
    hamburgerBtn.addEventListener("click", toggleHamburger);

    //hide navigation when link clicked 
    allTargetNavItems.forEach((item) => {
        item.addEventListener("click", closeNav);
    });

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
