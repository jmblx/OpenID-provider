import { initAccountSwitcher } from './accountSwitcher.js';

document.addEventListener('DOMContentLoaded', async () => {
  const mount = document.querySelector('.login-account-switcher');
  if (!mount) return;

  // context не равен 'panel' — поэтому allowAdd=false по умолчанию
  await initAccountSwitcher(mount, { allowAdd: false });
});