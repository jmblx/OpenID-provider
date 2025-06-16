import { getStoredParams } from './manageParamsMod.js';

const fingerprint = localStorage.getItem('deviceFingerprint') || '';

export async function fetchWithAuth(url, options = {}) {
    const defaults = {
        credentials: 'include',
        headers: {
            'X-Device-Fingerprint': fingerprint,
        }
    };

    if (!(options.body instanceof FormData)) {
        defaults.headers['Content-Type'] = 'application/json';
    }

    const mergedOptions = {
        ...defaults,
        ...options,
        headers: {
            ...defaults.headers,
            ...options.headers,
        }
    };

    let response = await fetch(url, mergedOptions);

    if (response.status === 401) {
        const refreshResponse = await fetch("/api/auth-service/refresh", {
            credentials: 'include',
            headers: {
                'X-Device-Fingerprint': fingerprint,
            }
        });

        if (refreshResponse.ok) {
            response = await fetch(url, mergedOptions);
        } else {
            redirectToLogin();
            throw new Error('Unauthorized - refresh failed');
        }
    }

    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.message || error.detail || 'Request failed');
    }

    return response;
}


window.cachedUserDataPromise = window.cachedUserDataPromise || null;

export async function loadUserData(emailElementId = 'user-email') {
  if (!window.cachedUserDataPromise) {
    window.cachedUserDataPromise = fetchWithAuth('/api/me')
      .then(response => response.json())
      .catch(err => {
        window.cachedUserDataPromise = null;
        throw err;
      });
  }

  const userData = await window.cachedUserDataPromise;

  if (emailElementId) {
    const el = document.getElementById(emailElementId);
    if (el) {
      el.textContent = userData.email;
    }
  }

  return userData;
}


export async function loadUserAvatar(avatarElementId = 'user-avatar') {
    const avatarUrl = '/user-avatars/jwt/';

    try {
        const userData = await window.cachedUserDataPromise;
        const lastUpdate = userData.avatar_update_timestamp;
        const url = lastUpdate ? `${avatarUrl}?t=${lastUpdate}` : `${avatarUrl}?t=${Math.floor(Date.now() / 1000)}`;

        const response = await fetchWithAuth(url);
        window.cachedUserDataPromise.avatar_update_timestamp = response.avatar_update_timestamp
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

export function redirectToLogin() {
    const params = getStoredParams();
    const loginUrl = new URL('/pages/login.html', window.location.origin);

    Object.entries(params).forEach(([key, value]) => {
        loginUrl.searchParams.append(key, value);
    });

    window.location.href = loginUrl.toString();
}

export async function logoutClient() {
    try {
        const response = await fetch("/api/auth-service/revoke", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (response.ok) {
            redirectToLogin();
        } else {
            const data = await response.json();
            alert(data.detail || "Logout failed");
        }
    } catch (error) {
        console.error("Logout error:", error);
        alert("Network error during logout");
    }
}

