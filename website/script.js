function generateTable() {
    const rows = 5;
    const columns = 6;
    const container = document.getElementById("tableContainer");

    container.innerHTML = '';

    const table = document.createElement("table");

    for(let i = 0; i < rows; i++) {
        const tr = document.createElement("tr");
        for(let j = 0; j < columns; j++) {
            const td = document.createElement("td");
            td.textContent = "(" + i + ", " + j + ")";
            tr.appendChild(td);
        }
        table.appendChild(tr);
    }

    container.appendChild(table);
}