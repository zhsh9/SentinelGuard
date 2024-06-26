import { reactive, toRefs } from "vue";

const state = reactive({
  time: 0,
  isRunning: false,
  timer: null,
});

const startTimer = () => {
  state.time = 0;
  state.isRunning = true;
  clearInterval(state.timer);
  state.timer = setInterval(() => {
    state.time++;
  }, 1000);
};

const stopTimer = () => {
  state.isRunning = false;
  clearInterval(state.timer);
};

export const useTimerStore = () => {
  return {
    ...toRefs(state),
    startTimer,
    stopTimer,
  };
};
