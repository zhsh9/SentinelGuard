// src/store.js
import { createStore } from "vuex";

export const store = createStore({
  state() {
    return {
      token: localStorage.getItem("token") || "", // 初始化时从 localStorage 加载 token
      dbName: localStorage.getItem("dbName") || "", // 初始化时从 localStorage 加载 dbName
      cur_db_path: "", // 初始化 cur_db_path
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
      state.cur_db_path = path; // 更新 cur_db_path
    },
    clearCurDbPath(state) {
      state.cur_db_path = ""; // 清除 cur_db_path
    },
  },
  actions: {
    updateCurDbPath({ commit }, path) {
      commit("setCurDbPath", path);
    },
    clearCurDbPath({ commit }) {
      commit("clearCurDbPath");
    },
  },
  getters: {
    curDbPath: (state) => state.cur_db_path,
    token: (state) => state.token,
    dbName: (state) => state.dbName,
  },
});

export default store;
