<template>
  <div class="role-management-page">
    <h1>Role Management</h1>

    <!-- Add New Role -->
    <div class="form-group">
      <input v-model="newRole" placeholder="Enter new role" />
      <button @click="addRole">Add Role</button>
    </div>

    <!-- Display List of Roles -->
    <ul>
      <li v-for="(role, index) in roles" :key="role.id">
        {{ role.name }}
        <button @click="editRole(role.id, role.name)">Edit</button>
        <button @click="deleteRole(role.id)">Delete</button>
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
import { getRoles, addRole, updateRole, deleteRole } from '../services/roleService';

export default defineComponent({
  setup() {
    const newRole = ref('');  // Input for new role
    const roles = ref<{ id: number; name: string }[]>([]);  // List of roles
    const error = ref<string | null>(null);  // Error message

    // Fetch roles on page load
    const fetchRoles = async () => {
      try {
        roles.value = await getRoles();
      } catch (err) {
        error.value = 'Failed to fetch roles.';
      }
    };

    // Function to add a new role
    const addRole = async () => {
      try {
        if (newRole.value.trim() === '') {
          error.value = 'Role cannot be empty';
          return;
        }
        const newRoleData = await addRole(newRole.value);
        roles.value.push(newRoleData);  // Update the list with the new role
        newRole.value = '';  // Clear input
        error.value = null;  // Clear error message
      } catch (err) {
        error.value = 'Failed to add role.';
      }
    };

    // Function to edit a role
    const editRole = async (id: number, currentName: string) => {
      const editedRole = prompt('Edit role:', currentName);
      if (editedRole) {
        try {
          const updatedRole = await updateRole(id, editedRole);
          const roleIndex = roles.value.findIndex((role) => role.id === id);
          if (roleIndex !== -1) {
            roles.value[roleIndex] = updatedRole;  // Update the list
          }
        } catch (err) {
          error.value = 'Failed to update role.';
        }
      }
    };

    // Function to delete a role
    const deleteRole = async (id: number) => {
      try {
        await deleteRole(id);
        roles.value = roles.value.filter((role) => role.id !== id);  // Remove from list
      } catch (err) {
        error.value = 'Failed to delete role.';
      }
    };

    // Fetch roles on component mount
    onMounted(fetchRoles);

    return {
      newRole,
      roles,
      error,
      addRole,
      editRole,
      deleteRole,
    };
  },
});
</script>

<style scoped>
.role-management-page {
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