document.addEventListener('DOMContentLoaded', () => {
    const ordersContainer = document.querySelector('.orders-container');
    const ordersLeft = document.getElementById('orders-left'); // Ensure it uses the correct ID

    // Event delegation for increase/decrease buttons
    ordersContainer.addEventListener('click', (event) => {
        const isIncreaseButton = event.target.classList.contains('increase');
        const isDecreaseButton = event.target.classList.contains('decrease');

        if (isIncreaseButton || isDecreaseButton) {
            const mealElement = event.target.closest('.meal');
            const quantityElement = mealElement.querySelector('.quantity-value');
            let currentQuantity = parseInt(quantityElement.dataset.quantity, 10);  // price here

            if (isIncreaseButton) {
                currentQuantity++;
            } else if (isDecreaseButton && currentQuantity > 0) {
                currentQuantity--;
            }

            if (currentQuantity === 0) {
                mealElement.remove();
            } else {
                quantityElement.dataset.quantity = currentQuantity;
                quantityElement.textContent = currentQuantity;
            }

            updateSubtotalAndTotal();
            checkScrollbar(); // Update scroll visibility when content changes
        }
    });

    // Function to calculate and update the subtotal and total prices
    function updateSubtotalAndTotal() {
        let subtotal = 0;
        const meals = document.querySelectorAll('.meal');

        meals.forEach(meal => {
            const price = parseFloat(meal.querySelector('h2').textContent.replace('$', ''));
            const quantity = parseInt(meal.querySelector('.quantity-value').dataset.quantity, 10);
            subtotal += price * quantity;
        });

        // Update subtotal
        document.getElementById('subtotal').textContent = `$${subtotal.toFixed(2)}`;

        // Check if subtotal is zero, if so set total to zero
        let total = subtotal + 5.00; // Add delivery fee
        if (subtotal === 0) {
            total = 0;  // Set total to zero when subtotal is zero
        }
        document.getElementById('total').textContent = `$${total.toFixed(2)}`;
    }

    // Function to handle the scroll effect when "View More" is clicked
    const viewMoreBtn = document.getElementById('view-more-btn');
    viewMoreBtn.addEventListener('click', () => {
        ordersLeft.scrollTo({
            top: ordersLeft.scrollHeight,
            behavior: 'smooth'
        });
    });

    // Function to handle the scroll and view more functionality with smooth scroll
    document.getElementById("view-more-btn").addEventListener("click", function () {
        const mealsContainer = document.getElementById("orders-left");
        mealsContainer.scrollTo({
            top: mealsContainer.scrollTop + 400,
            behavior: "smooth"
        });
    });

    // Function to check and hide the scrollbar when appropriate
    function checkScrollbar() {
        const ordersLeft = document.getElementById('orders-left');
        const meals = document.querySelectorAll('.meal');
        if (meals.length <= 2) {
            ordersLeft.style.overflowY = 'hidden'; // Hide scroll if there are 2 or fewer meals
        } else {
            ordersLeft.style.overflowY = 'scroll'; // Show scroll if there are more than 2 meals
        }
    }

    // Call checkScrollbar on page load to adjust scrollbar visibility
    checkScrollbar();

    // Offer code logic to set the total to zero when the correct offer code is entered
    const offerCodeInput = document.getElementById('offer-code-input');
    const offerCodeContainer = document.getElementById('offer-code-container');
    const offerCodeMessage = document.getElementById('offer-code-message');
    
    offerCodeInput.addEventListener('input', () => {
        const offerCode = offerCodeInput.value.trim();
        if (offerCode === 'alx') {
            offerCodeMessage.textContent = 'Offer code applied! Total is now $0.';
            updateSubtotalAndTotal();  // Update the totals to reflect the offer
        } else {
            offerCodeMessage.textContent = 'Enter a valid offer code';
        }
    });

    // Initial update for subtotal and total when page loads
    updateSubtotalAndTotal();
});
