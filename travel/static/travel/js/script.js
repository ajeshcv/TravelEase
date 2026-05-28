function toggleMenu() {
    var menu = document.getElementById("nav-menu");
    menu.classList.toggle("show");
}

document.addEventListener("DOMContentLoaded", () => {
    const userBoxes = document.querySelectorAll(".user-box");
    const reviewContents = document.querySelectorAll(".review-content");

    userBoxes.forEach((box) => {
        box.addEventListener("click", () => {
            const userId = box.dataset.userId;

            // Remove active class from all user boxes and hide all reviews
            userBoxes.forEach((userBox) => userBox.classList.remove("active"));
            reviewContents.forEach((content) => content.classList.remove("active"));

            // Set clicked user box and corresponding review as active
            box.classList.add("active");
            const selectedReview = document.getElementById(userId);
            if (selectedReview) {
                selectedReview.classList.add("active");
            }
        });
    });

    // Automatically set the first user and review as active on page load
    if (userBoxes.length > 0) {
        userBoxes[0].classList.add("active");
        reviewContents[0].classList.add("active");
    }
});





document.addEventListener("DOMContentLoaded", function () {
    const counters = document.querySelectorAll("count");
    const speed = 100; // The higher the number, the slower the animation
    let animated = false; // Flag to track if the counters have been animated

    function animateCount(counter) {
        const target = +counter.getAttribute("data-target");
        const increment = target / speed;

        function updateCount() {
            const displayedCount = +counter.innerText;

            if (displayedCount < target) {
                counter.innerText = Math.ceil(displayedCount + increment);
                requestAnimationFrame(updateCount);
            } else {
                counter.innerText = target;
            }
        }

        updateCount();
    }

    // Check if the element is in the viewport
    function isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    // Add scroll event listener
    window.addEventListener("scroll", function () {
        if (!animated) {
            if (Array.from(counters).some(counter => isElementInViewport(counter))) {
                animated = true; // Set the flag to true to prevent re-animation
                counters.forEach(counter => animateCount(counter));
            }
        }
    });
});





function swapImage(clickedThumbnail) {
    // Get the main image element
    const mainImage = document.getElementById('mainImage');
    
    // Get the source of the main image
    const currentMainImageSrc = mainImage.src;
    
    // Get the source of the clicked thumbnail image
    const clickedThumbnailSrc = clickedThumbnail.querySelector('img').src;
    
    // Swap the images
    mainImage.src = clickedThumbnailSrc;
    clickedThumbnail.querySelector('img').src = currentMainImageSrc;
  }
  


