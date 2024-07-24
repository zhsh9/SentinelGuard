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
          <p>Are you sure to start capturing http traffic?</p>
          <p>
            Current status: <span v-if="isSniffing">Sniffing</span
            ><span v-else>Not Sniffing</span>
          </p>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button type="button" class="btn btn-primary" @click="startCapture">
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
          <p>Are you sure to stop capturing http traffic?</p>
          <p>
            Current status: <span v-if="isSniffing">Sniffing</span
            ><span v-else>Not Sniffing</span>
          </p>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button type="button" class="btn btn-primary" @click="stopCapture">
            Stop
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from "vue";
import { Modal } from "bootstrap";
import axios from "axios";
import { useStore } from "vuex"; // 导入 Vuex

const store = useStore(); // 使用 Vuex
const timerStore = inject("timerStore");
const isSniffing = ref(false);

const fetchStatus = async () => {
  try {
    const response = await axios.get("/api/sniffer/status");
    isSniffing.value = response.data.sniffing;
    store.dispatch("updateIsSniffing", isSniffing.value);
  } catch (error) {
    console.error("Error fetching sniffer status:", error);
  }
};

const startCapture = async () => {
  try {
    const response = await axios.post("/api/sniffer/start", {
      interface: "eth0",
    });
    if (response.data.status === "success") {
      isSniffing.value = true;
      store.dispatch("updateIsSniffing", isSniffing.value);
      timerStore.startNewTimer();
      timerStore.startTimer();
    }
    alert(response.data.message);
    hideModal("startCaptureModal");
  } catch (error) {
    console.error("Error starting sniffer:", error);
  }
};

const stopCapture = async () => {
  try {
    const response = await axios.post("/api/sniffer/stop");
    if (response.data.status === "success") {
      isSniffing.value = false;
      store.dispatch("updateIsSniffing", isSniffing.value);
      timerStore.stopTimer();
    }
    alert(response.data.message);
    hideModal("stopCaptureModal");
  } catch (error) {
    console.error("Error stopping sniffer:", error);
    alert("Sniffer is not running");
  }
};

const hideModal = (modalId) => {
  const modalElement = document.getElementById(modalId);
  if (modalElement) {
    const modalInstance =
      Modal.getInstance(modalElement) || new Modal(modalElement);
    modalInstance.hide();
  } else {
    console.error(`Modal element with id ${modalId} not found`);
  }
};

onMounted(() => {
  fetchStatus();
});
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
  margin-left: 10px;
  width: auto + 20px;
  border-radius: 0;
}
</style>
