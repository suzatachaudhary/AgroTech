const carousel = document.querySelector('.carousel');
const items = document.querySelectorAll('.carousel-item');
let currentIndex = 0;
let startX, moveX, isDragging = false;

// Auto Slide Function
const autoSlide = () => {
    currentIndex++;
    if (currentIndex >= items.length) {
        currentIndex = 0;
    }
    updateCarousel();
};

let slideInterval = setInterval(autoSlide, 3000);

const updateCarousel = () => {
    carousel.style.transform = `translateX(-${currentIndex * 100}%)`;
};

// Touch Events for Dragging
carousel.addEventListener('touchstart', (e) => {
    startX = e.touches[0].clientX;
    isDragging = true;
    clearInterval(slideInterval);
});

carousel.addEventListener('touchmove', (e) => {
    if (isDragging) {
        moveX = e.touches[0].clientX - startX;
        carousel.style.transform = `translateX(calc(-${currentIndex * 100}% + ${moveX}px))`;
    }
});

carousel.addEventListener('touchend', () => {
    isDragging = false;
    if (moveX > 50) {
        currentIndex--;
        if (currentIndex < 0) {
            currentIndex = items.length - 1;
        }
    } else if (moveX < -50) {
        currentIndex++;
        if (currentIndex >= items.length) {
            currentIndex = 0;
        }
    }
    updateCarousel();
    slideInterval = setInterval(autoSlide, 3000);
});


