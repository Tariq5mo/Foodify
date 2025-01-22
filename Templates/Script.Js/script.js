document.addEventListener('DOMContentLoaded', () => {
    // Responsive menu toggle
    const menuIcon = document.getElementById('menu');
    const nav = document.querySelector('.nav');

    menuIcon.addEventListener('click', () => {
        nav.classList.toggle('active');
    });

    // Smooth scrolling for internal links
    const navLinks = document.querySelectorAll('.nav ul li a');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            if (link.getAttribute('href').startsWith('#')) {
                e.preventDefault();
                const targetId = link.getAttribute('href').substring(1);
                const targetSection = document.getElementById(targetId);
                window.scrollTo({
                    top: targetSection.offsetTop - document.querySelector('.header').offsetHeight,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Handle login form submission
    const loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const firstName = document.getElementById('first-name').value;
        const lastName = document.getElementById('last-name').value;
        const phone = document.getElementById('phone').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Save user data to local storage (for demonstration purposes)
        const userData = { firstName, lastName, phone, email, password };
        localStorage.setItem('user', JSON.stringify(userData));

        alert('Account created successfully!');
        window.location.href = 'home.html';
    });

    // Social login buttons (for demonstration purposes)
    const googleBtn = document.querySelector('.social-btn.google');
    const facebookBtn = document.querySelector('.social-btn.facebook');
    const instagramBtn = document.querySelector('.social-btn.instagram');

    googleBtn.addEventListener('click', () => {
        alert('Google login is not implemented in this demo.');
    });

    facebookBtn.addEventListener('click', () => {
        alert('Facebook login is not implemented in this demo.');
    });

    instagramBtn.addEventListener('click', () => {
        alert('Instagram login is not implemented in this demo.');
    });
});

    // Restaurant cards click event
    const restaurantCards = document.querySelectorAll('.restaurant-card');
    const mealsContainer = document.querySelector('.meals .container');
    const mealsSection = document.getElementById('meals');
    const cartCountElement = document.getElementById('cart-count');
    let cart = [];

    restaurantCards.forEach(card => {
        card.addEventListener('click', () => {
            const restaurant = card.getAttribute('data-restaurant');
            displayMeals(restaurant);
            mealsSection.scrollIntoView({ behavior: 'smooth' });
        });
    });

    // Display meals based on restaurant
    function displayMeals(restaurant) {
        mealsContainer.innerHTML = ''; // Clear previous meals
        const meals = getMealsForRestaurant(restaurant);
        meals.forEach(meal => {
            const mealCard = document.createElement('div');
            mealCard.classList.add('meal-card');
            mealCard.innerHTML = `
                <img src="${meal.image}" alt="${meal.name}">
                <h3>${meal.name}</h3>
                <p>${meal.description}</p>
                <p class="price">$${meal.price}</p>
                <button class="add-to-cart">Add to Cart</button>
            `;
            mealCard.querySelector('.add-to-cart').addEventListener('click', () => {
                addToCart(meal);
            });
            mealsContainer.appendChild(mealCard);
        });
    }

    // Get meals for a specific restaurant
    function getMealsForRestaurant(restaurant) {
        const meals = {
            restaurant1: [
                { name: 'food_1', description: 'Description 1', image: 'food_1.png', price: 10 },
                { name: 'food_3', description: 'Description 2', image: 'food_2.png', price: 12 },
                { name: 'food_3', description: 'Description 3', image: 'food_3.png', price: 15 },
                { name: 'food_4', description: 'Description 4', image: 'food_4.png', price: 8 },
                { name: 'food_5', description: 'Description 5', image: 'food_5.png', price: 9 },
                { name: 'food_6', description: 'Description 6', image: 'food_6.png', price: 11 },
                { name: 'food_7', description: 'Description 7', image: 'food_7.png', price: 13 },
                { name: 'food_8', description: 'Description 8', image: 'food_8.png', price: 14 },
                { name: 'food_9', description: 'Description 9', image: 'food_9.png', price: 10 },
                { name: 'Meal 10', description: 'Description 10', image: 'img/meal10.png', price: 12 },
                { name: 'Meal 11', description: 'Description 11', image: 'img/meal11.png', price: 15 },
                { name: 'Meal 12', description: 'Description 12', image: 'img/meal12.png', price: 8 }
            ],
            restaurant2: [
                { name: 'Meal 1', description: 'Description 1', image: 'food_10.png', price: 10 },
                { name: 'Meal 2', description: 'Description 2', image: 'food_11.png', price: 12 },
                { name: 'Meal 3', description: 'Description 3', image: 'food_12.png', price: 15 },
                { name: 'Meal 4', description: 'Description 4', image: 'food_13.png', price: 8 },
                { name: 'Meal 5', description: 'Description 5', image: 'food_14.png', price: 9 },
                { name: 'Meal 6', description: 'Description 6', image: 'food_15.png', price: 11 },
                { name: 'Meal 7', description: 'Description 7', image: 'food_16.png', price: 13 },
                { name: 'Meal 8', description: 'Description 8', image: 'food_17.png', price: 14 },
                { name: 'Meal 9', description: 'Description 9', image: 'img/meal9.png', price: 10 },
                { name: 'Meal 10', description: 'Description 10', image: 'img/meal10.png', price: 12 },
                { name: 'Meal 11', description: 'Description 11', image: 'img/meal11.png', price: 15 },
                { name: 'Meal 12', description: 'Description 12', image: 'img/meal12.png', price: 8 }
            ],
            restaurant3: [
                { name: 'Meal 1', description: 'Description 1', image: 'food_18.png', price: 10 },
                { name: 'Meal 2', description: 'Description 2', image: 'food_19.png', price: 12 },
                { name: 'Meal 3', description: 'Description 3', image: 'food_20.png', price: 15 },
                { name: 'Meal 4', description: 'Description 4', image: 'food_21.png', price: 8 },
                { name: 'Meal 5', description: 'Description 5', image: 'food_22.png', price: 9 },
                { name: 'Meal 6', description: 'Description 6', image: 'food_23.png', price: 11 },
                { name: 'Meal 7', description: 'Description 7', image: 'food_24.png', price: 13 },
                { name: 'Meal 8', description: 'Description 8', image: 'food_25.png', price: 14 },
                { name: 'Meal 9', description: 'Description 9', image: 'food.png.png', price: 10 },
                { name: 'Meal 10', description: 'Description 10', image: 'img/meal10.png', price: 12 },
                { name: 'Meal 11', description: 'Description 11', image: 'img/meal11.png', price: 15 },
                { name: 'Meal 12', description: 'Description 12', image: 'img/meal12.png', price: 8 }
            ],
            restaurant4: [
                { name: 'Meal 1', description: 'Description 1', image: 'img/meal1.png', price: 10 },
                { name: 'Meal 2', description: 'Description 2', image: 'img/meal2.png', price: 12 },
                { name: 'Meal 3', description: 'Description 3', image: 'img/meal3.png', price: 15 },
                { name: 'Meal 4', description: 'Description 4', image: 'img/meal4.png', price: 8 },
                { name: 'Meal 5', description: 'Description 5', image: 'img/meal5.png', price: 9 },
                { name: 'Meal 6', description: 'Description 6', image: 'img/meal6.png', price: 11 },
                { name: 'Meal 7', description: 'Description 7', image: 'img/meal7.png', price: 13 },
                { name: 'Meal 8', description: 'Description 8', image: 'img/meal8.png', price: 14 },
                { name: 'Meal 9', description: 'Description 9', image: 'img/meal9.png', price: 10 },
                { name: 'Meal 10', description: 'Description 10', image: 'img/meal10.png', price: 12 },
                { name: 'Meal 11', description: 'Description 11', image: 'img/meal11.png', price: 15 },
                { name: 'Meal 12', description: 'Description 12', image: 'img/meal12.png', price: 8 }
            ],
            restaurant5: [
                { name: 'Meal 1', description: 'Description 1', image: 'img/meal1.png', price: 10 },
                { name: 'Meal 2', description: 'Description 2', image: 'img/meal2.png', price: 12 },
                { name: 'Meal 3', description: 'Description 3', image: 'img/meal3.png', price: 15 },
                { name: 'Meal 4', description: 'Description 4', image: 'img/meal4.png', price: 8 },
                { name: 'Meal 5', description: 'Description 5', image: 'img/meal5.png', price: 9 },
                { name: 'Meal 6', description: 'Description 6', image: 'img/meal6.png', price: 11 },
                { name: 'Meal 7', description: 'Description 7', image: 'img/meal7.png', price: 13 },
                { name: 'Meal 8', description: 'Description 8', image: 'img/meal8.png', price: 14 },
                { name: 'Meal 9', description: 'Description 9', image: 'img/meal9.png', price: 10 },
                { name: 'Meal 10', description: 'Description 10', image: 'img/meal10.png', price: 12 },
                { name: 'Meal 11', description: 'Description 11', image: 'img/meal11.png', price: 15 },
                { name: 'Meal 12', description: 'Description 12', image: 'img/meal12.png', price: 8 }
            ],
            restaurant6: [
                { name: 'Meal 1', description: 'Description 1', image: 'img/meal1.png', price: 10 },
                { name: 'Meal 2', description: 'Description 2', image: 'img/meal2.png', price: 12 },
                { name: 'Meal 3', description: 'Description 3', image: 'img/meal3.png', price: 15 },
                { name: 'Meal 4', description: 'Description 4', image: 'img/meal4.png', price: 8 },
                { name: 'Meal 5', description: 'Description 5', image: 'img/meal5.png', price: 9 },
                { name: 'Meal 6', description: 'Description 6', image: 'img/meal6.png', price: 11 },
                { name: 'Meal 7', description: 'Description 7', image: 'img/meal7.png', price: 13 },
                { name: 'Meal 8', description: 'Description 8', image: 'img/meal8.png', price: 14 },
                { name: 'Meal 9', description: 'Description 9', image: 'img/meal9.png', price: 10 },
                { name: 'Meal 10', description: 'Description 10', image: 'img/meal10.png', price: 12 },
                { name: 'Meal 11', description: 'Description 11', image: 'img/meal11.png', price: 15 },
                { name: 'Meal 12', description: 'Description 12', image: 'img/meal12.png', price: 8 }
            ]
        };
        return meals[restaurant] || [];
    }

    // Add meal to cart
    function addToCart(meal) {
        const existingMeal = cart.find(item => item.name === meal.name);
        if (existingMeal) {
            existingMeal.quantity += 1;
        } else {
            cart.push({ ...meal, quantity: 1 });
        }
        updateCartCount();
        saveCartToLocalStorage();
    }

    // Update cart count
    function updateCartCount() {
        const totalItems = cart.reduce((total, item) => total + item.quantity, 0);
        cartCountElement.textContent = totalItems;
    }

    // Save cart to local storage
    function saveCartToLocalStorage() {
        localStorage.setItem('cart', JSON.stringify(cart));
    }

    // Load cart from local storage
    function loadCartFromLocalStorage() {
        const storedCart = localStorage.getItem('cart');
        if (storedCart) {
            cart = JSON.parse(storedCart);
            updateCartCount();
        }
    }

    // Load cart on page load
    loadCartFromLocalStorage();

    // Payment page functionality
    if (document.getElementById('payment')) {
        const invoiceDetails = document.querySelector('.invoice-details');
        const subtotalElement = document.getElementById('subtotal');
        const deliveryFeeElement = document.getElementById('delivery-fee');
        const totalElement = document.getElementById('total');

        let subtotal = 0;
        cart.forEach(meal => {
            const mealItem = document.createElement('div');
            mealItem.classList.add('meal-item');
            mealItem.innerHTML = `
                <p>${meal.name} - $${meal.price}</p>
            `;
            invoiceDetails.appendChild(mealItem);
            subtotal += meal.price;
        });

        const deliveryFee = subtotal * 0.02;
        const total = subtotal + deliveryFee;

        subtotalElement.textContent = subtotal.toFixed(2);
        deliveryFeeElement.textContent = deliveryFee.toFixed(2);
        totalElement.textContent = total.toFixed(2);
    }
