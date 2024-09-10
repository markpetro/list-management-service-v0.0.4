<template>
  <div class="dashboard-page">
    <h1>Welcome to your Dashboard</h1>
    <p>This is a secure area that requires authentication.</p>

    <!-- Add your dashboard content here, e.g., widgets, charts, etc. -->
    <div class="content">
      <!-- Placeholder content for now -->
      <p>Manage your lists, roles, and more!</p>
    </div>

    <button @click="logout">Logout</button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
  setup() {
    const router = useRouter();

    // Function to handle logout
    const logout = () => {
      // Remove the token from localStorage
      localStorage.removeItem('token');

      // Redirect to the login page
      router.push('/login');
    };

    return {
      logout,
    };
  },
});
</script>

<style scoped>
.dashboard-page {
  text-align: center;
  margin-top: 50px;
}

.content {
  margin: 20px 0;
}

button {
  padding: 10px 20px;
  background-color: #f44336;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #e53935;
}
</style>