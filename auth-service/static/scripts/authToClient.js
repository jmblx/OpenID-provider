// authToClient.js

import { fetchWithAuth, loadUserAvatar } from './commonApi.js';
import { getStoredParams } from './manageParamsMod.js';
import { logoutClient } from "./commonApi.js";

// Вспомогательная функция для парсинга expiry из presigned URL
function getPresignedExpiry(url) {
    try {
        const params = new URL(url).searchParams;
        const dateStr = params.get('X-Amz-Date');       // e.g. "20250609T181711Z"
        const expires = parseInt(params.get('X-Amz-Expires') || '0', 10);
        if (!dateStr || !expires) return null;

        const year  = +dateStr.slice(0, 4);
        const month = +dateStr.slice(4, 6) - 1;
        const day   = +dateStr.slice(6, 8);
        const hour  = +dateStr.slice(9, 11);
        const min   = +dateStr.slice(11, 13);
        const sec   = +dateStr.slice(13, 15);

        const dt = new Date(Date.UTC(year, month, day, hour, min, sec));
        dt.setSeconds(dt.getSeconds() + expires - 10);
        return dt;
    } catch {
        return null;
    }
}

// Загружает и кэширует presigned avatar_url клиента
async function loadClientAvatar(imgElementId = 'client-avatar') {
    const params = getStoredParams();
    const clientId = params.client_id;
    if (!clientId) return;
    const storageKey = `clientAvatar:${clientId}`;

    // Проверяем в localStorage
    let cached = null;
    try {
        const raw = localStorage.getItem(storageKey);
        if (raw) {
            cached = JSON.parse(raw);
            const expiresAt = new Date(cached.expires_at);
            if (expiresAt > new Date()) {
                document.getElementById(imgElementId).src = cached.avatar_url;
                return;
            }
        }
    } catch {
        // парсинг не удался — сбросим кеш
    }

    // Нужно получить новую ссылку
    try {
        const response = await fetchWithAuth(`/api/client/${clientId}/avatar`);
        if (!response.ok) throw new Error('Ошибка загрузки аватарки клиента');
        const data = await response.json();
        const avatarUrl = data.avatar_url;
        const expiresAt = getPresignedExpiry(avatarUrl);
        if (expiresAt) {
            localStorage.setItem(storageKey, JSON.stringify({
                avatar_url: avatarUrl,
                expires_at: expiresAt.toISOString()
            }));
        }
        document.getElementById(imgElementId).src = avatarUrl;
    } catch (e) {
        console.error(e);
        // При ошибке можно оставить дефолт или ничего не показывать
    }
}

export async function initAuthToClient() {
    try {
        const params = getStoredParams();
        const fingerprint = localStorage.getItem('deviceFingerprint') || '';

        // Сначала загружаем данные пользователя и клиента
        await loadUserData();
        await loadClientAvatar('client-avatar');

        const authData = await authorizeClient(params, fingerprint);
        setupUI(authData, params);
    } catch (error) {
        handleAuthError(error);
    }
}

async function loadUserData() {
    const response = await fetchWithAuth('/api/me');
    const userData = await response.json();
    document.getElementById('user-email').textContent = userData.email;
    await loadUserAvatar('user-avatar');
}

async function authorizeClient(params, fingerprint) {
    const response = await fetchWithAuth('/api/auth-to-client', {
        method: 'POST',
        body: JSON.stringify({
            client_id: parseInt(params.client_id, 10),
            required_resources: JSON.parse(params.required_resources),
            redirect_url: params.redirect_url,
            code_verifier: params.code_verifier,
            code_challenge_method: params.code_challenge_method,
            fingerprint
        })
    });
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData?.error?.title || 'Authorization failed');
    }
    return await response.json();
}

function setupUI(authData, params) {
    document.getElementById('client-name').textContent = authData.client_name;

    const resourcesContainer = document.getElementById('requested-resources');
    const parsedResources = JSON.parse(params.required_resources);

    if (parsedResources.user_data_needed?.length) {
        addResourceItem(resourcesContainer,
            'Требуемые данные:',
            parsedResources.user_data_needed.join(', '));
    }
    if (authData.rs_names) {
        const rsNames = Object.values(authData.rs_names).map(rs => rs.name);
        if (rsNames.length) {
            addResourceItem(resourcesContainer,
                'Ресурсные серверы:',
                rsNames.join(', '));
        }
    }

    document.getElementById('authorize-button').addEventListener('click', () => {
        if (document.getElementById('permission-checkbox').checked) {
            const redirectUrl = new URL(authData.redirect_url);
            redirectUrl.searchParams.append('auth_code', authData.auth_code);
            window.location.href = redirectUrl.toString();
        } else {
            alert('Please allow access to requested resources.');
        }
    });

    document.getElementById('profile-link').addEventListener('click', goToProfilePage);
    document.querySelector('.gear-icon').addEventListener('click', e => {
        e.stopPropagation();
        goToProfilePage();
    });
}

function addResourceItem(container, title, content) {
    const li = document.createElement('li');
    li.className = 'list-group-item permission-item';
    li.innerHTML = `<strong>${title}</strong> ${content}`;
    container.appendChild(li);
}

function goToProfilePage() {
    const profileUrl = new URL('/pages/profile.html', window.location.origin);
    if (!profileUrl.searchParams.has('client_name')) {
        profileUrl.searchParams.append(
            'client_name',
            document.getElementById('client-name').textContent
        );
    }
    window.location.href = profileUrl.toString();
}

function handleAuthError(error) {
    console.error('Authorization error:', error);
    let message = 'Произошла ошибка авторизации';
    if (error.message.includes('is not a valid redirect URL')) {
        const invalidUrl = error.message.split('is not a valid redirect URL')[0].trim();
        message = `Недопустимый URL для перенаправления: ${invalidUrl}`;
    } else if (error.message !== 'Authorization failed') {
        message = error.message;
    }
    alert(message);
}

document.addEventListener('DOMContentLoaded', initAuthToClient);
document.getElementById("logout-button")?.addEventListener("click", logoutClient);
