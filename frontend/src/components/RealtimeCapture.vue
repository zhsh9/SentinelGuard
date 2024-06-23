<template>
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
      <a class="dropdown-item" href="#">Start Capturing</a>
      <a class="dropdown-item" href="#">Stop Capturing</a>
    </div>
  </li>
</template>

<script>
export default {
  name: "UploadPcap",
};
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

.navbar-toggler {
  border: none;
  &:focus {
    outline: none;
    box-shadow: none;
  }
}

// drop-down menu
.dropdown-menu.show {
  margin-top: 12px;
  margin-left: 3px;
  width: auto + 20px;
  border-radius: 0;
}
</style>
