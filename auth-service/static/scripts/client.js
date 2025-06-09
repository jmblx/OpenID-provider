let isCreateMode = false;
let initialClientData = null;

// Ключи для localStorage
const AVATAR_URL_KEY = clientId => `avatar_url_${clientId}`;
const AVATAR_EXPIRY_KEY = clientId => `avatar_expiry_${clientId}`;

// Парсит presigned URL и возвращает объект Date – момент, когда он истекает (с учётом -10 сек)
function parsePresignedExpiry(url) {
    try {
        const params = new URL(url).searchParams;
        const dateStr = params.get('X-Amz-Date');        // e.g. 20250609T181711Z
        const expiresSec = parseInt(params.get('X-Amz-Expires') || '0', 10);
        if (!dateStr || !expiresSec) return null;

        const year   = +dateStr.slice(0, 4);
        const month  = +dateStr.slice(4, 6) - 1;
        const day    = +dateStr.slice(6, 8);
        const hour   = +dateStr.slice(9, 11);
        const minute = +dateStr.slice(11, 13);
        const second = +dateStr.slice(13, 15);

        const baseDate = new Date(Date.UTC(year, month, day, hour, minute, second));
        baseDate.setSeconds(baseDate.getSeconds() + expiresSec - 10);
        return baseDate;
    } catch {
        return null;
    }
}

// Проверяем, нужно ли обновить avatar_url
function shouldLoadAvatar(clientId) {
    const url = localStorage.getItem(AVATAR_URL_KEY(clientId));
    const expiry = localStorage.getItem(AVATAR_EXPIRY_KEY(clientId));
    if (!url || !expiry) return true;
    const expiresAt = new Date(expiry);
    return Date.now() >= expiresAt.getTime();
}

// Сохраняем в localStorage новую ссылку и время истечения
function cacheAvatar(clientId, url) {
    const expiryDate = parsePresignedExpiry(url);
    if (expiryDate) {
        localStorage.setItem(AVATAR_URL_KEY(clientId), url);
        localStorage.setItem(AVATAR_EXPIRY_KEY(clientId), expiryDate.toISOString());
    }
}

// Получаем из cache или undefined
function getCachedAvatar(clientId) {
    return localStorage.getItem(AVATAR_URL_KEY(clientId)) || undefined;
}

document.addEventListener("DOMContentLoaded", async function () {
    const params = new URLSearchParams(window.location.search);
    const clientId = params.get("clientId");

    if (!clientId) {
        // Страница создания
        isCreateMode = true;
        document.body.classList.add('create-mode');
        document.getElementById("client-name").textContent = "Создание нового клиента";
        enableClientEditing();
        addUrlField("", true);
        return;
    }

    // Загружаем данные клиента, возможно с avatar
    const clientData = await fetchClientData(clientId);
    if (clientData) {
        initialClientData = clientData;
        renderClientInfo(clientData, clientId);
    }

    initAvatarUploadHandler(clientId);
});

// Переписанный fetchClientData:
async function fetchClientData(clientId) {
    try {
        const loadAvatar = shouldLoadAvatar(clientId);
        const url = `/api/client/${clientId}?load_avatar=${loadAvatar}`;
        const response = await fetch(url);
        if (!response.ok) throw new Error("Ошибка загрузки данных");
        const data = await response.json();

        // Если сервер вернул avatar_url — кэшируем
        if (data.avatar_url) {
            cacheAvatar(clientId, data.avatar_url);
        }

        return data;
    } catch (error) {
        console.error(error);
        alert("Не удалось загрузить данные клиента.");
        return null;
    }
}

// Рендерим информацию и ставим аватар
function renderClientInfo(clientData, clientId) {
    document.getElementById("client-name").textContent = `Клиент: ${clientData.name}`;
    document.getElementById("client-name-input").value = clientData.name;
    document.getElementById("client-base-url-input").value = clientData.base_url;
    document.getElementById("client-type-select").value = clientData.type;

    const urlList = document.getElementById("allowed-urls-list");
    urlList.innerHTML = "";
    clientData.allowed_redirect_urls.forEach(url => addUrlField(url, false));

    // Ставим аватар из cache (если есть)
    const avatarImg = document.getElementById("client-avatar");
    const cached = getCachedAvatar(clientId);
    if (cached) {
        avatarImg.src = cached;
    }
}

// Инициализируем обработчики для обновления аватарки
function initAvatarUploadHandler(clientId) {
    const editAvatarIcon = document.getElementById("edit-avatar-icon");
    const avatarInput     = document.getElementById("avatar-file-input");
    const avatarImg       = document.getElementById("client-avatar");

    editAvatarIcon.addEventListener("click", () => avatarInput.click());

    avatarInput.addEventListener("change", async () => {
        const file = avatarInput.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch(`/api/client/${clientId}/avatar`, {
                method: "POST",
                body: formData
            });
            if (!response.ok) throw new Error("Ошибка загрузки аватарки");

            const data = await response.json();
            const newUrl = data.avatar_path;
            // Обновляем cache и на странице
            cacheAvatar(clientId, newUrl);
            avatarImg.src = newUrl;
        } catch (e) {
            console.error(e);
            alert("Не удалось обновить аватарку");
        }
    });
}

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