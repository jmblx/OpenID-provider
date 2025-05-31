let afterIdStack = [];
let currentAfterId = 0;
const pageSize = 15;

document.addEventListener("DOMContentLoaded", async function () {
    await loadClients();

    document.getElementById("next-page").addEventListener("click", async () => {
        if (lastLoadedId !== null) {
            afterIdStack.push(currentAfterId);
            currentAfterId = lastLoadedId;
            await loadClients();
        }
    });

    document.getElementById("prev-page").addEventListener("click", async () => {
        if (afterIdStack.length > 0) {
            currentAfterId = afterIdStack.pop();
            await loadClients();
        }
    });
});

let lastLoadedId = null;

async function loadClients() {
    try {
        const url = `/api/client/ids_data?after_id=${currentAfterId}&page_size=${pageSize}`;
        const response = await fetch(url);
        if (!response.ok) throw new Error("Ошибка загрузки данных");
        const clients = await response.json();

        renderClients(clients);

        const ids = Object.keys(clients).map(Number);
        lastLoadedId = ids.length > 0 ? Math.max(...ids) : null;

        document.getElementById("next-page").disabled = !lastLoadedId;
        document.getElementById("prev-page").disabled = afterIdStack.length === 0;
    } catch (error) {
        console.error(error);
        alert("Не удалось загрузить список клиентов.");
    }
}

function renderClients(clients) {
    const container = document.getElementById("clients-container");
    container.innerHTML = "";

    Object.entries(clients).forEach(([id, data]) => {
        const clientCard = document.createElement("div");
        clientCard.classList.add("col-md-3", "card-item", "client");
        clientCard.textContent = data.name;
        clientCard.onclick = () => window.location.href = `/pages/client.html?clientId=${id}`;
        container.appendChild(clientCard);
    });
}
