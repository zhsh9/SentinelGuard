<template>
  <div
    :class="[
      'overlay',
      'd-flex',
      'flex-column',
      'justify-content-center',
      'align-items-center',
      overlayThemeClass,
    ]"
  >
    <div class="progress" style="width: 50%">
      <div
        :class="[
          'progress-bar',
          'progress-bar-striped',
          'progress-bar-animated',
          barThemeClass,
        ]"
        role="progressbar"
        :aria-valuenow="progress"
        aria-valuemin="0"
        aria-valuemax="100"
        :style="{ width: progress + '%' }"
      ></div>
    </div>
    <div class="mt-3" :class="textThemeClass">
      Logout successful, redirecting...
    </div>
  </div>
</template>

<script>
export default {
  name: "LogoutSpinner",
  data() {
    return {
      progress: 0,
      overlayThemeClass: "",
      barThemeClass: "bg-success",
      textThemeClass: "text-success",
    };
  },
  mounted() {
    this.updateThemeClass();
    document.documentElement.addEventListener(
      "themeChange",
      this.updateThemeClass
    );
    this.animateProgress();
  },
  beforeUnmount() {
    document.documentElement.removeEventListener(
      "themeChange",
      this.updateThemeClass
    );
  },
  methods: {
    animateProgress() {
      const duration = 20; // 1 second in milliseconds
      const interval = 10; // update every 10ms
      const steps = duration / interval;
      const stepSize = 100 / steps;

      let currentProgress = 0;

      const intervalId = setInterval(() => {
        currentProgress += stepSize;
        if (currentProgress >= 100) {
          currentProgress = 100;
          clearInterval(intervalId);
        }
        this.progress = Math.round(currentProgress);
      }, interval);
    },
    updateThemeClass() {
      const isDark =
        document.documentElement.getAttribute("data-bs-theme") === "dark";
      this.overlayThemeClass = isDark ? "overlay-dark" : "";
      this.barThemeClass = isDark ? "bg-success" : "bg-primary";
      this.textThemeClass = isDark ? "text-success" : "text-primary";
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

.overlay-dark {
  background-color: rgba(0, 0, 0, 1); /* 半透明黑色背景 */
}
</style>
