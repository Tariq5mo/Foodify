// Initialize cart items
let cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];

// Update cart function
function updateCart(mealId, mealName, mealPrice, quantityChange) {
    const existingItemIndex = cartItems.findIndex(item => item.id === mealId);

    if (existingItemIndex !== -1) {
        cartItems[existingItemIndex].quantity += quantityChange;
        if (cartItems[existingItemIndex].quantity <= 0) {
            cartItems.splice(existingItemIndex, 1);
        }
    } else if (quantityChange > 0) {
        cartItems.push({
            id: mealId,
            name: mealName,
            price: mealPrice,
            quantity: quantityChange
        });
    }

    localStorage.setItem('cartItems', JSON.stringify(cartItems));
    updateCartDisplay();
}

// Update cart display
function updateCartDisplay() {
    const cartCount = document.getElementById('cart-count');
    const totalQuantity = cartItems.reduce((total, item) => total + item.quantity, 0);

    cartCount.textContent = totalQuantity;
    cartCount.classList.toggle('cart-count-hidden', totalQuantity === 0);
    cartCount.style.backgroundColor = totalQuantity > 0 ? 'red' : 'transparent';
}

// Add event listeners to meals
document.querySelectorAll('.meal').forEach(mealElement => {
    const mealId = mealElement.getAttribute('data-meal-id');
    const mealName = mealElement.querySelector('h3').textContent;
    const mealPrice = parseFloat(mealElement.querySelector('.price').getAttribute('data-price'));
    const quantityElement = mealElement.querySelector('.quantity-value');

    // Decrease quantity
    mealElement.querySelector('.decrease').addEventListener('click', () => {
        let quantity = parseInt(quantityElement.getAttribute('data-quantity'));
        if (quantity > 0) {
            quantity -= 1;
            quantityElement.setAttribute('data-quantity', quantity);
            quantityElement.innerText = quantity;
            updateCart(mealId, mealName, mealPrice, -1);
        }
    });

    // Increase quantity
    mealElement.querySelector('.increase').addEventListener('click', () => {
        let quantity = parseInt(quantityElement.getAttribute('data-quantity'));
        quantity += 1;
        quantityElement.setAttribute('data-quantity', quantity);
        quantityElement.innerText = quantity;
        updateCart(mealId, mealName, mealPrice, 1);
    });
});

// Cart icon click handler
document.querySelector('.cart-icon-container a').addEventListener('click', (e) => {
    e.preventDefault();
    if (cartItems.length > 0) {
        window.location.href = 'payment.html';
    } else {
        alert('Your cart is empty!');
    }
});

// Initialize cart display
updateCartDisplay();

// Function to update the cart (both quantity and price)
function updateCart(mealId, mealName, mealPrice, quantityChange) {
    const existingItemIndex = cartItems.findIndex(item => item.id === mealId);

    if (existingItemIndex !== -1) {
        // If the meal already exists in the cart, update the quantity
        const existingItem = cartItems[existingItemIndex];
        existingItem.quantity += quantityChange;
        if (existingItem.quantity <= 0) {
            cartItems.splice(existingItemIndex, 1); // Remove the meal if the quantity is zero or less
        }
    } else if (quantityChange > 0) {
        // If the meal does not exist in the cart, add it
        cartItems.push({
            id: mealId,
            name: mealName,
            price: mealPrice,
            quantity: quantityChange
        });
    }

    // Update the cart display based on the array
    updateCartDisplay();
}

// Function to update the cart display (showing only the number of meals in the nav bar)
function updateCartDisplay() {
    const cartCount = document.getElementById('cart-count');

    // Calculate the total number of meals in the cart
    const totalQuantity = cartItems.reduce((total, item) => total + item.quantity, 0);

    if (totalQuantity > 0) {
        // If the quantity is greater than zero, show a red badge
        if (!cartCount) {
            // If the element does not exist, add it to the DOM
            const span = document.createElement('span');
            span.id = 'cart-count';
            span.classList.remove('cart-count-hidden'); // Remove the hidden class
            span.style.backgroundColor = 'red'; // Add red background color
            span.style.color = 'white'; // Change the color to white for the number
            span.style.padding = '0.2em'; // Add padding to show the badge
            span.style.borderRadius = '50%'; // Make the badge circular
            document.querySelector('.cart-icon-container a').appendChild(span);  // Add it to the link
        }
    } else {
        // If the quantity is zero, remove the element completely
        if (cartCount) {
            cartCount.remove();
        }
    }
}

// Call the function to update the cart
updateCartDisplay();


//================================================================================================
// Modal functionality
const knowMoreButton = document.querySelector('.know_more'); // Button to open the modal
const modal = document.querySelector('.modal'); // Modal container
const closeModal = document.querySelector('.close'); // Close button inside the modal

// Add event listener to open the modal when the 'Know More' button is clicked
knowMoreButton.addEventListener('click', () => {
    modal.classList.add('show'); // Add class to show the modal with animation
    modal.classList.remove('fade-out'); // Remove fade-out class if modal is being shown
});

// Add event listener to close the modal when the close button is clicked
closeModal.addEventListener('click', () => {
    modal.classList.add('fade-out'); // Add fade-out class to trigger fade-out animation
    setTimeout(() => {
        modal.classList.remove('show', 'fade-out'); // Remove 'show' and 'fade-out' classes after animation
    }, 400); // Match the animation duration (e.g., 400ms)
});

// Add event listener to close the modal if the user clicks outside of it
window.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.classList.add('fade-out'); // Add fade-out class to trigger fade-out animation
        setTimeout(() => {
            modal.classList.remove('show', 'fade-out'); // Remove 'show' and 'fade-out' classes after animation
        }, 400); // Match the animation duration (e.g., 400ms)
    }
}
