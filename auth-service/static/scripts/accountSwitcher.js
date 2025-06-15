import { fetchWithAuth } from './commonApi.js';

const API = {
  AVAILABLE: '/api/available-accounts',
  DEACTIVATE: '/api/deactivate-current-account',
  ACTIVATE: '/api/activate-account',
};

/**
 * Запрашивает доступные аккаунты и возвращает { accounts, active_account_id }
 */
async function fetchAvailableAccounts() {
  const resp = await fetchWithAuth(API.AVAILABLE);
  if (!resp.ok) throw new Error('Не удалось получить список аккаунтов');
  return await resp.json();
}

/**
 * Деактивирует текущий аккаунт на сервере
 */
async function deactivateCurrent() {
  await fetchWithAuth(API.DEACTIVATE, { method: 'POST' });
}

/**
 * Активирует указанный аккаунт
 */
async function activateAccount(userId) {
  const resp = await fetchWithAuth(API.ACTIVATE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ new_active_user_id: userId })
  });
  if (!resp.ok) throw new Error('Не удалось активировать аккаунт');
}

/**
 * Рендерит переключатель аккаунтов внутри переданного контейнера.
 *
 * @param {HTMLElement} container — куда встраивать.
 * @param {Object} opts
 *   - allowAdd: boolean, показывать ли кнопку "Добавить аккаунт"
 *   - onSwitch: function(userId), колбек при выборе
 *   - onAdd: function(), колбек при нажатии "Добавить аккаунт"
 */
export async function initAccountSwitcher(container, { allowAdd = false, onSwitch, onAdd } = {}) {
  container.classList.add('account-switcher');
  container.innerHTML = `
    <img class="as-active-avatar" src="" alt="Avatar">
    <div class="as-menu"></div>
  `;

  const avatarEl = container.querySelector('.as-active-avatar');
  const menuEl   = container.querySelector('.as-menu');

  // Получаем аккаунты
  let { accounts, active_account_id } = await fetchAvailableAccounts();
  avatarEl.src = accounts[active_account_id]?.avatar_url || '/icons/defaultAvatar.svg';

  // Строим список
  menuEl.innerHTML = '';
  Object.entries(accounts).forEach(([id, info]) => {
    const item = document.createElement('div');
    item.className = 'account-item';
    if (id === active_account_id) item.classList.add('active');
    item.innerHTML = `
      <img src="${info.avatar_url}" class="item-avatar" alt="">
      <span class="item-email">${info.email}</span>
    `;
    item.addEventListener('click', async () => {
      try {
        if (container.dataset.context === 'panel') {
          // из панели сначала деактивируем, потом уходим на логин
          await deactivateCurrent();
          window.location.href = '/pages/login.html';
        } else {
          // на странице логина активируем и перезагружаем в приложение
          await activateAccount(id);
          window.location.reload();
        }
      } catch (e) {
        console.error(e);
        alert('Ошибка переключения аккаунта');
      }
    });
    menuEl.appendChild(item);
  });

  // Кнопка "Добавить"
  if (allowAdd) {
    const add = document.createElement('div');
    add.className = 'account-item add-account';
    add.innerHTML = `
      <img src="/icons/addAccount.svg" class="item-avatar" alt="+">
      <span class="item-email">Добавить аккаунт</span>
    `;
    add.addEventListener('click', onAdd || (() => window.location.href = '/pages/login.html'));
    menuEl.appendChild(add);
  }

  // Поведение меню
  avatarEl.addEventListener('click', e => {
    menuEl.classList.toggle('open');
  });
  document.addEventListener('click', e => {
    if (!container.contains(e.target)) menuEl.classList.remove('open');
  });
}
