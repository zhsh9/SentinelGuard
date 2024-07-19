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
              <span class="badge bg-primary rounded-pill">1420</span>
            </li>
            <li
              class="list-group-item d-flex justify-content-between align-items-center"
            >
              Total Number of Threats
              <span class="badge bg-primary rounded-pill">32</span>
            </li>
            <li
              class="list-group-item d-flex justify-content-between align-items-center"
            >
              Categories Selected
              <span
                id="categories-selected"
                class="badge bg-primary rounded-pill"
                >0</span
              >
            </li>
            <li
              class="list-group-item d-flex justify-content-between align-items-center"
            >
              Time of Capturing
              <span class="badge bg-primary rounded-pill">{{
                formattedTime
              }}</span>
            </li>
          </ul>
        </div>

        <hr class="fancy-line" />

        <div id="threat-cate">
          <ul class="list-group">
            <li
              class="list-group-item list-group-item-primary d-flex justify-content-between align-items-center"
            >
              Normal Packets
              <span class="badge bg-primary rounded-pill">14</span>
            </li>
            <li
              class="list-group-item list-group-item-warning d-flex justify-content-between align-items-center"
            >
              Insecure IPs
              <span class="badge bg-primary rounded-pill">2</span>
            </li>
            <li
              class="list-group-item list-group-item-warning d-flex justify-content-between align-items-center"
            >
              Insecure Referers
              <span class="badge bg-primary rounded-pill">2</span>
            </li>
            <li
              class="list-group-item list-group-item-warning d-flex justify-content-between align-items-center"
            >
              CVEs
              <span class="badge bg-primary rounded-pill">2</span>
            </li>
            <li
              class="list-group-item list-group-item-danger d-flex justify-content-between align-items-center"
            >
              Brute Force
              <span class="badge bg-primary rounded-pill">1</span>
            </li>
            <li
              class="list-group-item list-group-item-danger d-flex justify-content-between align-items-center"
            >
              Command Injection
              <span class="badge bg-primary rounded-pill">5</span>
            </li>
            <li
              class="list-group-item list-group-item-danger d-flex justify-content-between align-items-center"
            >
              CSRF
              <span class="badge bg-primary rounded-pill">4</span>
            </li>
            <li
              class="list-group-item list-group-item-danger d-flex justify-content-between align-items-center"
            >
              File Inclusion
              <span class="badge bg-primary rounded-pill">9</span>
            </li>
            <li
              class="list-group-item list-group-item-danger d-flex justify-content-between align-items-center"
            >
              File Upload
              <span class="badge bg-primary rounded-pill">8</span>
            </li>
            <li
              class="list-group-item list-group-item-danger d-flex justify-content-between align-items-center"
            >
              Insecure CAPTCHA
              <span class="badge bg-primary rounded-pill">0</span>
            </li>
            <li
              class="list-group-item list-group-item-danger d-flex justify-content-between align-items-center"
            >
              SQL Injection
              <span class="badge bg-primary rounded-pill">0</span>
            </li>
            <li
              class="list-group-item list-group-item-danger d-flex justify-content-between align-items-center"
            >
              SQL Injection (Blind)
              <span class="badge bg-primary rounded-pill">0</span>
            </li>
            <li
              class="list-group-item list-group-item-danger d-flex justify-content-between align-items-center"
            >
              XSS (Reflected)
              <span class="badge bg-primary rounded-pill">0</span>
            </li>
            <li
              class="list-group-item list-group-item-danger d-flex justify-content-between align-items-center"
            >
              XSS (Stored)
              <span class="badge bg-primary rounded-pill">0</span>
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
            <div class="btn-group me-2">
              <button type="button" class="btn btn-sm btn-outline-secondary">
                Share
              </button>
              <button type="button" class="btn btn-sm btn-outline-secondary">
                Export
              </button>
            </div>
            <button
              type="button"
              class="btn btn-sm btn-outline-secondary dropdown-toggle d-flex align-items-center gap-1"
            >
              <svg class="bi"><use xlink:href="#calendar3" /></svg>
              This week
            </button>
          </div>
        </div>

        <div class="table-responsive small">
          <table class="table table-striped table-sm">
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
              <tr v-for="(entry, index) in tableData" :key="entry.id">
                <td>{{ index + 1 }}</td>
                <td>{{ entry.category }}</td>
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
    </div>
  </div>
</template>

<script setup>
// import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";
import { computed, inject } from "vue";

const timerStore = inject("timerStore");

const formattedTime = computed(() => {
  const minutes = Math.floor(timerStore.time.value / 60);
  const seconds = timerStore.time.value % 60;
  return `${minutes}:${seconds.toString().padStart(2, "0")}`;
});
</script>

<script>
// export default {
//   name: "DashBoard",
//   setup() {},
// };

import axios from "axios";
import { mapGetters } from "vuex";
import { EventBus } from "@/eventBus";

export default {
  name: "DashBoard",
  data() {
    return {
      tableData: [], // 表格数据
    };
  },
  created() {
    // 在组件创建时获取初始数据（如果 curDbPath 已经有值）
    if (this.curDbPath) {
      this.fetchTableData(this.curDbPath);
    }
    // 监听事件总线的事件
    EventBus.on("fetchTableData", this.fetchTableData);
  },
  beforeUnmount() {
    // 移除事件监听器
    EventBus.off("fetchTableData", this.fetchTableData);
  },
  computed: {
    ...mapGetters(["curDbPath"]),
  },
  watch: {
    // 监听 cur_db_path 的变化
    curDbPath(newDbPath) {
      if (newDbPath) {
        this.fetchTableData(newDbPath);
      }
    },
  },
  methods: {
    // 获取选中数据库表的数据
    async fetchTableData(database) {
      try {
        const response = await axios.get(`/api/db/${database}/select`);
        this.tableData = response.data.data;
      } catch (error) {
        console.error("Error fetching table data:", error);
      }
    },
  },
};
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
  position: -webkit-sticky;
  position: sticky;
  // top: 48px;
  // height: calc(100vh - 48px);
  overflow-y: auto;
}

@media (min-width: 768px) {
  .sidebar .offcanvas-lg {
    position: -webkit-sticky;
    position: sticky;
    // top: 48px;
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

$column-widths: (
  30px,
  // column
  30px,
  // Category
  75px,
  // Source IP
  50px,
  // Source Port
  75px,
  // Destination IP
  50px,
  // Destination Port
  110px,
  // Time
  50px,
  // Request Method
  90px,
  // Request URI
  50px,
  // HTTP Version
  195px,
  // Header
  195px // Body
);

@function to-percentage($px) {
  @return $px / $total-width * 100%; // math pkg problem
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
</style>
