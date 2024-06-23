<template>
  <!-- Logout button -->
  <button
    type="button"
    class="btn btn-outline-primary"
    data-bs-toggle="modal"
    data-bs-target="#logoutModal"
  >
    Logout
  </button>

  <!-- Logout Confirmation Modal -->
  <div
    class="modal fade"
    id="logoutModal"
    data-bs-backdrop="static"
    data-bs-keyboard="false"
    tabindex="-1"
    aria-labelledby="logoutModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="logoutModalLabel">Logout Confirmation</h5>
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
            Confirm Logout
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { Modal } from "bootstrap";

const router = useRouter();
const store = useStore();

let modalInstance;

onMounted(() => {
  const modalElement = document.getElementById("logoutModal");
  modalInstance = new Modal(modalElement);
});

function confirmLogout() {
  // 关闭模态对话框;
  if (modalInstance) {
    modalInstance.hide();
  }

  // 执行登出逻辑
  store.commit("clearToken");
  router.push({ name: "login" });
}
</script>

<style lang="scss"></style>
