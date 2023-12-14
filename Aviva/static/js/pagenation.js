document.addEventListener("DOMContentLoaded", function () {
const table = document.querySelector(".table-data table");
const tbody = table.querySelector("tbody");
const itemsPerPage = 10; // Set the number of items per page

let currentPage = 1;
let rows = Array.from(tbody.querySelectorAll("tr"));

function showPage(page) {
    const start = (page - 1) * itemsPerPage;
    const end = start + itemsPerPage;

    rows.forEach((row, index) => {
    row.style.display = index >= start && index < end ? "table-row" : "none";
    });
}

function updatePaginationButtons() {
    const totalPages = Math.ceil(rows.length / itemsPerPage);

    const paginationContainer = document.createElement("div");
    paginationContainer.className = "pagination";

    for (let i = 1; i <= totalPages; i++) {
    const button = document.createElement("button");
    button.textContent = i;
    button.addEventListener("click", function () {
        currentPage = i;
        showPage(currentPage);
        updatePaginationButtons(); // Update buttons on click
    });

    // Add class for active page
    if (i === currentPage) {
        button.classList.add("active");
    }

    // Add hover effect
    button.addEventListener("mouseover", function () {
        button.classList.add("hover");
    });

    button.addEventListener("mouseout", function () {
        button.classList.remove("hover");
    });

    paginationContainer.appendChild(button);
    }

    // Remove existing pagination if any
    const existingPagination = table.parentNode.querySelector(".pagination");
    if (existingPagination) {
    existingPagination.remove();
    }

    table.parentNode.insertBefore(paginationContainer, table.nextSibling);
}

// Initial setup
showPage(currentPage);
updatePaginationButtons();
});