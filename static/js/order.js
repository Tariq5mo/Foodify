document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const orderItems = document.getElementById('orderItems');
    const subtotalElement = document.getElementById('subtotal');
    const totalElement = document.getElementById('total');
    const proceedBtn = document.getElementById('proceedToDelivery');

    // Constants
    const DELIVERY_FEE = 5.00;

    // Get cart items from localStorage

    function updatePriceBreakdown() {
        const subtotal = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        const total = subtotal + DELIVERY_FEE;

        document.getElementById('itemizedPrices').innerHTML = cartItems
            .map(item => `
                <div class="price-item">
                    <span>${item.name} x${item.quantity}</span>
                    <span>$${(item.price * item.quantity).toFixed(2)}</span>
                </div>
            `).join('');

        subtotalElement.textContent = `$${subtotal.toFixed(2)}`;
        totalElement.textContent = `$${total.toFixed(2)}`;
    }


    proceedBtn.addEventListener('click', () => {
        if (cartItems.length > 0) {
            localStorage.setItem('orderSummary', JSON.stringify({
                items: cartItems,
                subtotal: subtotalElement.textContent,
                total: totalElement.textContent,
                deliveryFee: DELIVERY_FEE
            }));
            window.location.href = 'delivery.html';
        }
    });

