<template>
  <div class="container-fluid">
    <div class="row">
      <div
        class="sidebar border border-right col-md-3 col-lg-2 p-0 bg-body-tertiary rounded-bottom"
      >
        <div id="info" class="my-2">
          <a
            type="button"
            class="btn btn-success"
            data-bs-toggle="tooltip"
            data-bs-placement="right"
            data-bs-original-title="Star me on GitHub"
            href="https://github.com/zhsh9/SentinelGuard"
          >
            v0.0.2
          </a>
          <figure>
            <blockquote class="blockquote">
              <p class="mb-0">No System Is Safe.</p>
            </blockquote>
            <figcaption class="blockquote-footer">
              <cite title="Source Title">Who Am I</cite>
            </figcaption>
          </figure>
        </div>

        <div id="select-threat">
          <ul class="list-group">
            <li
              class="list-group-item d-flex justify-content-between align-items-center"
            >
              Total Number of Packets
              <span class="badge bg-info rounded-pill">{{ totalPackets }}</span>
            </li>
            <li
              class="list-group-item d-flex justify-content-between align-items-center"
            >
              Total Number of Threats
              <span class="badge bg-info rounded-pill">{{ totalThreats }}</span>
            </li>
            <li
              class="list-group-item d-flex justify-content-between align-items-center"
            >
              Categories Selected
              <span id="categories-selected" class="badge bg-info rounded-pill"
                >{{ selectedCategories.length }} /
                {{ configedCategories }}</span
              >
            </li>
            <li
              class="list-group-item d-flex justify-content-between align-items-center"
            >
              Time of Capturing
              <span class="badge bg-info rounded-pill">{{
                formattedTime
              }}</span>
            </li>
          </ul>
        </div>

        <hr class="fancy-line" />

        <div id="threat-cate">
          <ul class="list-group">
            <li
              v-for="(count, category) in categoryCounts"
              :key="category"
              :class="getCategoryClass(category)"
              @click="toggleCategorySelection(category)"
            >
              {{ category }}
              <span :class="getCategoryBadgeClass(category)">{{ count }}</span>
            </li>
          </ul>
        </div>
      </div>

      <main class="ms-sm-auto col-md-8 col-lg-10 px-md-4">
        <div
          class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom"
        >
          <h1 class="h2">Dashboard</h1>
          <div class="btn-toolbar mb-2 mb-md-0">
            <!-- SVG Symbol Definitions -->
            <svg style="display: none">
              <symbol id="calendar3" fill="currentColor" viewBox="0 0 16 16">
                <path
                  d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"
                />
              </symbol>
              <symbol
                id="share"
                fill="currentColor"
                viewBox="0 0 458.624 458.624"
              >
                <path
                  d="M339.588,314.529c-14.215,0-27.456,4.133-38.621,11.239l-112.682-78.67c1.809-6.315,2.798-12.976,2.798-19.871 c0-6.896-0.989-13.557-2.798-19.871l109.64-76.547c11.764,8.356,26.133,13.286,41.662,13.286c39.79,0,72.047-32.257,72.047-72.047 C411.634,32.258,379.378,0,339.588,0c-39.79,0-72.047,32.257-72.047,72.047c0,5.255,0.578,10.373,1.646,15.308l-112.424,78.491 c-10.974-6.759-23.892-10.666-37.727-10.666c-39.79,0-72.047,32.257-72.047,72.047s32.256,72.047,72.047,72.047 c13.834,0,26.753-3.907,37.727-10.666l113.292,79.097c-1.629,6.017-2.514,12.34-2.514,18.872c0,39.79,32.257,72.047,72.047,72.047 c39.79,0,72.047-32.257,72.047-72.047C411.635,346.787,379.378,314.529,339.588,314.529z"
                />
              </symbol>
              <symbol id="export" fill="currentColor" viewBox="0 0 24 24">
                <polyline points="15 3 21 3 21 9"></polyline>
                <path
                  d="M21,13v7a1,1,0,0,1-1,1H4a1,1,0,0,1-1-1V4A1,1,0,0,1,4,3h7"
                ></path>
                <line x1="11" y1="13" x2="21" y2="3"></line>
              </symbol>
            </svg>
            <!-- Buttons -->
            <div class="btn-group me-2">
              <!-- Share button -->
              <button
                type="button"
                class="btn btn-sm btn-outline-secondary d-flex align-items-center gap-1"
                data-bs-toggle="modal"
                data-bs-target="#share-modal"
                @click="shareUrl"
              >
                <svg class="bi">
                  <use xlink:href="#share"></use>
                </svg>
                Share
              </button>
              <!-- Export button -->
              <button
                type="button"
                class="btn btn-sm btn-outline-secondary dropdown-toggle d-flex align-items-center gap-1"
                id="btnGroupDrop_Export"
                data-bs-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="true"
                @click="exportChecker"
              >
                <svg class="bi">
                  <use xlink:href="#export"></use>
                </svg>
                Export
              </button>
              <!-- Export drop-down -->
              <div
                class="dropdown-menu"
                aria-labelledby="btnGroupDrop_Export"
                data-popper-placement="bottom-start"
              >
                <a
                  class="dropdown-item"
                  href="/export/csv"
                  @click.prevent="exportData('csv')"
                  >CSV</a
                >
                <a
                  class="dropdown-item"
                  href="/export/pcap"
                  @click.prevent="exportData('pcap')"
                  >PCAP</a
                >
              </div>
            </div>
            <button
              type="button"
              class="btn btn-sm btn-outline-secondary dropdown-toggle d-flex align-items-center gap-1"
            >
              <svg class="bi">
                <use xlink:href="#calendar3"></use>
              </svg>
              This week
            </button>
          </div>
        </div>

        <!-- Share Modal -->
        <div class="modal fade" id="share-modal">
          <div class="modal-dialog" role="document">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">
                  <svg class="bi">
                    <use xlink:href="#share"></use>
                  </svg>
                  Share
                </h5>
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
                <p>URL copied to clipboard.</p>
              </div>
            </div>
          </div>
        </div>

        <div class="table-responsive small">
          <table class="table table-hover table-striped table-sm">
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col">Cate</th>
                <th scope="col">Src IP</th>
                <th scope="col">Src Port</th>
                <th scope="col">Dst IP</th>
                <th scope="col">Dst Port</th>
                <th scope="col">Time</th>
                <th scope="col">Method</th>
                <th scope="col">Request URI</th>
                <th scope="col">Version</th>
                <th scope="col">Header</th>
                <th scope="col">Body</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="entry in filteredTableData"
                :key="entry.id"
                data-bs-toggle="offcanvas"
                href="#recordOffcanvas"
                role="button"
                aria-controls="recordOffcanvas"
                @click="setCurrentEntry(entry)"
              >
                <td>
                  <span :class="getCategoryEntryClass(entry.category)">
                    {{ entry.id }}
                  </span>
                </td>
                <td>
                  <span :class="getCategoryEntryClass(entry.category)">
                    {{ entry.category }}
                  </span>
                </td>
                <td>{{ entry.source_ip }}</td>
                <td>{{ entry.source_port }}</td>
                <td>{{ entry.destination_ip }}</td>
                <td>{{ entry.destination_port }}</td>
                <td>{{ entry.time }}</td>
                <td>{{ entry.request_method }}</td>
                <td>{{ entry.request_uri }}</td>
                <td>{{ entry.http_version }}</td>
                <td>{{ entry.header_fields }}</td>
                <td>{{ entry.request_body }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </main>
      <!-- Include the HttpOffcanvas component -->
      <HttpOffcanvas />
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, computed, inject, onMounted, onBeforeUnmount, watch } from "vue";
import { useStore } from "vuex";
import { EventBus } from "@/eventBus";
import HttpOffcanvas from "./HttpOffcanvas.vue";

// 类别映射
const categoryMap = {
  "-1": "Unclassified",
  0: "Normal Packets",
  1: "Insecure IPs",
  2: "Insecure Referers",
  3: "CVEs",
  4: "Brute Force",
  5: "Command Injection",
  6: "CSRF",
  7: "File Inclusion",
  8: "File Upload",
  9: "Insecure CAPTCHA",
  10: "SQL Injection",
  11: "SQL Injection (Blind)",
  12: "XSS (Reflected)",
  13: "XSS (Stored)",
};

// 类别颜色映射
const warningCategories = ["Insecure IPs", "Insecure Referers", "CVEs"];
const dangerCategories = [
  "Brute Force",
  "Command Injection",
  "CSRF",
  "File Inclusion",
  "File Upload",
  "Insecure CAPTCHA",
  "SQL Injection",
  "SQL Injection (Blind)",
  "XSS (Reflected)",
  "XSS (Stored)",
];

// 从依赖注入中获取 timerStore
const timerStore = inject("timerStore");

// 计算属性：格式化时间
const formattedTime = computed(() => {
  const minutes = Math.floor(timerStore.time.value / 60);
  const seconds = timerStore.time.value % 60;
  return `${minutes}:${seconds.toString().padStart(2, "0")}`;
});

// 方法：分享 URL
const shareUrl = async () => {
  const url = window.location.href;

  // 使用 Clipboard API
  if (navigator.clipboard && navigator.clipboard.writeText) {
    try {
      await navigator.clipboard.writeText(url);
      return;
    } catch (err) {
      console.error("Failed to copy using Clipboard API: ", err);
    }
  }

  // 回退到 document.execCommand 方法
  const textArea = document.createElement("textarea");
  textArea.value = url;
  textArea.style.position = "fixed"; // 避免滚动到页面底部
  textArea.style.opacity = "0"; // 隐藏文本区域
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();

  try {
    const successful = document.execCommand("copy");
    if (successful) {
      // alert("URL copied to clipboard");
    } else {
      console.error("Fallback: Unable to copy");
      alert("Error copying URL");
    }
  } catch (err) {
    console.error("Fallback: Error copying URL: ", err);
    alert("Error copying URL");
  }

  document.body.removeChild(textArea);
};

// 使用 store
const store = useStore();

// 表格数据
const tableData = ref([]);
// 统计数据
const totalPackets = ref(0);
const totalThreats = ref(0);
const selectedCategories = ref([]); // 存储选中的类别数组
const configedCategories = ref(0); // 配置的攻击类别数
const categoryCounts = ref({
  "Normal Packets": 0,
  "Insecure IPs": 0,
  "Insecure Referers": 0,
  CVEs: 0,
  "Brute Force": 0,
  "Command Injection": 0,
  CSRF: 0,
  "File Inclusion": 0,
  "File Upload": 0,
  "Insecure CAPTCHA": 0,
  "SQL Injection": 0,
  "SQL Injection (Blind)": 0,
  "XSS (Reflected)": 0,
  "XSS (Stored)": 0,
});
const intervalId = ref(null); // 定时器 ID

const curDbPath = computed(() => store.getters.curDbPath);
const isSniffing = computed(() => store.getters.isSniffing);
const showExportDropdown = ref(false);

const filteredTableData = computed(() => {
  if (selectedCategories.value.length === 0) {
    return tableData.value;
  }
  return tableData.value.filter((entry) =>
    selectedCategories.value.includes(categoryMap[entry.category])
  );
});

// 获取选中数据库表的数据
const fetchTableData = async (database) => {
  try {
    if (!database && curDbPath.value && curDbPath.value.length > 0) {
      database = curDbPath.value;
    }

    if (database === undefined) {
      console.error("Database not specified and curDbPath is empty");
      return;
    }

    const response = await axios.get(`/api/db/${database}/select`);
    tableData.value = response.data.data;
    updateCategoryCounts();
  } catch (error) {
    console.error("Error fetching table data:", error);
  }
};

// 开始定时获取数据
const startFetchingData = () => {
  intervalId.value = setInterval(fetchTableData, 1000);
};

// 停止定时获取数据
const stopFetchingData = () => {
  clearInterval(intervalId.value);
  intervalId.value = null;
};

const updateCategoryCounts = () => {
  // Reset counts
  totalPackets.value = tableData.value.length;
  totalThreats.value = 0;
  for (const category in categoryCounts.value) {
    categoryCounts.value[category] = 0;
  }

  // Update counts based on tableData
  tableData.value.forEach((item) => {
    const category = categoryMap[item.category];
    if (
      category &&
      Object.prototype.hasOwnProperty.call(categoryCounts.value, category)
    ) {
      categoryCounts.value[category]++;
      if (category !== "Normal Packets") {
        totalThreats.value++;
      }
    }
  });
};

const toggleCategorySelection = (category) => {
  const index = selectedCategories.value.indexOf(category);
  if (index > -1) {
    selectedCategories.value.splice(index, 1);
  } else {
    selectedCategories.value.push(category);
  }
};

const getCategoryClass = (category) => {
  let className =
    "list-group-item d-flex justify-content-between align-items-center";
  if (warningCategories.includes(category)) {
    className += " list-group-item-warning";
  } else if (dangerCategories.includes(category)) {
    className += " list-group-item-danger";
  } else {
    className += " list-group-item-primary";
  }
  if (selectedCategories.value.includes(category)) {
    className += " active";
  }
  return className;
};

const getCategoryBadgeClass = (category) => {
  let className = "badge rounded-pill";
  if (warningCategories.includes(category)) {
    className += " bg-warning";
  } else if (dangerCategories.includes(category)) {
    className += " bg-danger";
  } else {
    className += " bg-primary";
  }
  return className;
};

const getCategoryEntryClass = (category) => {
  const normalCategories = [-1, 0];
  const warningCategories = [1, 2, 3];
  const dangerCategories = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13];

  const numericCategory = Number(category);

  if (normalCategories.includes(numericCategory)) {
    return "badge rounded-pill bg-primary";
  } else if (warningCategories.includes(numericCategory)) {
    return "badge rounded-pill bg-warning";
  } else if (dangerCategories.includes(numericCategory)) {
    return "badge rounded-pill bg-danger";
  } else {
    return "";
  }
};

const setCurrentEntry = (entry) => {
  // console.log("Setting current entry: ", entry);
  store.dispatch("updateCurrentEntry", entry);
};

// 在组件创建时获取初始数据（如果 curDbPath 已经有值）
onMounted(() => {
  if (curDbPath.value) {
    fetchTableData(curDbPath.value);
  }

  // 监听事件总线的事件
  EventBus.on("fetchTableData", fetchTableData);

  // 计算有多少种类的攻击
  configedCategories.value = Object.keys(categoryCounts.value).length;

  // 初始加载时检查 isSniffing 状态
  if (isSniffing.value) {
    startFetchingData();
  }
});

// 检查准备export的时候 有没有正在使用的表，没有就alert，有就不做任何操作
const exportChecker = async () => {
  if (
    curDbPath.value === undefined ||
    curDbPath.value === null ||
    curDbPath.value.length === 0
  ) {
    alert("Please select a database table first!");
    showExportDropdown.value = false;
    console.log("curDbPath is empty:", curDbPath.value);
    return;
  }
  if (isSniffing.value) {
    alert("Please stop sniffing first!");
    showExportDropdown.value = false;
    console.log("isSniffing is true:", isSniffing.value);
    return;
  }

  showExportDropdown.value = true; // 符合条件时显示下拉菜单
  console.log("showExportDropdown set to true");
};

// 下载指定格式的文件
const exportData = async (format) => {
  if (!showExportDropdown.value) {
    alert("Please select a database table or stop sniffing first!");
    return;
  }
  try {
    const response = await axios.get(
      `/api/db/${curDbPath.value}/export/${format}`,
      {
        responseType: "blob", // Important for downloading files
      }
    );

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `${curDbPath.value}.${format}`); // 文件名 前端表名.format
    document.body.appendChild(link);
    link.click();
    link.remove();
  } catch (error) {
    console.error("Error during file export:", error);
    alert("An error occurred while exporting the file.");
  }
};

// 移除事件监听器
onBeforeUnmount(() => {
  EventBus.off("fetchTableData", fetchTableData);
  stopFetchingData();
});

// 监听 curDbPath 和 isSniffing 的变化
watch(curDbPath, (newDbPath) => {
  if (newDbPath) {
    fetchTableData(newDbPath);
  }
});

watch(isSniffing, (newVal) => {
  if (newVal) {
    startFetchingData();
  } else {
    stopFetchingData();
  }
});
</script>

<style lang="scss" scoped>
.bi {
  display: inline-block;
  width: 1rem;
  height: 1rem;
}

/*
 * Sidebar
 */

// make sidebar sticky and scroolable
.sidebar {
  position: -webkit-fixed;
  position: fixed;
  overflow-y: auto;
}

@media (min-width: 768px) {
  .sidebar .offcanvas-lg {
    position: -webkit-fixed;
    position: fixed;
  }
}

.sidebar .nav-link {
  font-size: 0.875rem;
  font-weight: 500;
}

.sidebar .nav-link.active {
  color: #2470dc;
}

.sidebar-heading {
  font-size: 0.75rem;
}

#info {
  display: flex;
  flex-direction: column;
  align-items: center;

  a {
    padding: 0 0.6rem;
  }
}
#info > * {
  margin: 10px 0; /* 为每个子元素添加垂直间距 */
  padding: 0 15px;
}

// nice hr
hr.fancy-line {
  border: 0;
  height: 1px;
  background-image: -webkit-linear-gradient(
    left,
    rgba(0, 0, 0, 0),
    rgba(215, 215, 215, 0.75),
    rgba(0, 0, 0, 0)
  );
  background-image: -moz-linear-gradient(
    left,
    rgba(0, 0, 0, 0),
    rgba(215, 215, 215, 0.75),
    rgba(0, 0, 0, 0)
  );
  background-image: -ms-linear-gradient(
    left,
    rgba(0, 0, 0, 0),
    rgba(215, 215, 215, 0.75),
    rgba(0, 0, 0, 0)
  );
  background-image: -o-linear-gradient(
    left,
    rgba(0, 0, 0, 0),
    rgba(215, 215, 215, 0.75),
    rgba(0, 0, 0, 0)
  );
  box-shadow: 0px -2px 4px rgba(136, 136, 136, 0.75);
}

// sidebar height
#app > div.layout > div > div > div {
  height: 100%;
}

// Main: Table View
$total-width: 1000px;

// column, Category, Source IP, Source Port, Destination IP, Destination Port, Time, Request Method, Request URI, HTTP Version, Header, Body
$column-widths: (
  30px,
  30px,
  75px,
  50px,
  75px,
  50px,
  110px,
  50px,
  90px,
  50px,
  195px,
  195px
);

@function to-percentage($px) {
  @return calc($px / $total-width) * 100%;
  // @return math.div($px, $total-width); // has math pkg problem
}

table th,
table td {
  word-wrap: break-word; /* Ensures content will wrap within the cell */
  white-space: normal; /* Allows wrapping */
  width: 100px; /* Default fixed width for each column */
}

@for $i from 1 through length($column-widths) {
  th:nth-child(#{$i}),
  td:nth-child(#{$i}) {
    width: to-percentage(nth($column-widths, $i));
  }
}

table {
  table-layout: fixed; // Ensures table layout is fixed
  width: 100%; // Ensures the table takes up the full width of the container

  th,
  td {
    word-wrap: break-word; // Ensures content will wrap within the cell
    white-space: normal; // Allows wrapping
    overflow: hidden; // Hide overflow content
    text-overflow: ellipsis; // Adds ellipsis for overflow content
  }
}

@for $i from 1 through length($column-widths) {
  th:nth-child(#{$i}),
  td:nth-child(#{$i}) {
    width: to-percentage(nth($column-widths, $i));
  }
}

$primary-color: #78c2ad;

/* Table style */
tbody tr {
  transition: all 0.3s ease;

  &:hover {
    // font-weight: bold;
    filter: brightness(90%);
  }
}

/* Sidebar hover */
.list-group-item {
  transition: all 0.3s ease;
  &:hover {
    font-weight: bold;
    filter: brightness(90%);
  }
}

/* No margin for quote */
#info > figure > figcaption {
  margin-bottom: 0;
}

td span {
  font-weight: bolder;
}

.dropdown-menu {
  width: 100px !important;
  min-width: auto; /* 取消 Bootstrap 默认最小宽度 */
  position: absolute;
  inset: 0px auto auto 0px;
  margin: 0px;
  transform: translate3d(0px, 40px, 0px);
}

.offcanvas-custom {
  width: 50%; /* 设置offcanvas的宽度 */
  height: 100%;
}

// Export svg styles
#export polyline,
#export path,
#export line {
  fill: none;
  stroke: currentColor;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 1.5;
}
</style>
