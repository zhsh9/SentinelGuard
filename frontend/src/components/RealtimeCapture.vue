<template>
  <!-- Represents a dropdown menu for real-time capture functionality. -->
  <li class="nav-item dropdown">
    <a
      class="nav-link dropdown-toggle"
      data-bs-toggle="dropdown"
      href="#"
      role="button"
      aria-haspopup="true"
      aria-expanded="false"
      >Real-time Capture</a
    >
    <div class="dropdown-menu">
      <a
        class="dropdown-item"
        href="#"
        data-bs-toggle="modal"
        data-bs-target="#startCaptureModal"
        >Start Capturing</a
      >
      <a
        class="dropdown-item"
        href="#"
        data-bs-toggle="modal"
        data-bs-target="#stopCaptureModal"
        >Stop Capturing</a
      >
    </div>
  </li>
  <!-- Start capturing modal -->
  <StartSniffModal />
  <!-- Stop capturing modal -->
  <StopSniffModal />
</template>

<script setup>
import StartSniffModal from "./StartSniffModal.vue";
import StopSniffModal from "./StopSniffModal.vue";
</script>

<style lang="scss" scoped>
.nav-link {
  color: white;
  font-weight: bold;
  width: auto;

  &:hover {
    color: darken(#a2e5d2, 10%);
    text-decoration: underline;
  }
}

// drop-down menu
.dropdown-menu.show {
  margin-top: 12px;
  margin-left: 6px;
  width: auto + 20px;
}
</style>
