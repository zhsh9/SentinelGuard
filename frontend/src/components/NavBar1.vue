<template>
  <nav class="navbar navbar-expand-xl navbar-dark fixed-top bg-dark">
    <div class="container-fluid">
      <div class="navbar-brand-container col-md-3 col-lg-2">
        <div>
          <a class="navbar-brand" href="/"
            ><img class="navbar-brand" src="../assets/logo.svg" alt="logo" />
            SentinelGuard</a
          >
        </div>
      </div>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarCollapse"
        aria-controls="navbarCollapse"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div
        class="collapse navbar-collapse col-md-9 col-lg-10"
        id="navbarCollapse"
      >
        <ul class="navbar-nav me-auto mb-2 mb-md-0">
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
// import SearchItem from "@/components/SearchItem.vue";
import LogOut from "@/components/LogOut.vue";
import SearchItem from "./SearchItem.vue";
</script>

<style lang="scss" scoped>
nav {
  font-family: Montserrat, Arial, Helvetica, sans-serif;
}

// logo
.container-fluid img {
  width: 35px;
  margin-right: 3px;
}

$brand_column1_width: 20.7%;

// brand
.navbar-brand-container {
  font-size: 1.8rem;
  font-weight: bolder;
  display: flex;
  flex-direction: column;
  align-items: center; // 垂直居中对齐
}

.navbar {
  max-height: 65px;
}
</style>
