// Constants
const DELIVERY_FEE = 5.00;
const ITEMS_PER_PAGE = 8;

// DOM Elements
const elements = {
    orderItems: document.getElementById('orderItems'),
    subtotal: document.getElementById('subtotal'),
    total: document.getElementById('total'),
    proceedBtn: document.getElementById('proceedToDelivery')
};

// State Management
let cartItems = [];
let currentPage = 1;
let isLoading = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadCartItems();
    renderInitialOrder();
    setupEventListeners();
});

function loadCartItems() {
    try {
        cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
    } catch (error) {
        console.error('Error loading cart:', error);
        cartItems = [];
    }
}

function renderInitialOrder() {
    renderOrderItems(1);
    updatePriceDisplay();
}

function renderOrderItems(page) {
    const start = (page - 1) * ITEMS_PER_PAGE;
    const end = start + ITEMS_PER_PAGE;
    const items = cartItems.slice(start, end);

    items.forEach(item => {
        const mealCard = createMealCard(item);
        elements.orderItems.appendChild(mealCard);
    });
}

function createMealCard(item) {
    const card = document.createElement('div');
    card.className = 'meal-card';
    card.dataset.id = item.id;

    card.innerHTML = `
        <img src="${sanitizeInput(item.image)}" alt="${sanitizeInput(item.name)}">
        <div class="meal-info">
            <h3>${sanitizeInput(item.name)}</h3>
            <p>${sanitizeInput(item.description)}</p>
            <div class="quantity-controls">
                <button class="quantity-btn decrease">-</button>
                <span class="quantity-value">${item.quantity}</span>
                <button class="quantity-btn increase">+</button>
            </div>
            <div class="price">$${(item.price * item.quantity).toFixed(2)}</div>
        </div>
    `;

    return card;
}

// Infinite Scroll Handler
function handleScroll() {
    if (isLoading) return;

    const lastCard = elements.orderItems.lastElementChild;
    if (!lastCard) return;

    const lastCardOffset = lastCard.offsetTop + lastCard.clientHeight;
    const pageOffset = window.pageYOffset + window.innerHeight;

    if (pageOffset > lastCardOffset - 20) {
        loadMoreItems();
    }
}

function loadMoreItems() {
    if (currentPage * ITEMS_PER_PAGE >= cartItems.length) return;

    isLoading = true;
    currentPage++;

    renderOrderItems(currentPage);
    isLoading = false;
}

function updatePriceDisplay() {
    const subtotal = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    elements.subtotal.textContent = `$${subtotal.toFixed(2)}`;
    elements.total.textContent = `$${(subtotal + DELIVERY_FEE).toFixed(2)}`;
}

function setupEventListeners() {
    window.addEventListener('scroll', handleScroll);
    elements.orderItems?.addEventListener('click', handleQuantityChange);
    elements.proceedBtn?.addEventListener('click', handleProceedToDelivery);
}

function handleProceedToDelivery() {
    if (cartItems.length === 0) {
        alert('Please add items to your cart before proceeding');
        return;
    }

    try {
        const orderSummary = {
            items: cartItems,
            subtotal: elements.subtotal.textContent,
            total: elements.total.textContent,
            deliveryFee: DELIVERY_FEE
        };

        localStorage.setItem('orderSummary', JSON.stringify(orderSummary));
        window.location.href = 'delivery.html';
    } catch (error) {
        console.error('Error proceeding to delivery:', error);
    }
}

function sanitizeInput(input) {
    const div = document.createElement('div');
    div.textContent = input;
    return div.innerHTML;
}

