function fetchLiveUpdates() {
    fetch('/tools_home_live')
        .then(response => response.json())
        .then(data => {
            // Update Notifications
            let notificationsDiv = document.getElementById("notifications");
            if (data.notifications.length > 0) {
                let notificationList = "<h2>Notifications</h2><ul>";
                data.notifications.forEach(notification => {
                    notificationList += `<li>New Booking Request from User ${notification.farmer_id}</li>`;
                });
                notificationList += "</ul>";
                notificationsDiv.innerHTML = notificationList;
            } else {
                notificationsDiv.innerHTML = "<h2>Notifications</h2><p>No new notifications.</p>";
            }

            // Update Available Tools
            let availableToolsDiv = document.getElementById("available_tools");
            if (data.available_tools.length > 0) {
                let toolsList = "<h2>Available Tools for Rent</h2><ul>";
                data.available_tools.forEach(tool => {
                    toolsList += `<li>${tool.name} - ₹${tool.hourly_rate}/hour</li>`;
                });
                toolsList += "</ul>";
                availableToolsDiv.innerHTML = toolsList;
            } else {
                availableToolsDiv.innerHTML = "<h2>Available Tools for Rent</h2><p>No tools available.</p>";
            }

            // Update Ongoing Bookings
            let ongoingBookingsDiv = document.getElementById("ongoing_bookings");
            let bookingsHTML = "<h2>Ongoing Bookings</h2>";

            // Farmer's bookings
            bookingsHTML += "<h3>Your Bookings (Farmer)</h3>";
            if (data.farmer_bookings.length > 0) {
                bookingsHTML += "<ul>";
                data.farmer_bookings.forEach(booking => {
                    bookingsHTML += `<li>Tool ${booking.tool_id} - Status: ${booking.status}</li>`;
                });
                bookingsHTML += "</ul>";
            } else {
                bookingsHTML += "<p>No ongoing bookings.</p>";
            }

            // Owner's bookings
            bookingsHTML += "<h3>Your Listed Tools (Owner)</h3>";
            if (data.owner_bookings.length > 0) {
                bookingsHTML += "<ul>";
                data.owner_bookings.forEach(booking => {
                    bookingsHTML += `<li>Tool ${booking.tool_id} - Rented by User ${booking.farmer_id}</li>`;
                });
                bookingsHTML += "</ul>";
            } else {
                bookingsHTML += "<p>No ongoing bookings.</p>";
            }

            ongoingBookingsDiv.innerHTML = bookingsHTML;
        })
        .catch(error => console.error("Error fetching live updates:", error));
}

// Auto-update every 5 seconds
setInterval(fetchLiveUpdates, 5000);