<template>
  <div class="not-found-page">
    <h1>404 - Page Not Found</h1>
    <p>The page you are looking for does not exist.</p>
    <router-link to="/">Go back to home</router-link>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'NotFoundPage',
});
</script>

<style scoped>
.not-found-page {
  text-align: center;
  margin-top: 100px;
}

.not-found-page h1 {
  font-size: 2.5rem;
  margin-bottom: 20px;
}

.not-found-page p {
  font-size: 1.25rem;
}

router-link {
  color: #42b983;
  font-weight: bold;
  text-decoration: none;
}

router-link:hover {
  text-decoration: underline;
}
</style>