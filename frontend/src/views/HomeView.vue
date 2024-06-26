<template>
  <div class="layout">
    <!-- <NavBar /> -->
    <NavBar1 class="navbar" />
    <DashBoard class="dashboard" />
    <AppFooter class="footer" />
  </div>
</template>

<script setup>
// import NavBar from "@/components/NavBar.vue";
// import "bootstrap/dist/css/bootstrap.css";
import AppFooter from "@/components/AppFooter.vue";
import DashBoard from "@/components/DashBoard.vue";
import NavBar1 from "@/components/NavBar1.vue";
</script>

<script>
export default {
  name: "HomeView",
  setup() {
    return {};
  },
  data() {
    return {};
  },
  methods: {},
  created() {},
};
</script>

<style scoped>
html,
body,
.layout {
  height: 100%;
  margin: 0;
  display: flex;
  flex-direction: column;
}

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px; /* Adjust height as needed */
  z-index: 1000;
}

.dashboard {
  flex: 1;
  margin-top: 60px; /* Same as navbar height */
  margin-bottom: 60px; /* Same as footer height */
  overflow-y: auto;
}

.footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60px; /* Adjust height as needed */
  z-index: 1000;
}
</style>
