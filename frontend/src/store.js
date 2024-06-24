import { createStore } from "vuex";

export const store = createStore({
  state() {
    return {
      token: localStorage.getItem("token") || "", // 初始化时从 localStorage 加载 token
      dbName: localStorage.getItem("dbName") || "", // 初始化时从 localStorage 加载 dbName
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
  },
});

export default store;
