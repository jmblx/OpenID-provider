import { initYandexAuth } from './yandexAuth.js';
import { initLoginForm } from './login.js';
import { initPasswordReset } from './passwordReset.js';
import { saveInitialQueryParams } from './manageParamsMod.js';

document.addEventListener('DOMContentLoaded', async () => {
    saveInitialQueryParams();

    initYandexAuth('83c64ffbf6db4ea282b7e4d0c5cfbb51', 'https://menoitami.ru/pages/yandex-login.html');
    initLoginForm();
    initPasswordReset();

    const registerLink = document.getElementById('register-link');
    if (registerLink) {
        registerLink.href = '/pages/register.html';
    }
});