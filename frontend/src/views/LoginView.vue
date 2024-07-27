<template>
  <div class="login-view d-flex align-items-center py-4 bg-body-tertiary">
    <main class="form-signin w-100 m-auto">
      <form @submit.prevent="handleSubmit">
        <img
          class="mb-4"
          src="../assets/logo.svg"
          alt=""
          width="72"
          height="57"
        />
        <h1 class="h3 mb-3 fw-normal">Please login</h1>

        <div class="form-floating">
          <input
            type="text"
            class="form-control"
            id="floatingInput"
            placeholder="name@example.com"
            v-model="username"
          />
          <label for="floatingInput">Username</label>
        </div>
        <div class="form-floating">
          <input
            type="password"
            class="form-control"
            id="floatingPassword"
            placeholder="Password"
            v-model="password"
          />
          <label for="floatingPassword">Password</label>
        </div>

        <div class="form-check text-start my-3">
          <input
            class="form-check-input"
            type="checkbox"
            value="remember-me"
            id="flexCheckDefault"
            v-model="rememberMe"
          />
          <label class="form-check-label" for="flexCheckDefault">
            Remember me
          </label>
        </div>
        <button
          class="btn btn-primary w-100 py-2"
          type="submit"
          @click="showSpinner"
        >
          Login
        </button>
        <p class="my-3 text-body-secondary">&copy; 2024</p>
        <div v-if="errorMessage" class="alert alert-danger" role="alert">
          {{ errorMessage }}
        </div>
      </form>
    </main>
  </div>
  <LoginSpinner class="LoginSpinner" v-if="isSpinnerVisible" />
</template>

<script>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import axios from "axios";
import LoginSpinner from "@/components/LoginSpinner.vue";

export default {
  name: "LoginView",
  components: {
    LoginSpinner,
  },
  data() {
    return {
      isSpinnerVisible: false,
    };
  },
  methods: {
    showSpinner() {
      this.isSpinnerVisible = true;
      setTimeout(() => {
        this.isSpinnerVisible = false;
      }, 2000);
    },
  },
  setup() {
    // Variables
    const username = ref("");
    const password = ref("");
    const errorMessage = ref("");
    const router = useRouter();
    const rememberMe = ref(false);
    const store = useStore();

    onMounted(() => {
      // Check RememberMe
      if (localStorage.getItem("rememberMe") === "true") {
        username.value = localStorage.getItem("username");
        password.value = localStorage.getItem("password");
        rememberMe.value = true;
      }
    });

    // Login
    const handleSubmit = async () => {
      errorMessage.value = "";
      const path = "/api/login"; // Use relative path to proxy requests to backend
      const post_body = {
        username: username.value,
        password: password.value,
      };

      axios
        .post(path, post_body)
        .then((response) => {
          // console.log("Success login:", response);

          if (response.data && response.data.token) {
            // console.log("Token:", response.data.token);
            store.commit("setToken", response.data.token); // 存储 token 到 Vuex
            localStorage.setItem("token", response.data.token); // 存储 token 到 localStorage

            // 如果用户勾选了“记住我”，则存储用户名和密码
            if (rememberMe.value) {
              localStorage.setItem("username", username.value);
              localStorage.setItem("password", password.value);
              localStorage.setItem("rememberMe", true);
            } else {
              localStorage.removeItem("username");
              localStorage.removeItem("password");
              localStorage.setItem("rememberMe", false);
            }

            router.push({ name: "home" });
          } else {
            errorMessage.value = "Incorrect username or password";
          }
        })
        .catch((error) => {
          if (
            error.response &&
            error.response.data &&
            error.response.data.error
          ) {
            errorMessage.value = error.response.data.error;
          } else {
            errorMessage.value = "An error occurred. Please try again.";
          }
        });
    };

    return {
      username,
      password,
      rememberMe,
      errorMessage,
      handleSubmit,
    };
  },
};
</script>

<style lang="scss" scoped>
.login-view {
  height: 100%;
}

.form-signin {
  max-width: 330px;
  padding: 1rem;
}

.form-signin .form-floating:focus-within {
  z-index: 2;
}

.form-signin input[type="email"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}

.form-signin input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}

.form-signin img {
  width: 22%;
  height: auto;
}
</style>
