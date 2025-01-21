// Cart state management
let cartItems = [];

async function updateCart(mealId, mealName, mealPrice, action) {
    try {
        const response = await fetch('/api/v1/cart/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                menu_item_id: mealId,
                action: action
            })
        });

        if (!response.ok) {
            throw new Error('Failed to update cart');
        }

        const data = await response.json();

        // Update local cart state
        updateLocalCart(data);
        // Update the cart display
        updateCartDisplay();

        // Show success toast
        showToast('Cart updated successfully', 'success');

    } catch (error) {
        console.error('Error updating cart:', error);
        showToast('Failed to update cart', 'error');
    }
}

// Meal elements event handling
const mealElements = document.querySelectorAll(".meal");

mealElements.forEach((mealElement) => {
    const mealId = mealElement.getAttribute("data-meal-id");
    const mealName = mealElement.querySelector("h3").textContent;
    const mealPrice = parseFloat(
        mealElement.querySelector(".price").getAttribute("data-price")
    );
    const quantityElement = mealElement.querySelector(".quantity-value");

    const decreaseButton = mealElement.querySelector(".decrease");
    const increaseButton = mealElement.querySelector(".increase");

    async function updateQuantity(action) {
        // Check if user is logged in
        const isLoggedIn = document.body.classList.contains("user-logged-in");
        if (!isLoggedIn) {
            localStorage.setItem("pendingCartAction", JSON.stringify({ mealId, action }));
            window.location.href = "/login";
            return;
        }
        await updateCart(mealId, mealName, mealPrice, action);
    }

    increaseButton.addEventListener("click", () => updateQuantity("increase"));
    decreaseButton.addEventListener("click", () => updateQuantity("decrease"));
});

// Cart display functions
function updateCartDisplay() {
    const cartCount = document.getElementById('cart-count');
    const totalQuantity = cartItems.reduce((total, item) => total + item.quantity, 0);

    if (totalQuantity > 0) {
        cartCount.textContent = totalQuantity;
        cartCount.classList.add('cart-count-active');
    } else {
        cartCount.classList.remove('cart-count-active');
    }
}

function updateLocalCart(data) {
    if (data.order) {
        const itemIndex = cartItems.findIndex(item => item.id === data.item.id);
        if (itemIndex !== -1) {
            if (data.item.quantity > 0) {
                cartItems[itemIndex].quantity = data.item.quantity;
            } else {
                cartItems.splice(itemIndex, 1);
            }
        } else if (data.item.quantity > 0) {
            cartItems.push(data.item);
        }
    } else {
        cartItems = [];
    }
}

// Toast notification function
function showToast(message, type) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }, 100);
}

// Modal functionality
const knowMoreButton = document.querySelector('.know_more'); // Button to open the modal
const modal = document.querySelector('.modal'); // Modal container
const closeModal = document.querySelector('.close'); // Close button inside the modal

// Add null check before adding event listener
if (knowMoreButton) {
    knowMoreButton.addEventListener('click', () => {
        modal.classList.add('show'); // Add class to show the modal with animation
        modal.classList.remove('fade-out'); // Remove fade-out class if modal is being shown
    });
}

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
});

const element = document.getElementById('elementId');
if (element) {
    element.addEventListener('click', handler);
}
