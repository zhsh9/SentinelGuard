<template>
  <div
    class="offcanvas offcanvas-end offcanvas-custom"
    tabindex="-1"
    id="recordOffcanvas"
    aria-labelledby="recordOffcanvasLabel"
    ref="offcanvas"
    data-bs-scroll="true"
    data-bs-backdrop="false"
  >
    <div class="offcanvas-header">
      <h5 class="offcanvas-title" id="recordOffcanvasLabel">Record Details</h5>
      <button
        type="button"
        class="btn-close text-reset"
        data-bs-dismiss="offcanvas"
        aria-label="Close"
      ></button>
    </div>
    <div class="offcanvas-body">
      <p><strong>ID:</strong> {{ currentEntry?.id }}</p>
      <p><strong>Category:</strong> {{ currentEntry?.category }}</p>
      <p><strong>Source IP:</strong> {{ currentEntry?.source_ip }}</p>
      <p><strong>Source Port:</strong> {{ currentEntry?.source_port }}</p>
      <p><strong>Destination IP:</strong> {{ currentEntry?.destination_ip }}</p>
      <p>
        <strong>Destination Port:</strong> {{ currentEntry?.destination_port }}
      </p>
      <p><strong>Time:</strong> {{ currentEntry?.time }}</p>
      <p><strong>Method:</strong> {{ currentEntry?.request_method }}</p>
      <p><strong>Request URI:</strong> {{ currentEntry?.request_uri }}</p>
      <p><strong>Version:</strong> {{ currentEntry?.http_version }}</p>
      <p><strong>Header:</strong> {{ currentEntry?.header_fields }}</p>
      <p><strong>Body:</strong> {{ currentEntry?.request_body }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useStore } from "vuex";
import { Offcanvas } from "bootstrap";

const store = useStore();
const currentEntry = computed(() => store.getters.currentEntry);

const offcanvas = ref(null);

onMounted(() => {
  if (offcanvas.value) {
    new Offcanvas(offcanvas.value);
  }
});
</script>

<style scoped>
/* Add your styles here */
</style>
