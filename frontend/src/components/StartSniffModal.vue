<template>
  <div
    class="modal fade"
    id="startCaptureModal"
    tabindex="-1"
    aria-labelledby="startCaptureModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="startCaptureModalLabel">
            Start Capturing HTTP Traffic
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <p class="text-danger">
            Are you sure to start capturing http traffic?
          </p>
          <p class="text-warning">
            Current status:
            <strong>{{ isSniffing ? "Sniffing" : "Not Sniffing" }}</strong>
          </p>
          <div>
            <h5 class="select-title">Select Interfaces:</h5>
            <input
              type="checkbox"
              @change="toggleSelectAllInterfaces"
              :checked="allInterfacesSelected"
            />
            Select All
            <div v-for="iface in interfaces" :key="iface.name">
              <input
                type="checkbox"
                :value="iface.name"
                v-model="selectedInterfaces"
              />
              {{ iface.name }}: {{ iface.address }}
            </div>
          </div>
          <div>
            <h5 class="select-title">Select Ports:</h5>
            <input
              type="checkbox"
              @change="selectAllPorts"
              :checked="allPortsSelected"
            />
            Select All
            <div v-for="port in availablePorts" :key="port">
              <input type="checkbox" :value="port" v-model="selectedPorts" />
              {{ port }}
            </div>
          </div>
          <div>
            <label class="custom-port-label">Custom Port:</label>
            <input type="text" v-model="customPort" />
            <button @click="addCustomPort">Add</button>
          </div>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button type="button" class="btn btn-primary" @click="startCapture">
            Start
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref, onMounted, computed, inject } from "vue";
import { useStore } from "vuex";
import { Modal } from "bootstrap";

export default {
  name: "StartSniffModal",
  setup() {
    const store = useStore(); // 使用 Vuex
    const timerStore = inject("timerStore");
    const interfaces = ref([]);
    const selectedInterfaces = ref([]);
    const commonPorts = ref(["all", 80, 443, 8080, 3000]);
    const availablePorts = ref([...commonPorts.value]);
    const selectedPorts = ref([]);
    const customPort = ref("");

    const fetchInterfaces = async () => {
      try {
        const response = await axios.get("/api/sniffer/interfaces");
        interfaces.value = response.data;
      } catch (error) {
        console.error("Error fetching interfaces:", error);
      }
    };

    const fetchStatus = async () => {
      try {
        const response = await axios.get("/api/sniffer/status");
        store.dispatch("updateIsSniffing", response.data.sniffing);
      } catch (error) {
        console.error("Error fetching sniffer status:", error);
      }
    };

    const toggleSelectAllInterfaces = (event) => {
      if (event.target.checked) {
        selectAllInterfaces();
      } else {
        clearAllInterfaces();
      }
    };

    const selectAllInterfaces = () => {
      selectedInterfaces.value = interfaces.value.map((i) => i.name);
    };

    const clearAllInterfaces = () => {
      selectedInterfaces.value = [];
    };

    const addCustomPort = () => {
      const port = parseInt(customPort.value);
      if (port && !availablePorts.value.includes(port)) {
        availablePorts.value.push(port);
        customPort.value = "";
      }
    };

    const selectAllPorts = (event) => {
      if (event.target.checked) {
        selectedPorts.value = availablePorts.value.slice();
      } else {
        selectedPorts.value = [];
      }
    };

    const allInterfacesSelected = computed(() => {
      return selectedInterfaces.value.length === interfaces.value.length;
    });

    const allPortsSelected = computed(() => {
      return selectedPorts.value.length === availablePorts.value.length;
    });

    const startCapture = async () => {
      try {
        let response;

        // 如果没有选择接口或者选择了所有端口
        if (
          selectedInterfaces.value.length === 0 ||
          "all" in selectedPorts.value
        ) {
          response = await axios.post("/api/sniffer/start", {
            interface_list: selectedInterfaces.value,
          });
        } else {
          // 选择了特定端口
          response = await axios.post("/api/sniffer/start", {
            interface_list: selectedInterfaces.value,
            port_list: selectedPorts.value,
          });
        }

        // 如果成功开始抓包
        if (response.data.status === "success") {
          store.dispatch("updateIsSniffing", true);
          timerStore.startTimer();
        }
        hideModal();
      } catch (error) {
        // 如果抓包失败
        console.error("Error starting sniffer:", error);
      }
    };

    const hideModal = () => {
      const modalElement = document.getElementById("startCaptureModal");
      const modal = Modal.getInstance(modalElement);
      if (modal) {
        modal.hide();
      }
    };

    onMounted(() => {
      const modalElement = document.getElementById("startCaptureModal");
      new Modal(modalElement);
      fetchInterfaces();
      fetchStatus(); // 获取当前状态
    });

    const isSniffing = computed(() => store.state.isSniffing); // 从 Vuex 获取 isSniffing 状态

    return {
      isSniffing,
      interfaces,
      selectedInterfaces,
      commonPorts,
      availablePorts,
      selectedPorts,
      customPort,
      startCapture,
      toggleSelectAllInterfaces,
      selectAllInterfaces,
      clearAllInterfaces,
      addCustomPort,
      selectAllPorts,
      allInterfacesSelected,
      allPortsSelected,
    };
  },
};
</script>

<style scoped>
.custom-port-label {
  margin-right: 10px;
}

.select-title {
  margin-top: 10px;
  margin-bottom: 5px;
}
</style>
