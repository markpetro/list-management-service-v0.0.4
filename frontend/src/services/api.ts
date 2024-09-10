// api.ts
import axios from 'axios';

// Create an Axios instance with base URL and default settings
const api = axios.create({
    baseURL: 'http://localhost:8000/api', // Ensure this matches your backend URL
    headers: {
        'Content-Type': 'application/json',
    },
});

// Automatically include the JWT token in every request's header
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        // Handle request error here
        return Promise.reject(error);
    }
);

// Handle responses and errors globally
api.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        // Log the error for debugging purposes
        console.error('API response error:', error);

        // Optionally handle specific status codes
        if (error.response && error.response.status === 401) {
            // Handle unauthorized access, e.g., redirect to login page or show a message
            alert('Session expired. Please log in again.');
            localStorage.removeItem('token');
            window.location.href = '/login'; // Adjust the URL based on your routing
        }

        return Promise.reject(error);
    }
);

export default api;