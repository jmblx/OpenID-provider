let isCreateMode = false;
let initialClientData = null;

document.addEventListener("DOMContentLoaded", async function () {
    const params = new URLSearchParams(window.location.search);
    const clientId = params.get("clientId");

    if (!clientId) {
        isCreateMode = true;
        document.body.classList.add('create-mode');
        document.getElementById("client-name").textContent = "Создание нового клиента";
        enableClientEditing();
        addUrlField("", true);
        return;
    }

    const needAvatar = shouldUpdateAvatar(clientId);
    const clientData = await fetchClientData(clientId, needAvatar);

    if (clientData) {
        initialClientData = clientData;
        renderClientInfo(clientData);
        if (clientData.avatar_url) {
            const expiresAt = parsePresignedUrlExpiration(clientData.avatar_url);
            if (expiresAt) {
                localStorage.setItem(`avatar_url_${clientId}`, clientData.avatar_url);
                localStorage.setItem(`avatar_expires_${clientId}`, (expiresAt - 10).toString());
            }
            document.getElementById("client-avatar").src = clientData.avatar_url;
        } else {
            const cachedUrl = localStorage.getItem(`avatar_url_${clientId}`);
            if (cachedUrl) {
                document.getElementById("client-avatar").src = cachedUrl;
            }
        }
    }
});

function shouldUpdateAvatar(clientId) {
    const expires = localStorage.getItem(`avatar_expires_${clientId}`);
    if (!expires) return true;
    const expiresTs = parseInt(expires, 10);
    return isNaN(expiresTs) || Date.now() / 1000 > expiresTs;
}

function parsePresignedUrlExpiration(url) {
    try {
        const u = new URL(url);
        const dateStr = u.searchParams.get("X-Amz-Date");
        const expiresStr = u.searchParams.get("X-Amz-Expires");
        if (!dateStr || !expiresStr) return null;

        const date = new Date(
            Date.UTC(
                parseInt(dateStr.substring(0, 4)),
                parseInt(dateStr.substring(4, 6)) - 1,
                parseInt(dateStr.substring(6, 8)),
                parseInt(dateStr.substring(9, 11)),
                parseInt(dateStr.substring(11, 13)),
                parseInt(dateStr.substring(13, 15))
            )
        );
        return Math.floor(date.getTime() / 1000) + parseInt(expiresStr, 10);
    } catch {
        return null;
    }
}

async function fetchClientData(clientId, loadAvatar = false) {
    try {
        const url = new URL(`/api/client/${clientId}`, window.location.origin);
        if (loadAvatar) url.searchParams.set("load_avatar", "true");
        const response = await fetch(url.toString());
        if (!response.ok) throw new Error("Ошибка загрузки данных");
        return await response.json();
    } catch (error) {
        console.error(error);
        alert("Не удалось загрузить данные клиента.");
        return null;
    }
}

function renderClientInfo(clientData) {
    document.getElementById("client-name").textContent = `Клиент: ${clientData.name}`;
    document.getElementById("client-name-input").value = clientData.name;
    document.getElementById("client-base-url-input").value = clientData.base_url;
    document.getElementById("client-type-select").value = clientData.type;

    const urlList = document.getElementById("allowed-urls-list");
    urlList.innerHTML = "";
    clientData.allowed_redirect_urls.forEach(url => {
        addUrlField(url, false);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const editAvatarIcon = document.getElementById("edit-avatar-icon");
    const avatarInput = document.getElementById("avatar-file-input");

    editAvatarIcon.addEventListener("click", () => avatarInput.click());

    avatarInput.addEventListener("change", async () => {
        const file = avatarInput.files[0];
        if (!file) return;

        const params = new URLSearchParams(window.location.search);
        const clientId = params.get("clientId");
        if (!clientId) return alert("Клиент не выбран");

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch(`/api/client/${clientId}/avatar`, {
                method: "POST",
                body: formData
            });

            if (!response.ok) throw new Error("Ошибка загрузки аватарки");

            const data = await response.json();
            document.getElementById("client-avatar").src = data.avatar_path;

            localStorage.setItem(`avatar_url_${clientId}`, data.avatar_path);
            localStorage.removeItem(`avatar_expires_${clientId}`);
        } catch (e) {
            console.error(e);
            alert("Не удалось обновить аватарку");
        }
    });
});

function enableClientEditing() {
    document.getElementById("client-name-input").disabled = false;
    document.getElementById("client-base-url-input").disabled = false;
    document.getElementById("client-type-select").disabled = false;
    document.querySelector(".add-url-btn").classList.remove("hidden");
    document.getElementById("save-client-btn").classList.remove("hidden");
    document.getElementById("edit-icon").classList.add("hidden");

    const urlInputs = document.querySelectorAll("#allowed-urls-list input");
    urlInputs.forEach(input => input.disabled = false);
}

function addUrlField(url = "", editable = true) {
    const urlList = document.getElementById("allowed-urls-list");
    const li = document.createElement("li");
    li.innerHTML = `
        <input type="text" class="form-control" value="${url}" ${editable ? '' : 'disabled'}>
        <button onclick="removeUrlField(this)">Удалить</button>
    `;
    urlList.appendChild(li);

    if (!url) {
        const input = li.querySelector('input');
        input.disabled = false;
        input.focus();
    }
}

function removeUrlField(button) {
    const li = button.parentElement;
    li.remove();
}

async function saveClient() {
    const newName = document.getElementById("client-name-input").value;
    const newBaseUrl = document.getElementById("client-base-url-input").value;
    const newClientType = document.getElementById("client-type-select").value;

    const urlInputs = document.querySelectorAll("#allowed-urls-list input");
    const newAllowedUrls = Array.from(urlInputs).map(input => input.value.trim()).filter(url => url);

    const requestData = {
        name: newName,
        base_url: newBaseUrl,
        allowed_redirect_urls: newAllowedUrls,
        type: parseInt(newClientType, 10)
    };

    try {
        let response;
        const params = new URLSearchParams(window.location.search);
        let clientId = params.get("clientId");

        if (isCreateMode || !clientId) {
            response = await fetch("/api/client", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(requestData)
            });

            if (response.ok) {
                const newClient = await response.json();
                window.history.replaceState({}, "", `?clientId=${newClient.client_id}`);
                clientId = newClient.client_id;
                isCreateMode = false;
                document.body.classList.remove('create-mode');
            }
        } else {
            response = await fetch(`/api/client/${clientId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(requestData)
            });
        }

        if (!response.ok) {
            throw new Error(`Ошибка сохранения: статус ${response.status}`);
        }

        alert(isCreateMode ? "Клиент успешно создан!" : "Данные клиента успешно обновлены!");

        if (isCreateMode) {
            const newClient = await response.json();
            initialClientData = newClient;
            renderClientInfo(newClient);
            disableClientEditing();
        } else {
            disableClientEditing();
            const clientData = await fetchClientData(clientId);
            if (clientData) {
                renderClientInfo(clientData);
            }
        }
    } catch (error) {
        console.error(error);
        alert(`Ошибка ${isCreateMode ? 'создания' : 'обновления'} данных клиента: ${error.message}`);
    }
}

function disableClientEditing() {
    document.getElementById("client-name-input").disabled = true;
    document.getElementById("client-base-url-input").disabled = true;
    document.getElementById("client-type-select").disabled = true;
    document.querySelector(".add-url-btn").classList.add("hidden");
    document.getElementById("save-client-btn").classList.add("hidden");
    document.getElementById("edit-icon").classList.remove("hidden");

    const urlInputs = document.querySelectorAll("#allowed-urls-list input");
    urlInputs.forEach(input => input.disabled = true);
}