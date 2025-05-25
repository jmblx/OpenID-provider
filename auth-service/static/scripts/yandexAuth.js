import { getOrCreateFingerprint } from './fingerprint.js';

export function initYandexAuth({ clientId, redirectUri, authType = 'login' }) {
    const button = document.getElementById('yandexAuthBtn');
    if (!button) return;

    button.addEventListener('click', handleYandexAuth);

    async function handleYandexAuth() {
        try {
            const data = await YaAuthSuggest.init(
                {
                    client_id: clientId,
                    response_type: 'token',
                    redirect_uri: redirectUri
                },
                window.location.origin
            ).then(({ handler }) => handler());

            await sendYandexTokenToServer(data.access_token, authType);
        } catch (error) {
            console.error('Yandex auth error:', error);
            alert(error.type === 'access_denied'
                ? 'Вы отменили авторизацию'
                : 'Ошибка авторизации через Яндекс');
        }
    }

    async function sendYandexTokenToServer(token, authType) {
        const fingerprint = await getOrCreateFingerprint();
        const endpoint = authType === 'login' ? '/api/login/yandex' : '/api/register/yandex';

        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Device-Fingerprint': fingerprint,
            },
            body: JSON.stringify({ yandex_token: token, fingerprint })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Auth failed');
        }

        return handleAuthSuccess();
    }

    function handleAuthSuccess() {
        window.location.href = '/pages/auth-to-client.html';
    }
}