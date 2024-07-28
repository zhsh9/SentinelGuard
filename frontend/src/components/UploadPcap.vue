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

const selectedFile = ref(null);

const handleFileChange = (event) => {
  selectedFile.value = event.target.files[0];
};

const uploadFile = async () => {
  // 检查是否选择了文件
  if (!selectedFile.value) {
    alert("Please select a file first!");
    return;
  }

  // 检查文件后缀名是否为 pcap pcapng
  if (
    !selectedFile.value.name.endsWith(".pcap") ||
    !selectedFile.value.name.endsWith(".pcapng")
  ) {
    alert("Please select a .pcap file.");
    return;
  }

  // 检查文件类型 MIME 是否为 pcap pcapng
  if (
    selectedFile.value.type !== "application/vnd.tcpdump.pcap" &&
    selectedFile.value.type !== "application/vnd.tcpdump.pcapng"
  ) {
    alert("Please select a .pcap file.");
    return;
  }

  // 检查文件大小是否超过 10 MB
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
      closeModal();
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
