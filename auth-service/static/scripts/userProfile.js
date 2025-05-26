import {
    setupReturnButton,
    openAvatarUpload, uploadAvatar
} from './profileCommon.js';
import {loadUserData, loadUserAvatar} from "./commonApi";

document.addEventListener('DOMContentLoaded', async () => {
    try {
        await Promise.all([
            loadUserData('user-email'),
            loadUserAvatar('user-avatar')
        ]);

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
        console.error('Profile initialization error:', error);
    }
});