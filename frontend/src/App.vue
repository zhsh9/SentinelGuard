<template>
  <div id="app">
    <ToggleTheme />
    <router-view />
  </div>
  <!-- <AppFooter /> -->
</template>

<script setup>
// import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";
import { provide } from "vue";
import { useTimerStore } from "./timerStore";

const timerStore = useTimerStore();
provide("timerStore", timerStore);
</script>

<script>
import ToggleTheme from "./components/ToggleTheme.vue";

export default {
  name: "App",
  components: {
    ToggleTheme,
  },
  data() {
    return {
      transitionName: "",
    };
  },
};
</script>

<style lang="scss">
html,
body {
  height: 100%;
  margin: 0;
  padding: 0;
}

#app {
  // font-family: Avenir, Papyrus, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
}

.content-wrapper {
  flex: 1;
  overflow-y: auto;
  padding-top: 112px; /* Adjust this according to the height of your navbar */
}

.page {
  padding: 20px;
}

/* Modal */
.modal {
  --bs-modal-zindex: 2055 !important;
}

.modal-backdrop {
  position: relative; /* Modal 正常情况 */
  --bs-backdrop-opacity: 0; /* Modal 正常情况 */
  width: 0;
  height: 0;
}
</style>
