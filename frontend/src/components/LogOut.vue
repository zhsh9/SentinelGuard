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

  <LogoutSpinner class="LogoutSpinner" v-if="isLogoutSpinnerVisible" />

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
          <button type="button" class="btn btn-primary" @click="handleLogout">
            Confirm Logout
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LogoutSpinner from "@/components/LogoutSpinner.vue";
import { Modal } from "bootstrap";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

export default {
  components: {
    LogoutSpinner,
  },
  setup() {
    const router = useRouter();
    const store = useStore();
    const isLogoutSpinnerVisible = ref(false);
    let modalInstance;

    onMounted(() => {
      const modalElement = document.getElementById("logoutModal");
      modalInstance = new Modal(modalElement);
    });

    function showSpinner() {
      isLogoutSpinnerVisible.value = true;
      setTimeout(() => {
        isLogoutSpinnerVisible.value = false;
      }, 2000);
    }

    function confirmLogout() {
      // 关闭模态对话框
      if (modalInstance) {
        modalInstance.hide();
      }

      // 执行登出逻辑
      store.commit("clearToken");
      router.push({ name: "login" });
    }

    function handleLogout() {
      showSpinner();
      setTimeout(() => {
        confirmLogout();
      }, 1000);
    }

    return {
      isLogoutSpinnerVisible,
      handleLogout,
    };
  },
};
</script>

<style lang="scss"></style>
