// Constants
const DELIVERY_FEE = 5.00;
const ITEMS_PER_PAGE = 6;
const SCROLL_THRESHOLD = 100;

// DOM Elements
const elements = {
    orderItems: document.getElementById('orderItems'),
    subtotal: document.getElementById('subtotal'),
    total: document.getElementById('total'),
    proceedBtn: document.getElementById('proceedToDelivery'),
    priceBreakdown: document.getElementById('priceBreakdown'),
    loadingIndicator: document.getElementById('loadingIndicator')
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadCartItems();
    renderInitialOrder();
    setupEventListeners();
    updatePriceBreakdown();
});

function renderOrderItems(page) {
    const start = (page - 1) * ITEMS_PER_PAGE;
    const end = start + ITEMS_PER_PAGE;
    const items = cartItems.slice(start, end);

    const fragment = document.createDocumentFragment();
    items.forEach(item => {
        fragment.appendChild(createMealCard(item));
    });

    elements.orderItems.appendChild(fragment);
    updateLoadingState(false);
}

function createMealCard(item) {
    const card = document.createElement('div');
    card.className = 'meal-card';
    card.dataset.id = item.id;

    card.innerHTML = `
        <img src="${sanitizeInput(item.image)}" alt="${sanitizeInput(item.name)}">
        <div class="meal-info">
            <div class="meal-header">
                <h3>${sanitizeInput(item.name)}</h3>
                <span class="price">$${item.price.toFixed(2)}</span>
            </div>
            <p class="description">${sanitizeInput(item.description)}</p>
            <div class="meal-footer">
                <div class="quantity-controls">
                    <button class="quantity-btn decrease" aria-label="Decrease quantity">-</button>
                    <span class="quantity-value">${item.quantity}</span>
                    <button class="quantity-btn increase" aria-label="Increase quantity">+</button>
                </div>
                <span class="item-total">$${(item.price * item.quantity).toFixed(2)}</span>
            </div>
        </div>
    `;

    return card;
}

function updatePriceBreakdown() {
    const subtotal = calculateSubtotal();
    const total = subtotal + DELIVERY_FEE;

    elements.priceBreakdown.innerHTML = `
        <div class="price-summary">
            <div class="price-row">
                <span>Subtotal</span>
                <span>$${subtotal.toFixed(2)}</span>
            </div>
            <div class="price-row">
                <span>Delivery Fee</span>
                <span>$${DELIVERY_FEE.toFixed(2)}</span>
            </div>
            <div class="price-row total">
                <span>Total</span>
                <span>$${total.toFixed(2)}</span>
            </div>
        </div>
        <button id="proceedToDelivery" class="proceed-btn" ${cartItems.length === 0 ? 'disabled' : ''}>
            <span>Proceed to Delivery</span>
            <i class="fas fa-arrow-right"></i>
        </button>
    `;
}

function handleScroll() {
    if (isLoading) return;

    const { scrollTop, scrollHeight, clientHeight } = document.documentElement;

    if (scrollHeight - scrollTop - clientHeight < SCROLL_THRESHOLD) {
        loadMoreItems();
    }
}

function updateLoadingState(loading) {
    isLoading = loading;
    elements.loadingIndicator.style.display = loading ? 'block' : 'none';
}

function loadMoreItems() {
    if (currentPage * ITEMS_PER_PAGE >= cartItems.length) return;

    updateLoadingState(true);
    currentPage++;

    setTimeout(() => {
        renderOrderItems(currentPage);
    }, 500);
}

