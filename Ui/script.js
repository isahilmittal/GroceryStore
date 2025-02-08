
document.addEventListener("DOMContentLoaded", function () {
    loadStoreName();
    document.getElementById("product-search").addEventListener("input", fetchProducts);
});

function loadStoreName() {
    fetch("http://127.0.0.1:5000/get_store_name")
        .then(response => response.json())
        .then(data => {
            document.getElementById("store-name").innerText = data[0];
            document.getElementById("owner-name").innerText = data[1];
            
        })
        .catch(error => console.error("Error fetching store name:", error));
}

document.addEventListener("DOMContentLoaded", fetchProducts);
        
function fetchProducts() {
    document.getElementById("loading").style.display = "block";
    fetch('http://127.0.0.1:5000/products_home')
    .then(response => response.json())
    .then(data => {
        let tableBody = document.getElementById("productBody");
        tableBody.innerHTML = ""; 
        document.getElementById("loading").style.display = "none";

        data.forEach(product => {
            let row = `<tr>
                <td>${product.product_name}</td>
                <td>${product.Unit}</td>
                <td>${product.product_id}</td>
                <td>
                    <button class="update-btn" onclick="updatePrice(${product.product_id})">Add</button>
                    
                </td>
            </tr>`;
            tableBody.innerHTML += row;
        });
    });
}

function filterProducts() {
    let input = document.getElementById("searchInput").value.toLowerCase();
    let rows = document.querySelectorAll("#productBody tr");
    rows.forEach(row => {
        let productName = row.children[0].textContent.toLowerCase(); // Fixed index (0 = Product Name)
        row.style.display = productName.includes(input) ? "" : "none";
    });
}







function addProduct(product) {
    let tbody = document.querySelector("#order-summary tbody");
    let row = document.createElement("tr");
    row.innerHTML = `
        <td>${product.product_name}</td>
        <td><input type="number" value="1" min="1" onchange="updateTotal(this, ${product.price})"></td>
        <td>₹${product.price}</td>
        <td class="item-total">₹${product.price}</td>
        <td><button onclick="removeRow(this)">X</button></td>
    `;
    tbody.appendChild(row);
    updateTotalAmount();
}

function updateTotal(input, price) {
    let quantity = parseFloat(input.value);
    let totalCell = input.closest("tr").querySelector(".item-total");
    totalCell.innerText = `₹${(quantity * price).toFixed(2)}`;
    updateTotalAmount();
}

function removeRow(button) {
    button.closest("tr").remove();
    updateTotalAmount();
}

function updateTotalAmount() {
    let total = 0;
    document.querySelectorAll(".item-total").forEach(cell => {
        total += parseFloat(cell.innerText.replace("₹", ""));
    });
    document.getElementById("total-amount").innerText = total.toFixed(2);
}