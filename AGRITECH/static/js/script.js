const backgrounds = [
    "url('/static/images/bg.jpg')", 
    "url('/static/images/bg1.jpg')", 
    "url('/static/images/bg2.jpg')",
    "url('/static/images/bg3.jpg')",
    "url('/static/images/bg4.jpg')", 
    "url('/static/images/bg5.jpg')",
    "url('/static/images/bg6.jpg')",
    "url('/static/images/bg7.jpg')"
];

let currentBackground = 0;

// Function to change the background
function changeBackground() {
    let body = document.body;
    let backgroundWrapper = document.querySelector('.background-wrapper');
    
    // Fade out the background wrapper (5 seconds)
    backgroundWrapper.style.transition = 'opacity 5s ease-in-out';
    backgroundWrapper.style.opacity = 0;

    // After the fade-out transition, change the background
    setTimeout(() => {
        // Update background image
        backgroundWrapper.style.backgroundImage = backgrounds[currentBackground];
        
        // Fade in the background wrapper (5 seconds)
        backgroundWrapper.style.opacity = 1;
    }, 5000); // Match the opacity transition duration (5 seconds)

    // Update the background index
    currentBackground = (currentBackground + 1) % backgrounds.length;
}

// Initial background change
changeBackground();

// Change background every 10 seconds (5s fade out + 5s fade in)
setInterval(changeBackground, 10000);


