import api from './api';  // Import Axios instance

// Fetch the list of roles
export const getRoles = async () => {
    try {
        const response = await api.get('/roles');
        return response.data;
    } catch (error: any) {
        console.error('Failed to fetch roles:', error.response ? error.response.data : error.message);
        throw new Error('Failed to fetch roles.');
    }
};

// Add a new role
export const addRole = async (role: string) => {
    try {
        const response = await api.post('/roles', { role });
        return response.data;
    } catch (error: any) {
        console.error('Failed to add role:', error.response ? error.response.data : error.message);
        throw new Error('Failed to add role.');
    }
};

// Update an existing role
export const updateRole = async (id: number, role: string) => {
    try {
        const response = await api.put(`/roles/${id}`, { role });
        return response.data;
    } catch (error: any) {
        console.error('Failed to update role:', error.response ? error.response.data : error.message);
        throw new Error('Failed to update role.');
    }
};

// Delete a role
export const deleteRole = async (id: number) => {
    try {
        await api.delete(`/roles/${id}`);
    } catch (error: any) {
        console.error('Failed to delete role:', error.response ? error.response.data : error.message);
        throw new Error('Failed to delete role.');
    }
};