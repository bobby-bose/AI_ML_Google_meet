// Function to handle the button click event
document.getElementById("toggle-camera-btn").addEventListener("click", function() {
    // Get the CSRF token from the cookie
    const csrftoken = getCookie('csrftoken');

    // Send a POST request to the Django backend
    fetch('/toggle-camera/', {
        method: 'POST',  // Specify the request method
        headers: {
            'Content-Type': 'application/json',  // Specify the content type
            'X-CSRFToken': csrftoken  // Include the CSRF token in the headers
        },
    })
    .then(response => {
        if (response.ok) {
            // If request is successful, do something
            console.log('Camera turned on successfully.');
        } else {
            console.error('Failed to turn on camera.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
