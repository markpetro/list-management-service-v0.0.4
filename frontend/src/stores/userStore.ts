import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
    state: () => ({
        user: null,
        token: null,
    }),
    actions: {
        setUser(user: any) {
            this.user = user;
        },
        setToken(token: string) {
            this.token = token;
        },
        logout() {
            this.user = null;
            this.token = null;
        },
    },
});