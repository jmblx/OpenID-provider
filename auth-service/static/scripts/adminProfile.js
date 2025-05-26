import {
    loadUserData,
    loadUserAvatar,
    setupReturnButton,
    openAvatarUpload
} from './profileCommon.js';

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const userData = await loadUserData('user-email');
        document.getElementById('user-email-admin').textContent = userData.email;

        await loadUserAvatar('user-avatar');

        setupReturnButton();

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
        console.error('Admin profile initialization error:', error);
    }
});