document.addEventListener("DOMContentLoaded", function () {
    loadStoreName();
    fetchMonthlyRevenue();
    fetchOrders();
});

function loadStoreName() {
    fetch("http://127.0.0.1:5000/get_store_name")
        .then(response => response.json())
        .then(data => {
            document.getElementById("store-name").innerText = data;
        })
        .catch(error => console.error("Error fetching store name:", error));
}

function fetchMonthlyRevenue() {
    fetch("http://127.0.0.1:5000/monthlyrevenue")
        .then(response => response.json())
        .then(data => {
            document.getElementById("monthly-revenue").innerText = "Monthly Revenue : ₹ " + data;
        })
        .catch(error => console.error("Error fetching revenue:", error));
}

function fetchOrders() {
    document.getElementById("loading-message").style.display = "block";
    fetch("http://127.0.0.1:5000/orders")
        .then(response => response.json())
        .then(data => {
            const orderList = document.getElementById("order-list");
            orderList.innerHTML = "";
            data.forEach(order => {
                const row = `
                    <tr>
                        <td>${order.order_id}</td>
                        <td>₹${order.amount}</td>
                        <td>${order.customer_name}</td>
                        <td>${order.date}</td>
                        <td><button class="details-btn">View</button></td>
                    </tr>
                `;
                orderList.innerHTML += row;
            });
            document.getElementById("loading-message").style.display = "none";
        })
        .catch(error => console.error("Error fetching orders:", error));
}
