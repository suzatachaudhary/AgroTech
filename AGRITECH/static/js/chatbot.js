// Toggle chatbot window visibility
document.getElementById("chatbot-button").onclick = function () {
    const chatbotWindow = document.getElementById("chatbot-window");
    if (chatbotWindow.style.display === "none") {
        chatbotWindow.style.display = "block";
    } else {
        chatbotWindow.style.display = "none";
    }
};

// Basic chatbot response function
function sendMessageToChatbot(message) {
    const chatbotMessages = document.getElementById("chatbot-messages");
    chatbotMessages.innerHTML += `<div><strong>You:</strong> ${message}</div>`;

    // AI-like responses based on keywords (simple logic)
    let response = '';

    if (message.toLowerCase().includes("hi")) {
        response = "Hello! How can I assist you today?";
    }
    else if (message.toLowerCase().includes("hello")) {
         response = "Hello! How can I assist you today?";}
    else if (message.toLowerCase().includes("services")) {
        response = "We offer services like labour booking, agricultural tools booking,crop recommendations,farming related suggetions,farm related products buy and sell and knowladge about your crop's health. Would you like more information on any of these?";
    } else if (message.toLowerCase().includes("price")) {
        response = "Please contact us directly for pricing details based on the services you need.";
    } else if (message.toLowerCase().includes("labour registration")) {
        response = "To register as a labour, click on the 'Register' button on the homepage,And then select register as labour.";
    } else if (message.toLowerCase().includes("customer registration")) {
        response = "To register as a farmer, click on the 'Register' button on the homepage,And then select register as farmer.";
    } else if (message.toLowerCase().includes("contact")) {
        response = "You can reach us at agritechsolutions@gmail.com or call +123 456 7890. " ;
    } else if (message.toLowerCase().includes("login")) {
        response = '<a href="/login">Login</a>';
    } else if (message.toLowerCase().includes("register")) {
        response = '<a href="register.html">Register</a>';

    } else if (message.toLowerCase().includes("about")) {
        response = '<a href="about_us.html">AboutUs</a>';
    }else if (message.toLowerCase().includes("review")) {
        response = '<a href="reviews.html">Review</a>';
    } 
    else if (message.toLowerCase().includes("register")) {
        response = '<a href="customer.html">Register</a>';
    }else if(message.toLowerCase().includes("home")){
        response = '<a href="index.html">Home</a>';
        
    }
    
    else {
        response = "I'm sorry, I didn't understand that. Can you please rephrase?";
    }

    // Display the chatbot's response
    setTimeout(() => {
        chatbotMessages.innerHTML += `<div><strong>Chatbot:</strong> ${response}</div>`;
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight; // Scroll to the bottom
    }, 1000);
}

// Handle send button click
document.getElementById("send-message").onclick = function () {
    const userInput = document.getElementById("chatbot-input").value;
    if (userInput.trim()) {
        sendMessageToChatbot(userInput);
        document.getElementById("chatbot-input").value = '';
    }
};

// Handle Enter key press to send message
document.getElementById("chatbot-input").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        const userInput = document.getElementById("chatbot-input").value;
        if (userInput.trim()) {
            sendMessageToChatbot(userInput);
            document.getElementById("chatbot-input").value = '';
        }
    }
});
