window.onload = function () {
    // navbar

    const navDropdownBtn = document.querySelector(".nav__item-link");
    function myFunction() {
        document.querySelector(".nav__dropdown").classList.toggle("show");
    }

    navDropdownBtn.addEventListener("click", myFunction);

    const navMobile = document.querySelector(".nav-list");
    const navBtn = document.querySelector(".hamburger");
    const logoBtn = document.querySelector(".nav__logo");
    const allNavItems = document.querySelectorAll(".nav-link");

    window.onclick = function (event) {
        const targ = event.target;
        const drp = document.getElementsByClassName("nav__dropdown");
        for (let i = 0; i < drp.length; i++) {
            if (drp[i].previousElementSibling === targ) {
                drp[i].classList.toggle("show");
                drp[i].previousElementSibling.classList.toggle("active");
            } else {
                drp[i].classList.remove("show");
                drp[i].previousElementSibling.classList.remove("active");
            }
        }
    };

    const closeNav = () => {
        navBtn.classList.remove("is-active");
        navMobile.classList.remove("nav-list--active");
    };

    allNavItems.forEach((item) => {
        item.addEventListener("click", closeNav);
    });

    logoBtn.addEventListener("click", closeNav);

    const handleNav = () => {
        navBtn.classList.toggle("is-active");
        navMobile.classList.toggle("nav-list--active");
    };

    navBtn.addEventListener("click", handleNav);

    //cookies
    const cookieBox = document.querySelector(".cookie-box");
    const cookieBtn = document.querySelector(".cookie-btn");

    const showCookie = () => {
        const cookieSeen = localStorage.getItem("cookie");

        if (cookieSeen) {
            cookieBox.classList.add("hide");
        }
    };

    const handleCookieBox = () => {
        localStorage.setItem("cookie", "true");
        cookieBox.classList.add("hide");
        console.log("clicked");
    };

    cookieBtn.addEventListener("click", handleCookieBox);
    showCookie();

    // accordion

    const accordion = document.querySelector(".news__accordion");
    const accordionBtns = document.querySelectorAll(".news__btn");
    const accordionSections = document.querySelectorAll(".news__info");

    const accordionAddId = () => {
        for (let i = 1; i <= accordionBtns.length; i++) {
            const accordionBtn = accordionBtns[i - 1];
            accordionBtn.setAttribute("id", "accordion-open-" + i);
            const accordionInfo = accordionSections[i - 1];
            accordionInfo.setAttribute("id", "accordion-section-" + i);
        }
    };
    accordionAddId();

    accordionSections.forEach((section) => {
        section.setAttribute("aria-hidden", true);
        section.classList.remove("active");
    });

    accordionBtns.forEach((button) => {
        button.setAttribute("aria-expanded", false);
        const expanded = button.getAttribute("aria-expanded");
        const number = button.getAttribute("id").split("-").pop();
        const accordionSection = document.getElementById(
            `accordion-section-${number}`
        );

        button.addEventListener("click", () => {
            button.classList.toggle("expanded");
            accordionSection.classList.toggle("active");

            if (button.classList.contains("expanded")) {
                button.setAttribute("aria-expanded", true);
                accordionSection.setAttribute("aria-hidden", false);
            } else {
                button.setAttribute("aria-expanded", false);
                accordionSection.setAttribute("aria-hidden", true);
            }
        });
    });

    const closeAccordionItem = () => {
        const allActiveItems = document.querySelectorAll(".news__info");
        allActiveItems.forEach((item) => item.classList.remove("active"));
    };

    const clickOutsideAccordion = (e) => {
        if (
            e.target.classList.contains("news__btn") ||
            e.target.classList.contains("news__info") ||
            e.target.classList.contains("news__info-text")
        )
            return;

        closeAccordionItem();
    };

    window.addEventListener("click", clickOutsideAccordion);

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

    //photogallery
    //     const gallery = document.querySelectorAll(".gallery-image"),
    //         previewBox = document.querySelector(".preview-box"),
    //         previewImg = previewBox.querySelector(".gallery-img"),
    //         previewLink = previewBox.querySelector("a"),
    //         closeIcon = previewBox.querySelector(".icon"),
    //         currentImg = previewBox.querySelector(".current-img"),
    //         totalImg = previewBox.querySelector(".total-img"),
    //         shadow = document.querySelector(".shadow");

    //     for (let i = 0; i < gallery.length; i++) {
    //         totalImg.textContent = gallery.length; //passing total img length to totalImg variable
    //         let newIndex = i; //passing i value to newIndex variable
    //         let clickedImgIndex; //creating new variable

    //         gallery[i].onclick = () => {
    //             clickedImgIndex = i; //passing cliked image index to created variable (clickedImgIndex)
    //             function preview() {
    //                 currentImg.textContent = newIndex + 1; //passing current img index to currentImg varible with adding +1
    //                 let imageURL = gallery[newIndex].querySelector("img").src; //getting user clicked img url
    //                 let imageFileURL = gallery[newIndex].querySelector("a").href; //getting user clicked img url
    //                 console.log(imageFileURL);
    //                 previewImg.src = imageURL; //passing user clicked img url in previewImg src
    //                 previewLink.href = imageFileURL;
    //             }
    //             preview(); //calling above function

    //             const prevBtn = document.querySelector(".prev");
    //             const nextBtn = document.querySelector(".next");
    //             if (newIndex == 0) {
    //                 //if index value is equal to 0 then hide prevBtn
    //                 prevBtn.style.display = "none";
    //             }
    //             if (newIndex >= gallery.length - 1) {
    //                 //if index value is greater and equal to gallery length by -1 then hide nextBtn
    //                 nextBtn.style.display = "none";
    //             }
    //             prevBtn.onclick = () => {
    //                 newIndex--; //decrement index
    //                 if (newIndex == 0) {
    //                     preview();
    //                     prevBtn.style.display = "none";
    //                 } else {
    //                     preview();
    //                     nextBtn.style.display = "block";
    //                 }
    //             };
    //             nextBtn.onclick = () => {
    //                 newIndex++; //increment index
    //                 if (newIndex >= gallery.length - 1) {
    //                     preview();
    //                     nextBtn.style.display = "none";
    //                 } else {
    //                     preview();
    //                     prevBtn.style.display = "block";
    //                 }
    //             };
    //             document.querySelector("body").style.overflow = "hidden";
    //             previewBox.classList.add("show");
    //             shadow.style.display = "block";
    //             closeIcon.onclick = () => {
    //                 newIndex = clickedImgIndex; //assigning user first clicked img index to newIndex
    //                 prevBtn.style.display = "block";
    //                 nextBtn.style.display = "block";
    //                 previewBox.classList.remove("show");
    //                 shadow.style.display = "none";
    //                 document.querySelector("body").style.overflow = "scroll";
    //             };
    //         }
    //     };

// Close the dropdown if the user clicks outside of it
// window.onclick = function (e) {
//     if (!e.target.matches(".nav__item-link")) {
//         var myDropdown = document.querySelector(".nav-item");
//         if (myDropdown.classList.contains("show")) {
//             myDropdown.classList.remove("show");
//         }
//     }
// };

// function openAccordionItems() {
//     if (this.nextElementSibling.classList.contains("active")) {
//         this.nextElementSibling.classList.remove("active");
//     } else {
//         closeAccordionItem();
//         this.nextElementSibling.classList.toggle("active");
//     }
// }
// accordionBtns.forEach((btn) =>
//     btn.addEventListener("click", openAccordionItems)
// );
