import { getOrCreateFingerprint } from './auth/fingerprint.js';
import { initYandexAuth } from './auth/yandexAuth.js';
import { saveInitialQueryParams } from './manageParamsMod.js';

document.addEventListener('DOMContentLoaded', async () => {
    const fingerprint = await getOrCreateFingerprint();

    saveInitialQueryParams();

    initYandexAuth({
        clientId: '83c64ffbf6db4ea282b7e4d0c5cfbb51',
        redirectUri: 'https://menoitami.ru/pages/yandex-login.html',
        authType: 'register'
    });

    document.getElementById('registerButton').addEventListener('click', handleRegister);
});

async function handleRegister() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const fingerprint = await getOrCreateFingerprint();

    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Device-Fingerprint': fingerprint,
            },
            body: JSON.stringify({ email, password, fingerprint })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Registration failed');
        }

        window.location.href = '/pages/auth-to-client.html';
    } catch (error) {
        alert(error.message);
    }
}