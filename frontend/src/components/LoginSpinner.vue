<template>
  <div
    class="overlay d-flex flex-column justify-content-center align-items-center"
  >
    <div class="progress" style="width: 50%">
      <div
        class="progress-bar progress-bar-striped progress-bar-animated bg-success"
        role="progressbar"
        :aria-valuenow="progress"
        aria-valuemin="0"
        aria-valuemax="100"
        :style="{ width: progress + '%' }"
      ></div>
    </div>
    <div class="mt-3 text-success">Login successful, redirecting...</div>
  </div>
</template>

<script>
export default {
  name: "LoginSpinner",
  data() {
    return {
      progress: 0,
    };
  },
  mounted() {
    this.animateProgress();
  },
  methods: {
    animateProgress() {
      const duration = 10; // 1 second
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
  background-color: rgba(255, 255, 255, 1); /* 半透明白色背景 */
  z-index: 9999; /* 确保覆盖在最上层 */
}
</style>
