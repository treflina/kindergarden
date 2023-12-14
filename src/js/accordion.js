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
            accordionSection.style.maxHeight = `calc(${accordionSection.scrollHeight}px + ${accordionSection.parentElement.scrollHeight}px)`;
        } else {
            button.setAttribute("aria-expanded", false);
            accordionSection.setAttribute("aria-hidden", true);
            accordionSection.style.maxHeight = 0;
        }
    });
});

// function getCookie(name) {
//     var nameEQ = name + "=";
//     var ca = document.cookie.split(";");
//     for (var i = 0; i < ca.length; i++) {
//         var c = ca[i];
//         while (c.charAt(0) == " ") c = c.substring(1, c.length);
//         if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
//     }
//     return null;
// }

const openFirstNews = () => {
    const firstNews = document.getElementById("accordion-section-1");
    const firstNewsBtn = document.getElementById("accordion-open-1");
    firstNews.classList.add("active");
    firstNewsBtn.classList.add("expanded");
    firstNews.setAttribute("aria-hidden", false);
    firstNewsBtn.setAttribute("aria-expanded", true);
    firstNews.style.maxHeight = `calc(${firstNews.scrollHeight}px + ${firstNews.parentElement.scrollHeight}px)`;
};

// if (!(window.innerWidth <= 800 && window.innerHeight <= 1000)
    // && !(getCookie('firstNews'))
// ) {
    // document.cookie =
    //     "firstNews=seen; expires=session; path=/;";
//     openFirstNews();
// }
// openFirstNews();