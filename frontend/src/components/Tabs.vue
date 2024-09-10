<template>
  <div class="tabs">
    <div class="tab-headers">
      <button
          v-for="tab in tabs"
          :key="tab.name"
          @click="selectTab(tab)"
          :class="{ active: tab.isActive }"
      >
        {{ tab.name }}
      </button>
    </div>
    <div class="tab-content">
      <slot :name="selectedTab"></slot>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  props: {
    initialTab: {
      type: String,
      default: '',
    },
  },
  setup(props, { slots }) {
    const tabs = ref(
        slots.default().map((slot: any) => ({
          name: slot.props.name,
          isActive: slot.props.name === props.initialTab,
        }))
    );

    const selectedTab = ref(props.initialTab);

    const selectTab = (tab: any) => {
      tabs.value.forEach((t: any) => (t.isActive = false));
      tab.isActive = true;
      selectedTab.value = tab.name;
    };

    return {
      tabs,
      selectedTab,
      selectTab,
    };
  },
});
</script>

<style>
.tabs {
  display: flex;
  flex-direction: column;
}
.tab-headers {
  display: flex;
}
.tab-headers button {
  margin-right: 10px;
  padding: 10px;
  cursor: pointer;
}
.tab-headers button.active {
  font-weight: bold;
}
.tab-content {
  margin-top: 20px;
}
</style>