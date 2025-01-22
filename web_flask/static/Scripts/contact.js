document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chatMessages');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendMessage');
    const stars = document.querySelectorAll('.fa-star');
    const feedbackForm = document.getElementById('feedbackForm');

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

    // Star rating system
    stars.forEach(star => {
        star.addEventListener('click', () => {
            const rating = star.getAttribute('data-rating');
            stars.forEach(s => {
                if (s.getAttribute('data-rating') <= rating) {
                    s.classList.add('active');
                } else {
                    s.classList.remove('active');
                }
            });
        });

        star.addEventListener('mouseover', () => {
            const rating = star.getAttribute('data-rating');
            stars.forEach(s => {
                if (s.getAttribute('data-rating') <= rating) {
                    s.classList.add('hover');
                }
            });
        });

        star.addEventListener('mouseout', () => {
            stars.forEach(s => s.classList.remove('hover'));
        });
    });

    // Feedback form submission
    feedbackForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const type = document.getElementById('feedbackType').value;
        const text = document.getElementById('feedbackText').value;
        const rating = document.querySelectorAll('.fa-star.active').length;

        // Here you would typically send this data to your backend
        console.log({ type, text, rating });

        alert('Thank you for your feedback!');
        feedbackForm.reset();
        stars.forEach(s => s.classList.remove('active'));
    });
});
