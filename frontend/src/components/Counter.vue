<template>
  <div>
    <p>Count is: {{ count }}</p>
    <button @click="increment">Increment</button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useMainStore } from '../store';

export default defineComponent({
  setup() {
    const store = useMainStore();
    return {
      count: store.count,
      increment: store.increment,
    };
  },
});
</script>