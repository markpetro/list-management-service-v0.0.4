import axios from 'axios';

// Create an axios instance with the base URL and default header settings
const api = axios.create({
    baseURL: 'http://localhost:8000',  // Ensure this matches your backend URL
    headers: {
        'Content-Type': 'application/json',
    },
});

// Interface for the login response
interface LoginResponse {
    access_token: string;
    token_type: string;
}

// Login function: sends a POST request to the backend with the provided username and password
export const login = async (username: string, password: string): Promise<LoginResponse> => {
    try {
        const response = await api.post<LoginResponse>('/auth/login', { username, password });
        const token = response.data.access_token;

        // Store the token in local storage
        localStorage.setItem('token', token);

        // Return the received data (token and token type)
        return response.data;
    } catch (error: any) {
        // Log the error for debugging purposes
        const errorMessage = error.response ? error.response.data.detail : error.message;
        console.error('Login error:', errorMessage);

        // Throw an error with a user-friendly message
        throw new Error('Failed to login. Please check your credentials.');
    }
};