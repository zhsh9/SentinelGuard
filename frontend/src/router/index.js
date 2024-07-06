import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import store from "../store";
import axios from "axios";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const token = store.state.token;
  console.log("Navigating to:", to.name);
  console.log("Current token:", token);

  if (!token && to.name !== "login") {
    // 如果没有 token 且目标不是登录页面，则重定向到登录页面
    next({ name: "login" });
  } else if (token) {
    const path = "/api/verify"; // Use relative path to proxy
    const post_body = { token: token };

    try {
      const response = await axios.post(path, post_body);
      console.log("API Response:", response.data);

      if (response.data.status === "200") {
        if (to.name === "login") {
          next({ name: "home" }); // 如果已登录且目标是登录页面，则重定向到主页
        } else {
          next(); // 如果已登录且目标不是登录页面，则继续导航
        }
      } else {
        store.commit("clearToken"); // 清除无效的 token
        next({ name: "login" }); // 验证失败，重定向到登录页
      }
    } catch (error) {
      console.error("Error verifying token:", error);
      store.commit("clearToken"); // 捕获错误时也清除 token
      next({ name: "login" }); // 重定向到登录页
    }
  } else {
    next(); // 没有 token 且目标是登录页面，继续导航
  }
});

export default router;
