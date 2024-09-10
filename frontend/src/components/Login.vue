<template>
  <div>
    <form @submit.prevent="handleLogin">
      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { login } from '../services/authService';

export default defineComponent({
  setup() {
    const username = ref('');
    const password = ref('');

    const handleLogin = async () => {
      try {
        const result = await login(username.value, password.value);
        console.log('Login success:', result);
      } catch (error) {
        console.error('Login failed:', error);
      }
    };

    return {
      username,
      password,
      handleLogin,
    };
  },
});
</script>