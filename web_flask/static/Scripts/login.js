document.addEventListener('DOMContentLoaded', () => {
    // Get the current mode from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const mode = urlParams.get('mode') || 'login';

    // Get form elements
    const formTitle = document.querySelector('.form-box h2');
    const submitBtn = document.querySelector('.submit-btn');
    const switchModeText = document.querySelector('.form-footer span');
    const switchModeLink = document.querySelector('.form-footer a');
    const passwordConfirmGroup = document.querySelector('.confirm-password-group');

    // Update form based on mode
    function updateFormMode(currentMode) {
        if (currentMode === 'login') {
            formTitle.textContent = 'Login';
            submitBtn.textContent = 'Login';
            switchModeText.textContent = "Don't have an account?";
            switchModeLink.textContent = 'Sign up';
            switchModeLink.href = '?mode=signup';
            if (passwordConfirmGroup) {
                passwordConfirmGroup.style.display = 'none';
            }
        } else {
            formTitle.textContent = 'Sign Up';
            submitBtn.textContent = 'Sign Up';
            switchModeText.textContent = 'Already have an account?';
            switchModeLink.textContent = 'Login';
            switchModeLink.href = '?mode=login';
            if (passwordConfirmGroup) {
                passwordConfirmGroup.style.display = 'block';
            }
        }
    }

    // Initial form setup
    updateFormMode(mode);

    // Form validation and submission
    const loginForm = document.getElementById('loginForm');
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        if (mode === 'signup') {
            const confirmPassword = document.getElementById('confirmPassword').value;
            if (password !== confirmPassword) {
                alert("Passwords don't match!");
                return;
            }
        }

        try {
            // Add your authentication logic here
            const response = await fetch('/api/auth', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    mode,
                    email,
                    password
                })
            });

            if (response.ok) {
                window.location.href = '/'; // Redirect to home page on success
            } else {
                const error = await response.json();
                alert(error.message);
            }
        } catch (error) {
            console.error('Authentication error:', error);
            alert('An error occurred during authentication');
        }
    });
});
