const API_URL = "http://localhost:5000";

let cart = [];

async function loadMenu() {

    const response = await fetch(`${API_URL}/api/menu`);

    const menu = await response.json();

    const menuDiv = document.getElementById("menu");

    menuDiv.innerHTML = "";

    menu.forEach(item => {

        menuDiv.innerHTML += `
            <div class="menu-item">
                <h3>${item.name}</h3>
                <p>${item.category}</p>
                <p>₹${item.price}</p>

                <button onclick="addToCart(${item.id}, '${item.name}', ${item.price})">
                    Add to Cart
                </button>
            </div>
        `;
    });
}


function addToCart(id, name, price) {

    cart.push({
        id: id,
        name: name,
        price: price
    });

    displayCart();
}


function displayCart() {

    const cartDiv = document.getElementById("cart");

    cartDiv.innerHTML = "<h3>Cart</h3>";

    let total = 0;

    cart.forEach(item => {

        total += Number(item.price);

        cartDiv.innerHTML += `
            <p>${item.name} - ₹${item.price}</p>
        `;
    });

    cartDiv.innerHTML += `<strong>Total: ₹${total}</strong>`;
}


async function placeOrder() {

    const customerName =
        document.getElementById("customerName").value;

    if (!customerName || cart.length === 0) {

        document.getElementById("message").innerText =
            "Please enter your name and add items.";

        return;
    }

    const total = cart.reduce(
        (sum, item) => sum + Number(item.price),
        0
    );

    const response = await fetch(
        `${API_URL}/api/order`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                customer_name: customerName,
                items: cart,
                total: total
            })
        }
    );

    const result = await response.json();

    document.getElementById("message").innerText =
        result.message;

    cart = [];

    displayCart();
}


loadMenu();