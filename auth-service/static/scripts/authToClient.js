import { fetchWithAuth, loadUserAvatar } from './commonApi.js';
import { getStoredParams, saveInitialQueryParams } from './manageParamsMod.js';

export async function initAuthToClient() {
    saveInitialQueryParams();
    const params = getStoredParams();
    const fingerprint = localStorage.getItem('deviceFingerprint') || '';

    try {
        await Promise.all([
            loadUserData(),
            initClientAuthorization(params, fingerprint)
        ]);
    } catch (error) {
        handleAuthError(error);
    }

    setupEventListeners();
}

async function loadUserData() {
    const response = await fetchWithAuth('/api/me');
    const userData = await response.json();
    document.getElementById('user-email').textContent = userData.email;
    await loadUserAvatar('user-avatar');
}

async function initClientAuthorization(params, fingerprint) {
    const response = await fetchWithAuth('/api/auth-to-client', {
        method: 'POST',
        body: JSON.stringify({
            client_id: parseInt(params.client_id),
            required_resources: JSON.parse(params.required_resources),
            redirect_url: params.redirect_url,
            code_verifier: params.code_verifier,
            code_challenge_method: params.code_challenge_method
        })
    });

    const data = await response.json();
    displayClientData(data, params);
}

function displayClientData(data, params) {
    document.getElementById('client-name').textContent = data.client_name;
    const requestedResources = document.getElementById('requested-resources');
    const parsedResources = JSON.parse(params.required_resources);

    if (parsedResources.user_data_needed?.length) {
        addResourceItem(requestedResources,
            `Требуемые данные: ${parsedResources.user_data_needed.join(', ')}`);
    }

    if (data.rs_names) {
        const rsNames = Object.values(data.rs_names).map(rs => rs.name);
        if (rsNames.length) {
            addResourceItem(requestedResources,
                `Ресурсные серверы: ${rsNames.join(', ')}`);
        }
    }
}

function addResourceItem(container, text) {
    const li = document.createElement('li');
    li.classList.add('list-group-item');
    li.textContent = text;
    container.appendChild(li);
}

function setupEventListeners() {
    document.getElementById('profile-link').addEventListener('click', goToProfilePage);
    document.querySelector('.gear-icon').addEventListener('click', (e) => {
        e.stopPropagation();
        goToProfilePage();
    });

    document.getElementById('authorize-button').addEventListener('click', handleAuthorization);
}

function handleAuthorization() {
    if (!document.getElementById('permission-checkbox').checked) {
        alert('Please allow access to requested resources.');
        return;
    }

    const params = getStoredParams();
    if (params.redirect_url) {
        const redirectUrl = new URL(params.redirect_url);
        redirectUrl.searchParams.append('auth_code', params.auth_code);
        window.location.href = redirectUrl.toString();
    } else {
        alert('Error: redirect_url not found.');
    }
}

function goToProfilePage() {
    const params = getStoredParams();
    const profileUrl = new URL('/pages/profile.html', window.location.origin);

    for (const [key, value] of Object.entries(params)) {
        profileUrl.searchParams.append(key, value);
    }

    if (!profileUrl.searchParams.has('client_name')) {
        const clientName = document.getElementById('client-name')?.textContent;
        if (clientName) {
            profileUrl.searchParams.append('client_name', clientName);
        }
    }

    window.location.href = profileUrl.toString();
}

function handleAuthError(error) {
    console.error('Authorization error:', error);
    let errorMessage = 'Произошла ошибка авторизации';

    const errorData = error.data?.error || error.data;
    if (errorData?.title) {
        errorMessage = errorData.title.includes('is not a valid redirect URL')
            ? `Недопустимый URL для перенаправления: ${
                errorData.title.split('is not a valid redirect URL')[0].trim()
            }`
            : errorData.title;
    } else if (error.message && error.message !== 'Authorization failed') {
        errorMessage = error.message;
    }

    alert(errorMessage);
}

document.addEventListener('DOMContentLoaded', () => {
    initAuthToClient().catch(console.error);
});