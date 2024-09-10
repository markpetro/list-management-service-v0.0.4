<template>
  <div>
    <h2>{{ msg }}</h2>
    <button @click="changeMessage">Change Message</button>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  props: {
    msg: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const message = ref(props.msg);

    const changeMessage = () => {
      message.value = "Message has been updated!";
    };

    return {
      message,
      changeMessage,
    };
  },
});
</script>