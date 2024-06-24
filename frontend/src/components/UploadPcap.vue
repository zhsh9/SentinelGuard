<template>
  <li class="nav-item">
    <a class="nav-link active" href="#">Upload PCAP</a>
  </li>
</template>

<script>
export default {
  name: "UploadPcap",
};
</script>

<style lang="scss" scoped>
.nav-link {
  font-weight: bold;

  &:hover {
    color: darken(#a2e5d2, 10%) !important;
    text-decoration: underline;
  }
}
</style>
