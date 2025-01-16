// State management
let cartState = {};
let isInitialized = false;
let currentPage = 1;
let totalPages = 1;
const ITEMS_PER_PAGE = 8;

// Cart management functions
async function initializeCartState() {
    if (isInitialized) return cartState;

    try {
        const response = await fetch("/api/v1/cart/state");
        if (response.ok) {
            const data = await response.json();
            cartState = data.items.reduce((acc, item) => {
                acc[item.menu_item_id] = item.quantity;
                return acc;
            }, {});
            updateCartBadge(data.order?.total_price || 0);
            updateAllQuantities();
            isInitialized = true;
            return cartState;
        }
    } catch (error) {
        console.error("Cart state error:", error);
    }
    return {};
}

// UI Helper functions
function updateQuantityDisplay(mealId, quantity) {
    const quantitySpan = document.querySelector(`.meal[data-meal-id="${mealId}"] .quantity-value`);
    if (quantitySpan) {
        quantitySpan.textContent = quantity;
        quantitySpan.setAttribute("data-quantity", quantity);
    }
}

function updateCartBadge(totalPrice) {
    const cartBadge = document.getElementById("cart-count");
    if (!totalPrice || totalPrice <= 0) {
        cartBadge.textContent = "";
        cartBadge.classList.remove("cart-count-active");
        cartBadge.classList.add("cart-count-hidden");
    } else {
        cartBadge.textContent = `$${parseFloat(totalPrice).toFixed(2)}`;
        cartBadge.classList.remove("cart-count-hidden");
        cartBadge.classList.add("cart-count-active");
        cartBadge.offsetHeight; // Trigger reflow for smooth transition
    }
}

function showToast(message, type = "success") {
    let toast = document.getElementById("toast") || createToastElement();
    toast.className = `toast ${type}`;
    toast.textContent = message;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 3000);
}

function createToastElement() {
    const toast = document.createElement("div");
    toast.id = "toast";
    document.body.appendChild(toast);
    return toast;
}

// Search and display functions
async function performSearch(resetPage = false) {
    if (resetPage) currentPage = 1;

    const searchBar = document.getElementById("search_bar");
    const filterSelect = document.getElementById("filter");
    const query = searchBar.value;
    const restaurant = filterSelect.value;

    try {
        const response = await fetch(
            `/api/v1/search?query=${encodeURIComponent(query)}&restaurant=${encodeURIComponent(restaurant)}&page=${currentPage}`
        );
        const data = await response.json();
        updateMealsSection(data.meals);
        updatePagination(data.total);
    } catch (error) {
        console.error("Search failed:", error);
    }
}

// Initialization and event listeners
document.addEventListener("DOMContentLoaded", async function () {
    cartState = await initializeCartState();

    const searchBar = document.getElementById("search_bar");
    const searchButton = document.getElementById("searchButton");
    const filterSelect = document.getElementById("filter");

    // Search events
    searchButton.addEventListener("click", () => performSearch(true));
    searchBar.addEventListener("keyup", (event) => {
        if (event.key === "Enter") performSearch(true);
    });
    filterSelect.addEventListener("change", () => performSearch(true));

    // Pagination events
    setupPaginationListeners();

    // Initial search
    performSearch(true);
});

// Visibility change handler
document.addEventListener("visibilitychange", async () => {
    if (document.visibilityState === "visible") {
        await initializeCartState();
    }
});

// Helper functions

function sanitizeName(name) {
    return name.replace(/\s+/g, "_");
}

async function findImage(basePath, fileName) {
    const extensions = ["png"];
    for (const ext of extensions) {
        try {
            const response = await fetch(
                `../static/images/menu_items/${basePath}/${fileName}.${ext}`
            );
            if (response.ok) {
                return `${fileName}.${ext}`;
            }
        } catch (error) {
            continue;
        }
    }
    return "default.png"; // Fallback image
}

async function updateMealsSection(meals) {
    const mealElements = await Promise.all(
        meals.map(async (meal) => {
            const imagePath = await findImage(
                sanitizeName(meal.restaurant_name),
                sanitizeName(meal.name)
            );

            // Get quantity from cartState
            const quantity = cartState[meal.id] || 0;

            return `
                <div class="meal" data-meal-id="${meal.id}">
                    <img src="../static/images/menu_items/${sanitizeName(
                        meal.restaurant_name
                    )}/${imagePath}"
                         alt="${meal.name}"
                         onerror="this.src='../static/images/default.png'" />
                    <hr />
                    <div class="meal-info">
                        <h3>${meal.name}</h3>
                        <div class="meal-footer">
                            <span class="price" data-price="${meal.price}">$${
                meal.price
            }</span>
                            <div class="quantity">
                                <img src="../static/images/reduce.png" class="decrease" alt="Reduce quantity" />
                                <span class="quantity-value" data-quantity="${quantity}">${quantity}</span>
                                <img src="../static/images/add.png" class="increase" alt="Increase quantity" />
                            </div>
                        </div>
                    </div>
                </div>
            `;
        })
    );

    const mealsSection = document.querySelector(".meals");
    mealsSection.innerHTML = mealElements.join("");
    attachQuantityListeners();
}

function attachQuantityListeners() {
    const meals = document.querySelectorAll(".meal");

    meals.forEach((meal) => {
        const decreaseBtn = meal.querySelector(".decrease");
        const increaseBtn = meal.querySelector(".increase");
        const quantitySpan = meal.querySelector(".quantity-value");
        const mealId = meal.dataset.mealId;

        async function handleQuantityUpdate(action) {
            try {
                // 1. Pre-checks
                const isAuthenticated =
                    document.body.classList.contains("user-logged-in");
                if (!isAuthenticated) {
                    localStorage.setItem(
                        "pendingCartAction",
                        JSON.stringify({
                            mealId,
                            action,
                            returnUrl: window.location.pathname,
                        })
                    );
                    window.location.href = "/login";
                    return;
                }

                const response = await fetch("/api/v1/cart/update", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        menu_item_id: mealId,
                        action: action,
                    }),
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || "Failed to update cart");
                }

                const data = await response.json();

                // Update UI immediately based on action and response
                let newQuantity;
                if (action === "decrease") {
                    const currentQuantity = parseInt(
                        quantitySpan.getAttribute("data-quantity")
                    );
                    newQuantity = currentQuantity > 1 ? currentQuantity - 1 : 0;
                } else {
                    newQuantity = data.item.quantity;
                }

                // Always update the UI with the new quantity
                updateQuantityDisplay(mealId, newQuantity);
                updateCartBadge(data.order ? data.order.total_price : 0);

                // Update cartState
                if (newQuantity === 0) {
                    delete cartState[mealId];
                } else {
                    cartState[mealId] = newQuantity;
                }

                // Show appropriate message
                if (
                    (data.order && data.order.status === "cancelled") ||
                    newQuantity === 0
                ) {
                    showToast("Item removed from cart");
                } else {
                    showToast(`Cart ${action}d successfully`);
                }

                // Update localStorage
                localStorage.setItem("cartState", JSON.stringify(cartState));
            } catch (error) {
                console.error("Error:", error);
                showToast(error.message, "error");
            }
        }

        decreaseBtn.addEventListener("click", () =>
            handleQuantityUpdate("decrease")
        );
        increaseBtn.addEventListener("click", () =>
            handleQuantityUpdate("increase")
        );
    });
}

function updatePagination(totalItems) {
    totalPages = Math.ceil(totalItems / ITEMS_PER_PAGE);

    // Don't show pagination if only one page
    if (totalPages <= 1) {
        document.querySelector(".pagination").style.display = "none";
        return;
    }

    document.querySelector(".pagination").style.display = "flex";

    // Update page numbers display
    let pagesHtml = "";

    // Logic for displaying page numbers with ellipsis
    const showPage = (i) => {
        pagesHtml += `<span class="page-number ${i === currentPage ? "active" : ""}"
            data-page="${i}">${i}</span>`;
    };

    const showEllipsis = () => {
        pagesHtml += '<span class="ellipsis">...</span>';
    };

    // Always show first page
    showPage(1);

    // Logic for pages between first and last
    for (let i = 2; i < totalPages; i++) {
        if (
            i === currentPage || // Current page
            i === currentPage - 1 || // One before current
            i === currentPage + 1 || // One after current
            i === 2 || // Second page
            i === totalPages - 1 // Second-to-last page
        ) {
            showPage(i);
        } else if (
            i === currentPage - 2 ||
            i === currentPage + 2
        ) {
            showEllipsis();
        }
    }

    // Always show last page if more than one page
    if (totalPages > 1) {
        showPage(totalPages);
    }

    // Update DOM
    const pageNumbers = document.getElementById("pageNumbers");
    pageNumbers.innerHTML = pagesHtml;

    // Update prev/next buttons state
    const prevPage = document.getElementById("prevPage");
    const nextPage = document.getElementById("nextPage");

    prevPage.classList.toggle("disabled", currentPage === 1);
    nextPage.classList.toggle("disabled", currentPage === totalPages);
}

function setupPaginationListeners() {
    const prevPage = document.getElementById("prevPage");
    const nextPage = document.getElementById("nextPage");
    const pageNumbers = document.getElementById("pageNumbers");

    prevPage.addEventListener("click", function (e) {
        e.preventDefault();
        if (currentPage > 1) {
            currentPage--;
            performSearch(false); // Don't reset page when using pagination
        }
    });

    nextPage.addEventListener("click", function (e) {
        e.preventDefault();
        if (currentPage < totalPages) {
            currentPage++;
            performSearch(false); // Don't reset page when using pagination
        }
    });

    // Add click handler for page numbers
    pageNumbers.addEventListener("click", function (e) {
        if (e.target.classList.contains("page-number")) {
            e.preventDefault();
            currentPage = parseInt(e.target.dataset.page);
            performSearch(false); // Don't reset page when using pagination
        }
    });
}

// Update all quantities in UI
function updateAllQuantities() {
    document.querySelectorAll(".meal").forEach((meal) => {
        const mealId = meal.dataset.mealId;
        const quantity = cartState[mealId] || 0;
        updateQuantityDisplay(mealId, quantity);
    });
}
