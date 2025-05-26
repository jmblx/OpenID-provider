import { getStoredParams } from './manageParamsMod.js';

const fingerprint = localStorage.getItem('deviceFingerprint') || '';

export async function fetchWithAuth(url, options = {}) {
    const defaults = {
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-Device-Fingerprint': fingerprint,
            ...options.headers,
        },
        ...options
    };

    const response = await fetch(url, defaults);

    if (response.status === 401) {
        redirectToLogin();
        throw new Error('Unauthorized');
    }

    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.message || 'Request failed');
    }

    return response;
}

export async function loadUserData(emailElementId = 'user-email') {
    try {
        const response = await fetchWithAuth('/api/me');
        const userData = await response.json();

        if (emailElementId && document.getElementById(emailElementId)) {
            document.getElementById(emailElementId).textContent = userData.email;
        }

        return userData;
    } catch (error) {
        console.error('Error loading user data:', error);
        throw error;
    }
}

export async function loadUserAvatar(avatarElementId = 'user-avatar') {
    const avatarUrl = '/avatars/jwt/';
    const localStorageKey = 'lastAvatarUpdate';

    try {
        const lastUpdate = localStorage.getItem(localStorageKey);
        const url = lastUpdate ? `${avatarUrl}?t=${lastUpdate}` : avatarUrl;

        const response = await fetchWithAuth(url);
        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob);

        if (avatarElementId && document.getElementById(avatarElementId)) {
            document.getElementById(avatarElementId).src = imageUrl;
        }

        return imageUrl;
    } catch (error) {
        console.error('Error loading avatar:', error);
        const defaultAvatar = '/icons/defaultAvatar.svg';
        if (avatarElementId && document.getElementById(avatarElementId)) {
            document.getElementById(avatarElementId).src = defaultAvatar;
        }
        return defaultAvatar;
    }
}

function redirectToLogin() {
    const params = getStoredParams();
    const loginUrl = new URL('/pages/login.html', window.location.origin);

    Object.entries(params).forEach(([key, value]) => {
        loginUrl.searchParams.append(key, value);
    });

    window.location.href = loginUrl.toString();
}