document.addEventListener('DOMContentLoaded', () => {
    const orderItems = document.getElementById('orderItems');
    const itemizedPrices = document.getElementById('itemizedPrices');
    const subtotalElement = document.getElementById('subtotal');
    const totalElement = document.getElementById('total');
    const proceedBtn = document.getElementById('proceedToDelivery');
    const deliveryFee = 5.00;

    function updateOrderSummary() {
        orderItems.innerHTML = '';
        itemizedPrices.innerHTML = '';
        let subtotal = 0;

        cartItems.forEach(item => {
            // Create order item box
            const orderItem = document.createElement('div');
            orderItem.className = 'order-item';
            orderItem.innerHTML = `
                <img src="${item.image || 'default-meal.jpg'}" alt="${item.name}">
                <div class="item-details">
                    <h3>${item.name}</h3>
                    <div class="item-controls">
                        <div class="quantity-controls">
                            <button class="quantity-btn decrease" data-id="${item.id}">-</button>
                            <span class="quantity">${item.quantity}</span>
                            <button class="quantity-btn increase" data-id="${item.id}">+</button>
                        </div>
                        <button class="remove-btn" data-id="${item.id}">Remove</button>
                    </div>
                </div>
                <div class="item-price">$${(item.price * item.quantity).toFixed(2)}</div>
            `;
            orderItems.appendChild(orderItem);

            // Add to itemized prices
            const itemPrice = document.createElement('div');
            itemPrice.className = 'itemized-price';
            itemPrice.innerHTML = `
                <span>${item.name} x${item.quantity}</span>
                <span>$${(item.price * item.quantity).toFixed(2)}</span>
            `;
            itemizedPrices.appendChild(itemPrice);

            subtotal += item.price * item.quantity;
        });

        subtotalElement.textContent = `$${subtotal.toFixed(2)}`;
        totalElement.textContent = `$${(subtotal + deliveryFee).toFixed(2)}`;

        // Update proceed button state
        proceedBtn.disabled = cartItems.length === 0;
    }

    // Event delegation for quantity controls
    orderItems.addEventListener('click', (e) => {
        if (e.target.classList.contains('quantity-btn')) {
            const itemId = e.target.dataset.id;
            const isIncrease = e.target.classList.contains('increase');
            updateItemQuantity(itemId, isIncrease);
            updateOrderSummary();
        }
    });

    updateOrderSummary();
});

document.getElementById('proceedToDelivery').addEventListener('click', () => {
    // Check if cart has items
    const cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];

    if (cartItems.length === 0) {
        alert('Your cart is empty! Please add items before proceeding.');
        return;
    }

    // Store order summary
    const orderSummary = {
        items: cartItems,
        subtotal: document.getElementById('subtotal').textContent,
        total: document.getElementById('total').textContent,
        deliveryFee: '5.00'
    };
    localStorage.setItem('orderSummary', JSON.stringify(orderSummary));

    // Navigate to delivery page
    window.location.href = '/delivery';  // Changed from /location
});

