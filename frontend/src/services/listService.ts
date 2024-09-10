// listfront/src/services/listService.ts
import api from './api';  // Axios instance

// Fetch the list of items
export const getListItems = async () => {
    try {
        const response = await api.get('/lists');
        return response.data;
    } catch (error) {
        throw new Error('Failed to fetch list items.');
    }
};

// Add a new item to the list
export const addListItem = async (item: string) => {
    try {
        const response = await api.post('/lists', { item });
        return response.data;
    } catch (error) {
        throw new Error('Failed to add list item.');
    }
};

// Update an existing item in the list
export const updateListItem = async (id: number, item: string) => {
    try {
        const response = await api.put(`/lists/${id}`, { item });
        return response.data;
    } catch (error) {
        throw new Error('Failed to update list item.');
    }
};

// Delete an item from the list
export const deleteListItem = async (id: number) => {
    try {
        await api.delete(`/lists/${id}`);
    } catch (error) {
        throw new Error('Failed to delete list item.');
    }
};