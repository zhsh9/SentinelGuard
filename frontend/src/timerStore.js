import { reactive, toRefs } from "vue";

const state = reactive({
  time: 0,
  isRunning: false,
  timer: null,
});

// 恢复状态
const loadState = () => {
  const savedTime = localStorage.getItem("timer-time");
  const savedIsRunning = localStorage.getItem("timer-isRunning");

  if (savedTime !== null) {
    state.time = Number(savedTime);
  }

  if (savedIsRunning === "true") {
    startTimer();
  }
};

// 保存状态
const saveState = () => {
  localStorage.setItem("timer-time", state.time);
  localStorage.setItem("timer-isRunning", state.isRunning);
};

const startNewTimer = () => {
  state.time = 0; // 重置时间为 0
  saveState();
};

const startTimer = () => {
  state.isRunning = true; // 设置 isRunning 为 true, 表示计时器正在运行
  clearInterval(state.timer);
  saveState();
  state.timer = setInterval(() => {
    state.time++;
    saveState();
  }, 1000);
};

const stopTimer = () => {
  state.isRunning = false;
  clearInterval(state.timer);
  saveState();
};

// 在应用加载时恢复状态
loadState();

export const useTimerStore = () => {
  return {
    ...toRefs(state),
    startNewTimer,
    startTimer,
    stopTimer,
  };
};
