document.addEventListener('DOMContentLoaded', () => {
    const cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
    const cartContainer = document.getElementById('cart-items');
    const subtotalElement = document.getElementById('subtotal');
    const totalElement = document.getElementById('total');
    const deliveryFee = 5.00;
    const creditCardForm = document.getElementById('credit-card-form');
    const paymentOptions = document.querySelectorAll('input[name="payment"]');

    function updateCartCount() {
        const cartCount = document.getElementById('cart-count');
        const totalQuantity = cartItems.reduce((total, item) => total + item.quantity, 0);

        if (totalQuantity > 0) {
            cartCount.textContent = totalQuantity;
            cartCount.classList.remove('cart-count-hidden');
        } else {
            cartCount.classList.add('cart-count-hidden');
        }
    }

    function updateOrderSummary() {
        cartContainer.innerHTML = '';
        let subtotal = 0;

        cartItems.forEach(item => {
            const itemElement = document.createElement('div');
            itemElement.className = 'cart-item';
            itemElement.innerHTML = `
                <span>${item.name} x ${item.quantity}</span>
                <span>$${(item.price * item.quantity).toFixed(2)}</span>
            `;
            cartContainer.appendChild(itemElement);
            subtotal += item.price * item.quantity;
        });

        subtotalElement.textContent = `$${subtotal.toFixed(2)}`;
        totalElement.textContent = `$${(subtotal + deliveryFee).toFixed(2)}`;
    }

    function updateTotals() {
        fetch('/api/v1/payment/totals')
            .then(response => response.json())
            .then(data => {
                document.getElementById('subtotal').textContent = `$${data.subtotal}`;
                document.getElementById('total').textContent = `$${data.total}`;
            })
            .catch(error => console.error('Error:', error));
    }

    // Update totals periodically
    setInterval(updateTotals, 5000);

    paymentOptions.forEach(option => {
        option.addEventListener('change', () => {
            creditCardForm.style.display =
                option.value === 'credit' ? 'flex' : 'none';
        });
    });

    document.getElementById('confirm-payment').addEventListener('click', () => {
        const paymentMethod = document.querySelector('input[name="payment"]:checked').value;

        if (paymentMethod === 'credit' && !validateCreditCard()) {
            alert('Please fill in all credit card details correctly');
            return;
        }

        alert(`Order confirmed! Payment method: ${paymentMethod}`);
        localStorage.removeItem('cartItems');
        window.location.href = 'index.html';
    });

    function validateCreditCard() {
        if (document.querySelector('input[name="payment"]:checked').value !== 'credit') {
            return true;
        }

        const inputs = creditCardForm.querySelectorAll('input');
        return Array.from(inputs).every(input => input.value.trim() !== '');
    }

    updateOrderSummary();
    updateCartCount();
});
