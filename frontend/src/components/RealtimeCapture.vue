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
  <div
    class="modal fade"
    id="startCaptureModal"
    data-bs-backdrop="static"
    data-bs-keyboard="false"
    tabindex="-1"
    aria-labelledby="startCaptureModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="startCaptureModal">Start Capturing</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <p>Are you sure you really want to start capturing http traffic?</p>
          <p>Other info: db_name, username, time, ...</p>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button type="button" class="btn btn-primary" @click="confirmLogout">
            Start
          </button>
        </div>
      </div>
    </div>
  </div>
  <!-- Stop capturing modal -->
  <div
    class="modal fade"
    id="stopCaptureModal"
    data-bs-backdrop="static"
    data-bs-keyboard="false"
    tabindex="-1"
    aria-labelledby="stopCaptureModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="stopCaptureModalLabel">
            Logout Confirmation
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <p>Are you sure you really want to logout?</p>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button type="button" class="btn btn-primary" @click="confirmLogout">
            Stop
          </button>
        </div>
      </div>
    </div>
  </div>
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
