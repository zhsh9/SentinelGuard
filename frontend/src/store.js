// src/store.js
import { createStore } from "vuex";

export const store = createStore({
  state() {
    return {
      token: localStorage.getItem("token") || "", // 初始化时从 localStorage 加载 token
      dbName: localStorage.getItem("dbName") || "", // 初始化时从 localStorage 加载 dbName
      curDbPath: "", // 初始化 curDbPath
      isSniffing: false, // 初始化 isSniffing 状态
      currentEntry: null, // 初始化 currentEntry
    };
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
      localStorage.setItem("token", token); // 同步更新 localStorage
    },
    clearToken(state) {
      state.token = null;
      localStorage.removeItem("token"); // 清除 localStorage 中的 token
    },
    setDbName(state, dbName) {
      state.dbName = dbName;
      localStorage.setItem("dbName", dbName); // 同步更新 localStorage
    },
    clearDbName(state) {
      state.dbName = null;
      localStorage.removeItem("dbName"); // 清除 localStorage 中的 dbName
    },
    setCurDbPath(state, path) {
      state.curDbPath = path; // 更新 curDbPath
    },
    clearCurDbPath(state) {
      state.curDbPath = ""; // 清除 curDbPath
    },
    setIsSniffing(state, value) {
      state.isSniffing = value; // 更新 isSniffing 状态
    },
    clearIsSniffing(state) {
      state.isSniffing = false; // 清除 isSniffing 状态
    },
    setCurrentEntry(state, entry) {
      state.currentEntry = entry; // 更新 currentEntry
    },
    clearCurrentEntry(state) {
      state.currentEntry = null; // 清除 currentEntry
    },
  },
  actions: {
    updateCurDbPath({ commit }, path) {
      commit("setCurDbPath", path);
    },
    clearCurDbPath({ commit }) {
      commit("clearCurDbPath");
    },
    updateIsSniffing({ commit }, value) {
      commit("setIsSniffing", value);
    },
    clearIsSniffing({ commit }) {
      commit("clearIsSniffing");
    },
    updateCurrentEntry({ commit }, entry) {
      commit("setCurrentEntry", entry);
    },
    clearCurrentEntry({ commit }) {
      commit("clearCurrentEntry");
    },
  },
  getters: {
    curDbPath: (state) => state.curDbPath,
    token: (state) => state.token,
    dbName: (state) => state.dbName,
    isSniffing: (state) => state.isSniffing,
    currentEntry: (state) => state.currentEntry,
  },
});

export default store;
