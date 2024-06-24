<template>
  <nav class="navbar navbar-expand-lg bg-dark fixed-top" data-bs-theme="light">
    <div class="container-fluid">
      <a class="navbar-brand" href="/">
        <img src="../assets/logo.png" alt="Logo" style="height: 75px" />
        <span>SentinelGuard</span>
      </a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarColor01"
        aria-controls="navbarColor01"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse mt-2" id="navbarColor01">
        <ul class="navbar-nav me-auto">
          <DataBase />
          <UploadPcap />
          <RealtimeCapture />
        </ul>
        <SearchItem />
        <LogOut />
      </div>
    </div>
  </nav>
</template>

<script setup>
import DataBase from "@/components/DataBase.vue";
import UploadPcap from "@/components/UploadPcap.vue";
import RealtimeCapture from "@/components/RealtimeCapture.vue";
import SearchItem from "@/components/SearchItem.vue";
import LogOut from "@/components/LogOut.vue";
</script>

<script>
export default {
  name: "NavBar",
};
</script>

<style lang="scss" scoped>
// navbar
.navbar {
  padding: 5px 15px;
  padding-bottom: 8px;

  .navbar-brand {
    color: white;
    font-size: 1.5em;
    font-weight: bold;
    font-family: Papyrus, Arial, Helvetica, sans-serif;
    margin: 0;
    margin-right: 5px;
    padding-top: 10px;

    span {
      display: inline-block; /* 确保 margin-top 生效 */
      margin-left: 10px;
      margin-top: 0px;
      margin-bottom: 0;
      height: auto;
    }

    &:hover {
      // color: darken(white, 10%);
      color: darken(#a2e5d2, 10%);
    }
  }

  .navbar-nav {
    font-size: 1.3em;
  }

  .form-control {
    margin-right: 0.5rem;
  }

  .btn {
    margin-left: 0.5rem;
  }
}

.navbar-brand a,
img {
  width: auto;
  height: auto;
}

#app > div:nth-child(3) > nav > div > a > span {
  font-size: 45px;
  font-weight: bolder;
  padding-top: 10px;

  border-right: 1 solid white;
}

#app > div:nth-child(3) > nav > div > a > img {
  padding-bottom: 10px;
  padding-right: 10px;
}
</style>
