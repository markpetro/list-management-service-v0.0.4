<template>
  <div class="login-page">
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username">Username</label>
        <input v-model="username" id="username" placeholder="Enter username" required />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input v-model="password" type="password" id="password" placeholder="Enter password" required />
      </div>
      <button type="submit">Login</button>
    </form>

    <!-- Display error message if login fails -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
import { login } from '../services/authService';

export default defineComponent({
  setup() {
    const username = ref('');
    const password = ref('');
    const error = ref<string | null>(null);
    const router = useRouter();

    const handleLogin = async () => {
      error.value = null;
      try {
        const response = await login(username.value, password.value);
        console.log('Login successful:', response);
        router.push('/dashboard');
      } catch (err: any) {
        console.error('Login failed:', err.message || err);  // Log error details
        error.value = err.message || 'Invalid username or password';
      }
    };

    return {
      username,
      password,
      error,
      handleLogin,
    };
  },
});
</script>

<style scoped>
.login-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.form-group {
  margin-bottom: 1rem;
}

input {
  padding: 0.5rem;
  margin-top: 0.25rem;
  width: 100%;
  max-width: 300px;
}

button {
  padding: 0.5rem 1rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

.error-message {
  margin-top: 1rem;
  color: red;
}
</style>