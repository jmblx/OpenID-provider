import { fetchWithAuth, loadUserAvatar } from './commonApi.js';
import { getStoredParams, saveInitialQueryParams } from './manageParamsMod.js';
import { logoutClient } from "./commonApi.js";

export async function initAuthToClient() {
    try {
        saveInitialQueryParams();
        const params = getStoredParams();
        const fingerprint = localStorage.getItem('deviceFingerprint') || '';

        await loadUserData();

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
            client_id: parseInt(params.client_id),
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

    // Настройка перехода в профиль
    document.getElementById('profile-link').addEventListener('click', goToProfilePage);
    document.querySelector('.gear-icon').addEventListener('click', (e) => {
        e.stopPropagation();
        goToProfilePage();
    });
}

function addResourceItem(container, title, content) {
    const item = document.createElement('li');
    item.className = 'list-group-item permission-item';
    item.innerHTML = `<strong>${title}</strong> ${content}`;
    container.appendChild(item);
}

function goToProfilePage() {
    const profileUrl = new URL('/pages/profile.html', window.location.origin);

    if (!profileUrl.searchParams.has('client_name')) {
        const clientName = document.getElementById('client-name').textContent;
        profileUrl.searchParams.append('client_name', clientName);
    }

    window.location.href = profileUrl.toString();
}

function handleAuthError(error) {
    console.error('Authorization error:', error);

    let errorMessage = 'Произошла ошибка авторизации';
    if (error.message.includes('is not a valid redirect URL')) {
        const invalidUrl = error.message.split('is not a valid redirect URL')[0].trim();
        errorMessage = `Недопустимый URL для перенаправления: ${invalidUrl}`;
    } else if (error.message !== 'Authorization failed') {
        errorMessage = error.message;
    }

    alert(errorMessage);
}

document.addEventListener('DOMContentLoaded', initAuthToClient);

document.getElementById("logout-button")?.addEventListener("click", logoutClient);
