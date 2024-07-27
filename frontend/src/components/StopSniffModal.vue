<template>
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
import { computed, inject } from "vue";
import { useStore } from "vuex";
import { Modal } from "bootstrap";
import axios from "axios";

const store = useStore();
const timerStore = inject("timerStore");
const isSniffing = computed(() => store.state.isSniffing);

const stopCapture = async () => {
  try {
    const response = await axios.post("/api/sniffer/stop");
    if (response.data.status === "success") {
      store.dispatch("updateIsSniffing", false);
      timerStore.stopTimer();
    }
    hideModal("stopCaptureModal");
  } catch (error) {
    console.error("Error stopping sniffer:", error);
    alert("Sniffer is not running");
  }
};

const hideModal = (modalId) => {
  const modalElement = document.getElementById(modalId);
  const modalInstance = Modal.getInstance(modalElement);
  if (modalInstance) {
    modalInstance.hide();
  }
};
</script>

<style scoped>
/* 添加样式以适应需求 */
</style>
