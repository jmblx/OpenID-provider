import { initYandexAuth } from './yandexAuth.js';
import { initLoginForm } from './login.js';
import { initPasswordReset } from './passwordReset.js';
import { saveInitialQueryParams } from './manageParamsMod.js';

document.addEventListener('DOMContentLoaded', async () => {
    saveInitialQueryParams();

    initYandexAuth({
        clientId: '83c64ffbf6db4ea282b7e4d0c5cfbb51',
        redirectUri: 'https://menoitami.ru/pages/yandex-login.html',
        authType: 'login'
    });
    initLoginForm();
    initPasswordReset();
});