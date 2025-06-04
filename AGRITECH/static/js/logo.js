const logo = document.querySelector('.farmera-logo');
const overlay = document.querySelector('.overlay');
const textContainer = document.querySelector('.farmera-text');
const impactSound = new Audio('static/sounds/impact.mp3');
const fullscreenImage = document.querySelector('.fullscreen-image');
const letters = "AGRITECH".split("");

logo.addEventListener('click', () => {
    overlay.style.opacity = "1";
    overlay.style.visibility = "visible";
    textContainer.innerHTML = "";
    textContainer.style.opacity = "1";

    letters.forEach((letter, index) => {
        let span = document.createElement('span');
        span.textContent = letter;
        span.style.animationDelay = `${index * 0.5}s`;
        textContainer.appendChild(span);
    });

    setTimeout(() => {
        fullscreenImage.style.opacity = "1";
        fullscreenImage.style.visibility = "visible";
        fullscreenImage.style.transform = "translate(-50%, -50%) scale(40)";
        impactSound.play();
    }, letters.length * 500 + 1000);

    setTimeout(() => {
        fullscreenImage.style.opacity = "0";
        fullscreenImage.style.visibility = "hidden";
        overlay.style.opacity = "0";
        setTimeout(() => {
            overlay.style.visibility = "hidden";
            textContainer.style.opacity = "0";
        }, 1000);
    }, letters.length * 500 + 3000);
});

window.onload = function() {
    var video = document.getElementById('transitionVideo');
   // Path to your sound file
    audio.play();

    video.onended = function() {
        video.style.display = 'none'; // Hide the video after it ends
        dashboardContent.style.display = 'block'; // Show the dashboard content
        dashboardContent.classList.add('blink'); // Add blinking effect
    };
};

function createWaterDrop() {
    let drop = document.createElement("div");
    drop.classList.add("water-drop");

    // Random position along the pipe
    let positionX = Math.random() * window.innerWidth;
    drop.style.left = positionX + "px";

    document.querySelector(".water-drop-container").appendChild(drop);

    // Remove drop and create ripple effect after it falls
    setTimeout(() => {
        drop.remove();
        createRipple(positionX);
    }, 2000);
}

// Function to create multiple layered ripples at the landing point
function createRipple(x) {
    let rippleCount = Math.floor(Math.random() * 2) + 2; // 2 to 3 ripples

    for (let i = 0; i < rippleCount; i++) {
        let ripple = document.createElement("div");
        ripple.classList.add("ripple");

        // Slight randomness in size and opacity
        let randomSize = Math.random() * 10 + 20; // 20px to 30px
        ripple.style.width = randomSize + "px";
        ripple.style.height = randomSize + "px";
        ripple.style.opacity = Math.random() * 0.5 + 0.5; // 0.5 to 1 opacity

        ripple.style.left = x + "px";
        ripple.style.top = "700px"; // Adjust based on ground level

        document.querySelector(".water-drop-container").appendChild(ripple);

        // Remove ripple after animation
        setTimeout(() => {
            ripple.remove();
        }, 1500);
    }
}

// Generate new drops every 400ms
setInterval(createWaterDrop, 400);

