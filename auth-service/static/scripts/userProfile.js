import {
    loadUserData,
    loadUserAvatar,
    setupReturnButton,
    openAvatarUpload
} from './profileCommon.js';

document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Загрузка данных пользователя
        await Promise.all([
            loadUserData('user-email'),
            loadUserAvatar('user-avatar')
        ]);

        // Настройка кнопки возврата
        setupReturnButton();

        // Обработчики событий
        document.getElementById('user-avatar')?.addEventListener('click', openAvatarUpload);
        document.querySelector('.edit-icon')?.addEventListener('click', openAvatarUpload);
        document.getElementById('avatar-upload')?.addEventListener('change', async () => {
            try {
                await uploadAvatar();
                alert('Avatar updated successfully!');
                await loadUserAvatar('user-avatar');
            } catch {
                alert('Failed to upload avatar');
            }
        });
    } catch (error) {
        console.error('Profile initialization error:', error);
    }
});