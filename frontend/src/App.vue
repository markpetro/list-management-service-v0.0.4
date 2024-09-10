<template>
  <div id="app">
    <!-- Navbar will go here (optional) -->
    <Navbar />

    <!-- Main content will be rendered here by Vue Router -->
    <router-view />
  </div>
</template>

<script setup lang="ts">
// Import the Navbar component (optional)
import Navbar from './components/Navbar.vue';
</script>

<style scoped>
/* Basic styling for the app layout */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>