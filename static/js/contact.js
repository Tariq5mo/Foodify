document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chatMessages');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendMessage');
    const stars = document.querySelectorAll('.rating i');
    const feedbackForm = document.getElementById('feedbackForm');
    const submitButton = feedbackForm.querySelector('button[type="submit"]');
    const ratingText = document.querySelector('.rating-text');
    let selectedRating = 0;

    // Add welcome message
    addMessage("Welcome to Foodify! How can we help you today?", 'received');

    // Send message function
    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            addMessage(message, 'sent');
            messageInput.value = '';

            // Simulate auto-response
            setTimeout(() => {
                const responses = [
                    "Thank you for your message. Our team will get back to you shortly.",
                    "We've received your message and will respond as soon as possible.",
                    "Thanks for reaching out! We'll handle your request promptly."
                ];
                const randomResponse = responses[Math.floor(Math.random() * responses.length)];
                addMessage(randomResponse, 'received');
            }, 1000);
        }
    }

    // Add message to chat
    function addMessage(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Rating text options
    const ratingTexts = {
        1: 'Poor',
        2: 'Fair',
        3: 'Good',
        4: 'Very Good',
        5: 'Excellent'
    };

    // Handle star rating
    stars.forEach(star => {
        star.addEventListener('mouseenter', () => {
            const rating = parseInt(star.dataset.rating);
            highlightStars(rating);
            ratingText.textContent = ratingTexts[rating];
        });

        star.addEventListener('mouseleave', () => {
            highlightStars(selectedRating);
            ratingText.textContent = selectedRating ? ratingTexts[selectedRating] : 'Select your rating';
        });

        star.addEventListener('click', () => {
            selectedRating = parseInt(star.dataset.rating);
            highlightStars(selectedRating);
            ratingText.textContent = ratingTexts[selectedRating];
            submitButton.disabled = false;
        });
    });

    function highlightStars(rating) {
        stars.forEach(s => {
            const starRating = parseInt(s.dataset.rating);
            s.classList.toggle('active', starRating <= rating);
        });
    }

    // Handle form submission
    feedbackForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const restaurantId = document.getElementById('feedbackType').value;
        const feedback = document.getElementById('feedbackText').value;

        try {
            const response = await fetch('/api/v1/submit_review', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    restaurant_id: restaurantId,
                    rating: selectedRating,
                    feedback
                })
            });

            const data = await response.json();

            if (data.success) {
                showSuccessMessage();
                resetForm();
            } else {
                alert(data.error || 'Error submitting review');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error submitting review');
        }
    });

    function showSuccessMessage() {
        const successMessage = document.getElementById('successMessage');
        successMessage.style.display = 'block';

        setTimeout(() => {
            successMessage.style.opacity = '0';
            setTimeout(() => {
                successMessage.style.display = 'none';
                successMessage.style.opacity = '1';
            }, 500);
        }, 3000);
    }

    function resetForm() {
        feedbackForm.reset();
        selectedRating = 0;
        highlightStars(0);
        ratingText.textContent = 'Select your rating';
        submitButton.disabled = true;
    }

    // Add cart count update functionality
    function updateCartCount() {
        const cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
        const cartCount = document.getElementById('cart-count');
        const totalQuantity = cartItems.reduce((total, item) => total + item.quantity, 0);

        if (totalQuantity > 0) {
            cartCount.textContent = totalQuantity;
            cartCount.classList.remove('cart-count-hidden');
            cartCount.classList.add('cart-count-active');
        } else {
            cartCount.classList.remove('cart-count-active');
            cartCount.classList.add('cart-count-hidden');
        }
    }

    // Initialize cart count
    updateCartCount();
});
