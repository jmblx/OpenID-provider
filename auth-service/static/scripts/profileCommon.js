import { getStoredParams } from './manageParamsMod.js';
import {fetchWithAuth, loadUserData, loadUserAvatar, logoutClient} from './commonApi.js';

export async function uploadUserAvatar() {
    const fileInput = document.getElementById('avatar-upload');
    if (!fileInput?.files?.length) return false;

    try {
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        await fetchWithAuth('/api/avatar', {
            method: 'POST',
            body: formData
        });
        await loadUserAvatar()

        return true;
    } catch (error) {
        console.error('Error uploading avatar:', error);
        throw error;
    }
}

export function setupReturnButton() {
    const params = getStoredParams();
    const returnButton = document.getElementById('return-button');
    if (!returnButton) return;

    const requiredParams = ['client_id', 'required_resources', 'redirect_url'];
    const hasAuthParams = requiredParams.every(param => params[param]);

    if (!hasAuthParams) {
        returnButton.classList.add('hidden');
        return;
    }

    returnButton.textContent = `<- Authorize on ${params.client_name || 'Client'}`;
    returnButton.addEventListener('click', () => {
        const redirectUrl = new URL('/pages/auth-to-client.html', window.location.origin);
        Object.entries(params).forEach(([key, value]) => {
            if (key !== 'client_name') {
                redirectUrl.searchParams.append(key, value);
            }
        });
        window.location.href = redirectUrl.toString();
    });
}

export function openAvatarUpload() {
    document.getElementById('avatar-upload')?.click();
}