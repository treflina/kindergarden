
$(document).ready(function () {
    const browserFontSize = getComputedStyle(
        document.querySelector("body")
    ).fontSize;
    const largeScreen =  62 * parseInt(browserFontSize)
    const smallScreen =  32.5 * parseInt(browserFontSize)

    console.log(largeScreen)
    const slider = $(".events-slider");

    slider.slick({
        infinite: false,
        arrows: true,
        slidesToShow: 3,
        slidesToScroll: 3,
        speed: 0,
        responsive: [
            {
                breakpoint: largeScreen,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                },
            },
            {
                breakpoint: smallScreen,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                },
            },
        ],
    });

    function getCurrentSlide(slideItems) {
        if (!slideItems.length) {
            return null;
        }

        let slideIndex = null;

        for (let i = 0; i < slideItems.length; i++) {
            let currentItem = slideItems[i];
            if (
                currentItem
                    .querySelector(".event")
                    .classList.contains("active")
            ) {
                slideIndex = currentItem.getAttribute("data-slick-index");
                if (slideIndex > 0) {
                    return slideIndex;
                }
            }
            slideIndex = currentItem.getAttribute("data-slick-index");
        }

        return slideIndex;
    }

    const slideItems = document.getElementsByClassName("slick-slide");
    const currentSlideIndex = getCurrentSlide(slideItems);
    if (null !== currentSlideIndex) {
          slider.slick("slickGoTo", currentSlideIndex);
        }

    slider.slick('slickSetOption', 'speed', 1000);
});