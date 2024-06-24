<template>
  <div
    :class="[
      'overlay',
      'd-flex',
      'flex-column',
      'justify-content-center',
      'align-items-center',
      themeClass,
    ]"
  >
    <div :class="['spinner-border', themeClass]" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
    <div class="mt-3" :class="themeClass">Login successful, redirecting...</div>
  </div>
</template>

<script>
export default {
  name: "LoginSpinner",
  data() {
    return {
      themeClass: "text-success", // 默认主题类
    };
  },
  created() {
    this.updateThemeClass();
    document.documentElement.addEventListener(
      "themeChange",
      this.updateThemeClass
    );
  },
  beforeUnmount() {
    document.documentElement.removeEventListener(
      "themeChange",
      this.updateThemeClass
    );
  },
  methods: {
    updateThemeClass() {
      const isDark =
        document.documentElement.getAttribute("data-bs-theme") === "dark";
      this.themeClass = isDark ? "text-light" : "text-success";
    },
  },
};
</script>

<style scoped>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: var(--bs-body-bg); /* 使用 Bootstrap 的 CSS 变量 */
  z-index: 9999; /* 确保覆盖在最上层 */
}
</style>
