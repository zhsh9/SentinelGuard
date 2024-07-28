<template>
  <li class="nav-item" data-bs-toggle="modal" data-bs-target="#uploadPcapModal">
    <a class="nav-link active" href="#">Upload PCAP</a>
  </li>

  <!-- Upload PCAP Modal -->
  <div class="modal fade modal-lg" id="uploadPcapModal">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Upload PCAP</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          >
            <span aria-hidden="true"></span>
          </button>
        </div>
        <div class="modal-body">
          <div>
            <label for="formFile" class="form-label mt-1"
              >Upload a pcap file to be analysed:</label
            >
            <input
              class="form-control"
              type="file"
              id="formFile"
              @change="handleFileChange"
            />
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
          <button type="button" class="btn btn-primary" @click="uploadFile">
            Upload
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { Modal } from "bootstrap";
import { useStore } from "vuex"; // 使用 Vuex

const selectedFile = ref(null);
const store = useStore();

const handleFileChange = (event) => {
  selectedFile.value = event.target.files[0];
};

// 检查文件头
const checkFileHeader = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = (event) => {
      const arrayBuffer = event.target.result;
      const header = new Uint8Array(arrayBuffer, 0, 4);
      const headerHex = Array.from(header)
        .map((byte) => byte.toString(16).padStart(2, "0"))
        .join("");

      // pcap: D4C3B2A1 or A1B2C3D4
      // pcapng: 0A0D0D0A
      // snoop: 736e6f6f70 (ASCII for 'snoop')
      // erf: 454652 (ASCII for 'ERF')
      if (
        headerHex === "d4c3b2a1" ||
        headerHex === "a1b2c3d4" ||
        headerHex === "0a0d0d0a" ||
        headerHex === "736e6f6f70" ||
        headerHex.startsWith("454652")
      ) {
        resolve(true);
      } else {
        resolve(false);
      }
    };
    reader.onerror = () => reject(new Error("Error reading file"));
    reader.readAsArrayBuffer(file.slice(0, 4));
  });
};

const uploadFile = async () => {
  // 检查是否选择了文件
  if (!selectedFile.value) {
    alert("Please select a file first!");
    return;
  }

  // 检查文件后缀名是否为 pcap, pcapng, snoop, erf
  const file = selectedFile.value;
  const fileName = file.name.toLowerCase();
  const validExtensions = [".pcap", ".pcapng", ".snoop", ".erf", ".hccapx"];

  // 检查文件后缀名是否为支持的格式
  if (!validExtensions.some((ext) => fileName.endsWith(ext))) {
    alert("Please select a valid .pcap, .pcapng, .snoop, or .erf file.");
    return;
  }

  // 检查文件头是否为 pcap, pcapng, snoop, erf
  try {
    const isValidHeader = await checkFileHeader(file);
    if (!isValidHeader) {
      alert("Please select a valid .pcap, .pcapng, .snoop, or .erf file.");
      return;
    }
  } catch (error) {
    console.error("Error checking file header:", error);
    alert("An error occurred while checking the file.");
    return;
  }

  // 检查文件大小是否超过 100 MB
  if (selectedFile.value.size > 100 * 1024 * 1024) {
    alert("File size must be less than 100 MB.");
    return;
  }

  // 创建一个 FormData 对象，用于将文件上传到服务器
  const formData = new FormData();
  formData.append("pcapFile", selectedFile.value);

  try {
    const response = await fetch("/api/upload-pcap", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      alert("File uploaded successfully!");
      // 处理上传成功的逻辑
      store.dispatch("updateIsSniffing", true);
      // 等待 1 秒后关闭模态框
      setTimeout(closeModal, 1000);
    } else {
      alert("File upload failed.");
      // 处理上传失败的逻辑
      // closeModal();
    }
  } catch (error) {
    console.error("Error uploading file:", error);
    alert("An error occurred while uploading the file.");
    // closeModal();
  }
};

const closeModal = () => {
  const modalElement = document.getElementById("uploadPcapModal");
  const modalInstance =
    Modal.getInstance(modalElement) || new Modal(modalElement);
  modalInstance.hide();
  // 1秒后设置 Dashboard 不继续从数据库中读取数据
  setTimeout(() => {
    stopSniffing();
  }, 1000);
};

const stopSniffing = () => {
  store.dispatch("clearIsSniffing");
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
