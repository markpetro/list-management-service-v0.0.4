<template>
  <div class="list-management-page">
    <h1>List Management</h1>

    <!-- Add New List Item -->
    <div class="form-group">
      <input v-model="newItem" placeholder="Enter new list item" />
      <button @click="addItem">Add Item</button>
    </div>

    <!-- Display List Items -->
    <ul>
      <li v-for="(item, index) in items" :key="item.id">
        {{ item.name }}
        <button @click="editItem(item.id, item.name)">Edit</button>
        <button @click="deleteItem(item.id)">Delete</button>
      </li>
    </ul>

    <!-- Error Message -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { getListItems, addListItem, updateListItem, deleteListItem } from '../services/listService';

export default defineComponent({
  setup() {
    const newItem = ref('');  // Input for new list item
    const items = ref<{ id: number; name: string }[]>([]);  // List of items
    const error = ref<string | null>(null);  // Error message

    // Fetch list items on page load
    const fetchItems = async () => {
      try {
        items.value = await getListItems();
      } catch (err) {
        error.value = 'Failed to fetch list items.';
      }
    };

    // Function to add a new item to the list
    const addItem = async () => {
      try {
        if (newItem.value.trim() === '') {
          error.value = 'Item cannot be empty';
          return;
        }
        const newItemData = await addListItem(newItem.value);
        items.value.push(newItemData);  // Update the list with the new item
        newItem.value = '';  // Clear input
        error.value = null;  // Clear error message
      } catch (err) {
        error.value = 'Failed to add item.';
      }
    };

    // Function to edit an item
    const editItem = async (id: number, currentName: string) => {
      const editedItem = prompt('Edit item:', currentName);
      if (editedItem) {
        try {
          const updatedItem = await updateListItem(id, editedItem);
          const itemIndex = items.value.findIndex((item) => item.id === id);
          if (itemIndex !== -1) {
            items.value[itemIndex] = updatedItem;  // Update the list
          }
        } catch (err) {
          error.value = 'Failed to update item.';
        }
      }
    };

    // Function to delete an item
    const deleteItem = async (id: number) => {
      try {
        await deleteListItem(id);
        items.value = items.value.filter((item) => item.id !== id);  // Remove from list
      } catch (err) {
        error.value = 'Failed to delete item.';
      }
    };

    // Fetch items on component mount
    onMounted(fetchItems);

    return {
      newItem,
      items,
      error,
      addItem,
      editItem,
      deleteItem,
    };
  },
});
</script>

<style scoped>
.list-management-page {
  margin: 20px;
}

.form-group {
  margin-bottom: 10px;
}

input {
  padding: 10px;
  margin-right: 10px;
}

button {
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
  margin-left: 5px;
}

button:hover {
  background-color: #45a049;
}

.error-message {
  color: red;
}
</style>