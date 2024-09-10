<template>
  <nav class="navbar">
    <ul>
      <li>
        <router-link to="/">Home</router-link>
      </li>
      <li>
        <router-link to="/dashboard">Dashboard</router-link>
      </li>
      <li>
        <router-link to="/list-management">List Management</router-link>
      </li>
      <li>
        <router-link to="/role-management">Role Management</router-link>
      </li>
    </ul>
  </nav>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'Navbar',
});
</script>

<style scoped>
.navbar {
  background-color: #333;
  padding: 1rem;
}

.navbar ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  display: flex;
}

.navbar ul li {
  margin-right: 20px;
}

.navbar ul li a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

.navbar ul li a:hover {
  text-decoration: underline;
}
</style>