import { defineStore } from 'pinia';

// Defining the main store
export const useMainStore = defineStore('main', {
    state: () => ({
        count: 0,
    }),
    actions: {
        increment() {
            this.count++;
        }
    }
});