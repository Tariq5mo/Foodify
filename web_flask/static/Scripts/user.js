document.addEventListener('DOMContentLoaded', () => {
    const profileForm = document.getElementById('profileForm');
    const photoUpload = document.getElementById('photoUpload');
    const userPhoto = document.getElementById('userPhoto');

    // Handle photo upload
    photoUpload.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                userPhoto.src = e.target.result;
                localStorage.setItem('userPhoto', e.target.result);
            };
            reader.readAsDataURL(file);
        }
    });

    // Handle form submission
    profileForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const oldPassword = document.getElementById('oldPassword').value;
        const newPassword = document.getElementById('newPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;

        // Validate passwords match
        if (newPassword !== confirmPassword) {
            alert("New passwords don't match!");
            return;
        }

        // TODO: Add API call to update user profile
        alert('Profile updated successfully!');
    });

    // Load saved photo if exists
    const savedPhoto = localStorage.getItem('userPhoto');
    if (savedPhoto) {
        userPhoto.src = savedPhoto;
    }
});
