import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { store } from "./store";

// import "bootstrap/dist/css/bootstrap.min.css"; // 和其他的CSS导入冲突了
import "bootstrap/dist/js/bootstrap.bundle.min.js";

const app = createApp(App);
app.use(router);
app.use(store);
app.mount("#app");
