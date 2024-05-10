document.addEventListener('DOMContentLoaded', function() {
    // Handle the Sign Up button click
    const signUpButton = document.getElementById('sign-up-btn');
    if (signUpButton) {
        signUpButton.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent the default form submission
            window.location.href = '/register'; // Redirect to the registration page
        });
    }

    // Handle the Log In button click
    const logInButton = document.getElementById('log-in-btn');
    if (logInButton) {
        logInButton.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent the default form submission
            window.location.href = '/login'; // Redirect to the login page
        });
    }
});
