<template>
  <div class="role-list">
    <h1>Roles</h1>
    <ul>
      <li v-for="role in roles" :key="role.id">{{ role.name }}</li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { getRoles } from '../services/roleService';

export default defineComponent({
  name: 'RoleList',
  setup() {
    const roles = ref([]);

    const fetchRoles = async () => {
      try {
        roles.value = await getRoles();
      } catch (error) {
        console.error('Failed to fetch roles:', error);
      }
    };

    onMounted(fetchRoles);

    return {
      roles,
    };
  },
});
</script>