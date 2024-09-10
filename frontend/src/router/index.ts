import { createRouter, createWebHistory } from 'vue-router';

// Import your page components
import LoginPage from '../pages/LoginPage.vue';
import DashboardPage from '../pages/DashboardPage.vue';
import ListManagementPage from '../pages/ListManagementPage.vue';
import RoleManagementPage from '../pages/RoleManagementPage.vue';
import NotFoundPage from '../pages/NotFoundPage.vue';

// Define routes
const routes = [
    {
        path: '/',
        name: 'Login',
        component: LoginPage,
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: DashboardPage,
        meta: { requiresAuth: false },  // Mark this route as requiring authentication
    },
    {
        path: '/list-management',
        name: 'ListManagement',
        component: ListManagementPage,
        meta: { requiresAuth: false },  // Protected route
    },
    {
        path: '/role-management',
        name: 'RoleManagement',
        component: RoleManagementPage,
        meta: { requiresAuth: false },  // Protected route
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: NotFoundPage,
    },
];

// Create the router instance
const router = createRouter({
    history: createWebHistory(),
    routes,
});

// Navigation guard to check for authentication
router.beforeEach((to, from, next) => {
    // Check if the route requires authentication
    if (to.meta.requiresAuth) {
        const token = localStorage.getItem('token');  // Get token from localStorage

        if (!token) {
            // If no token, redirect to login
            return next({ name: 'Login' });
        }
    }

    // If no authentication is required, or the user is authenticated, allow access
    next();
});

export default router;