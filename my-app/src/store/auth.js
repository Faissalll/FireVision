import { reactive } from 'vue';

export const auth = reactive({
    user: JSON.parse(localStorage.getItem('user')) || null,

    login(userData) {
        this.user = userData;
        localStorage.setItem('user', JSON.stringify(userData));
    },

    logout() {
        this.user = null;
        localStorage.removeItem('user');
    }
});
