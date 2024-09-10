// Importing necessary libraries and components
import { createApp } from 'vue';  // The main function to create a Vue app instance
import App from './App.vue';      // The root component where the entire app starts
import router from './router';    // Vue Router configuration for navigating between pages
import { createPinia } from 'pinia';  // Pinia store for global state management

// Create the Vue app instance
const app = createApp(App);

// Use Vue Router to handle page navigation
app.use(router);

// Use Pinia for state management across components
app.use(createPinia());

// Mount the app to the #app element in index.html
app.mount('#app');