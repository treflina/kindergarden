document.addEventListener("DOMContentLoaded", function (event) {
    const chronicleSection = document.getElementById("chronicle");
    const btnLinks = document.getElementsByClassName("pagination-link");
    let page = 1;

    const removeAndSetActiveClass = (p) => {
        [...btnLinks].forEach((btn) => {
            btn.classList.remove("active");
            if (btn.classList.contains(`pagination-link-${p}`)) {
                btn.classList.add("active");
            }
        });
    };

    const getPosts = (page) => {
        fetch(
            "/" +
                "?" +
                new URLSearchParams({
                    page: page,
                }),
            {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            }
        )
            .then(function (response) {
                return response.text();
            })
            .then(function (data) {
                while (chronicleSection.firstChild) {
                    chronicleSection.removeChild(chronicleSection.firstChild);
                }
                chronicleSection.insertAdjacentHTML("afterbegin", data);
            })
            .catch(function (err) {
                console.warn("Something went wrong.", err);
            });
    };

    getPosts(page);

    [...btnLinks].forEach((btn) => {
        btn.addEventListener("click", function getPostsAfterClick(e) {
            e.preventDefault();

            let targetUrl = `${btn.href}`.split("=")[1];
            if (targetUrl) {
                page = parseInt(targetUrl);
            } else {
                page = 1;
            }

            getPosts(page);
            // <!-- let height = chronicleSection.offsetHeight;
            // chronicleSection.style.minHeight = `${height}px`; -->

            removeAndSetActiveClass(page);
            document
                .getElementById("chronicle")
                .scrollIntoView({ behavior: "smooth" });
        });
    });
});
