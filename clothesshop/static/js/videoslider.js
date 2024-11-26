
const btns = document.querySelectorAll(".nav-btn");
const slides = document.querySelectorAll(".video-slide");
const contents = document.querySelectorAll(".content");

let currentSlide = 0;
let slideInterval;

var sliderNav = function (manual) {
    clearInterval(slideInterval);
    btns.forEach((btn) => {
        btn.classList.remove("active");
    });

    slides.forEach((slide) => {
        slide.classList.remove("active");
        slide.pause();
    });

    contents.forEach((content) => {
        content.classList.remove("active");
    });

    btns[manual].classList.add("active");
    slides[manual].classList.add("active");
    contents[manual].classList.add("active");

    slides[manual].currentTime = 0;
    slides[manual].play();

    autoSlide(manual);
};

var autoSlide = function (index) {
    clearTimeout(slideInterval);

    const startTimer = () => {
        const videoDuration = slides[index].duration * 1000;
        slideInterval = setTimeout(() => {
            currentSlide = (index + 1) % slides.length;
            sliderNav(currentSlide);
        }, videoDuration);
    };

    if (slides[index].readyState >= 1) {
        startTimer();
    } else {
        slides[index].addEventListener('loadedmetadata', startTimer);
    }
};


btns.forEach((btn, i) => {
    btn.addEventListener("click", () => {
        currentSlide = i;
        sliderNav(i);
    });
});

sliderNav(currentSlide);