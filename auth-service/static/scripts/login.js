import { getOrCreateFingerprint } from './fingerprint.js';

export function initLoginForm() {
    const loginButton = document.getElementById('loginButton');
    if (!loginButton) return;

    loginButton.addEventListener('click', handleLogin);

    async function handleLogin() {
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const fingerprint = await getOrCreateFingerprint();

        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Device-Fingerprint': fingerprint,
                },
                body: JSON.stringify({ email, password, fingerprint })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(
                    response.status === 403
                        ? 'Неправильный email или пароль'
                        : error.detail || 'Ошибка входа'
                );
            }

            handleAuthSuccess();
        } catch (error) {
            alert(error.message);
        }
    }

    function handleAuthSuccess() {
        // Параметры берутся из sessionStorage в auth-to-client.html
        window.location.href = '/pages/auth-to-client.html';
    }
}