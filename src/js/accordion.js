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

const detectMob = () => {
     return window.innerWidth <= 800 && window.innerHeight <= 1000;
 }

const openFirstNews = () => {
    const firstNews = document.getElementById("accordion-section-1");
    const firstNewsBtn = document.getElementById("accordion-open-1");
    firstNews.classList.add("active");
    firstNews.setAttribute("aria-hidden", false);
    firstNewsBtn.setAttribute("aria-expanded", false);
};

if (!detectMob()) {
    openFirstNews();
}


const closeAccordionItem = () => {
    const allActiveItems = document.querySelectorAll(".news__info");
    allActiveItems.forEach((item) => item.classList.remove("active"));
};

const clickOutsideAccordion = (e) => {
    if (e.target.classList.contains("body")) {
        const i = e.target;
        closeAccordionItem();
        return;
    } else if (
        e.target.classList.contains("news__btn") ||
        e.target.classList.contains("news__info") ||
        e.target.classList.contains("news__info-text") ||
        e.target.classList.contains("colheaders") ||
        e.target.parentElement.parentElement.classList.contains("colheaders") ||
        e.target.parentElement.parentElement.classList.contains("tb-block") ||
        e.target.parentElement.parentElement.classList.contains(
            "thead-block"
        ) ||
        e.target.parentElement.parentElement.classList.contains("tbody-block")
    ) {
        return;
    } else {
        const i = e.target;
        closeAccordionItem();
    }
};

window.addEventListener("click", clickOutsideAccordion);
