<template>
  <div>
    <!-- <NavBar /> -->
    <NavBar1 />
    <DashBoard />
  </div>
</template>

<script setup>
// import NavBar from "@/components/NavBar.vue";
// import "bootstrap/dist/css/bootstrap.css";
import NavBar1 from "@/components/NavBar1.vue";
import DashBoard from "@/components/DashBoard.vue";
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

<style lang="scss" scoped></style>
