<template>
  <!-- Database dropdown -->
  <li class="nav-item dropdown">
    <a
      class="nav-link dropdown-toggle"
      data-bs-toggle="dropdown"
      href="#"
      role="button"
      aria-haspopup="true"
      aria-expanded="false"
      >Database</a
    >
    <div class="dropdown-menu">
      <a
        class="dropdown-item"
        href="#"
        data-bs-toggle="modal"
        data-bs-target="#dbInfoModal"
        >Database Info</a
      >
      <div class="dropdown-divider"></div>
      <a
        class="dropdown-item"
        href="#"
        data-bs-toggle="modal"
        data-bs-target="#createDBModal"
        >Create Database</a
      >
      <a
        class="dropdown-item"
        href="#"
        data-bs-toggle="modal"
        data-bs-target="#switchDBModal"
        >Switch Database</a
      >
      <div class="dropdown-divider"></div>
      <a
        class="dropdown-item"
        href="#"
        data-bs-toggle="modal"
        data-bs-target="#emptyDBModal"
        >Empty Database</a
      >
      <a
        class="dropdown-item"
        href="#"
        data-bs-toggle="modal"
        data-bs-target="#deleteDBModal"
        >Delete Database</a
      >
    </div>
  </li>

  <!-- Database Modals -->
  <!-- Check Database Info Modal -->
  <div
    class="modal fade"
    id="dbInfoModal"
    data-bs-backdrop="static"
    data-bs-keyboard="false"
    tabindex="-1"
    aria-labelledby="dbInfoModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="dbInfoModalLabel">
            Current Database Information
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
          <p>The using table: {{ curDbPath }}</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-success" data-bs-dismiss="modal">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Create Database Modal -->
  <div
    class="modal fade"
    id="createDBModal"
    data-bs-backdrop="static"
    data-bs-keyboard="false"
    tabindex="-1"
    aria-labelledby="createDBModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="createDBModalLabel">Create Database</h5>
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
          <input
            type="text"
            class="form-control form-control-dark"
            v-model="newDatabaseName"
            placeholder="Enter database name"
          />
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button
            type="button"
            class="btn btn-primary"
            data-bs-dismiss="modal"
            @click="createDB"
          >
            Create
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Switch Database Modal -->
  <div
    class="modal fade"
    id="switchDBModal"
    data-bs-backdrop="static"
    data-bs-keyboard="false"
    tabindex="-1"
    aria-labelledby="switchDBModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="switchDBModalLabel">Switch Database</h5>
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
            <label for="dbSelect" class="form-label">Select Database</label>
            <select
              multiple
              class="form-select"
              id="dbSelect"
              style="height: 300px"
              v-model="selectedDatabase"
            >
              <option v-for="db in databases" :key="db">{{ db }}</option>
            </select>
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
          <button
            type="button"
            class="btn btn-primary"
            data-bs-dismiss="modal"
            @click="switchDB"
          >
            Switch
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Empty Database Modal -->
  <div
    class="modal fade"
    id="emptyDBModal"
    data-bs-backdrop="static"
    data-bs-keyboard="false"
    tabindex="-1"
    aria-labelledby="emptyDBModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title text-danger" id="emptyDBModalLabel">
            Empty Database
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
          <p class="text-danger">
            ❗️Are you sure to empty the current database?❗️
          </p>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button
            type="button"
            class="btn btn-danger"
            data-bs-dismiss="modal"
            @click="emptyDB"
          >
            Empty
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Delete Database Modal -->
  <div
    class="modal fade"
    id="deleteDBModal"
    data-bs-backdrop="static"
    data-bs-keyboard="false"
    tabindex="-1"
    aria-labelledby="deleteDBModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title text-danger" id="deleteDBModalLabel">
            Delete Database
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
          <p class="text-danger">
            ❗️Are you sure to delete the current database?❗️
          </p>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button
            type="button"
            class="btn btn-danger"
            data-bs-dismiss="modal"
            @click="deleteDB"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapActions, mapGetters } from "vuex";
import { EventBus } from "@/eventBus";

export default {
  name: "DataBase",
  data() {
    return {
      newDatabaseName: "", // 新数据库名输入
      selectedDatabase: "", // 选中的数据库
      databases: [], // 数据库列表
    };
  },
  created() {
    this.fetchDBInfo(); // 组件创建时获取数据库信息
  },
  computed: {
    ...mapGetters(["curDbPath"]), // 从 Vuex 获取当前数据库路径
  },
  methods: {
    ...mapActions(["updateCurDbPath"]), // 从 Vuex 引入更新数据库路径的方法

    // 获取数据库信息
    async fetchDBInfo() {
      try {
        // 获取当前有哪些表
        const response = await axios.get("/api/db/info");
        this.databases = response.data.tables;
        console.log("Database info:", response.data);

        // 获取当前正在使用的表名
        const response2 = await axios.get("/api/db/cur_db");
        this.updateCurDbPath(response2.data.table_name); // 更新 Vuex 中的 cur_db_path
        console.log("Current database:", response2.data);
      } catch (error) {
        console.error("Error fetching database info:", error);
      }
    },

    // 创建新数据库
    async createDB() {
      try {
        const response = await axios.post("/api/db/create", {
          time: this.newDatabaseName,
        });
        console.log("Create database response:", response.data);
        if (response.data.status === "200") {
          alert(response.data.message);
          await this.fetchDBInfo(); // 更新数据库列表
        }
      } catch (error) {
        console.error("Error creating database:", error);
        if (error.response && error.response.status === 400) {
          // 提取并显示错误信息
          const errorMessage = error.response.data.error;
          alert(`Error: ${errorMessage}`);
        } else {
          alert("An unexpected error occurred");
        }
      }
    },

    // 切换数据库
    async switchDB() {
      try {
        const response = await axios.post("/api/db/use", {
          table_name: this.selectedDatabase,
        });
        console.log("Switch database response:", response.data);
        if (response.data.status === "200") {
          alert("Database switched successfully");
          await this.fetchDBInfo(); // 更新数据库信息
        } else {
          alert("Error switching database");
        }
      } catch (error) {
        console.error("Error switching database:", error);
      }
    },

    // 清空数据库
    async emptyDB() {
      try {
        // TODO: empty database
        const response = await axios.get(`/api/db/${this.curDbPath}/clean`);
        console.log("Empty database response:", response.data);
        if (response.data.status === "200") {
          alert("Database emptied successfully");
          // 刷新页面
          // window.location.reload();
          // 触发数据重新加载事件
          EventBus.emit("fetchTableData", this.curDbPath);
        } else {
          alert("Error emptying database");
        }
      } catch (error) {
        console.error("Error emptying database:", error);
      }
    },

    // 删除数据库（功能待实现）
    async deleteDB() {
      try {
        // TODO: delete database
        // const response = await axios.post("/api/db/delete");
        // if (response.data.success) {
        //   alert("Database deleted successfully");
        // } else {
        //   alert("Error deleting database");
        // }
      } catch (error) {
        console.error("Error deleting database:", error);
      }
    },
  },
};
</script>

<style lang="scss" scoped>
// Navbar styling
.nav-link {
  color: white;
  font-weight: bold;
  width: auto;

  &:hover {
    color: darken(#a2e5d2, 10%);
    text-decoration: underline;
  }
}

#navbarColor01 > ul > li:nth-child(1) > a {
  padding-left: 20px;
}

.navbar-toggler {
  border: none;

  &:focus {
    outline: none;
    box-shadow: none;
  }
}

// drop-down menu
.dropdown-menu.show {
  margin-top: 29px;
  margin-left: 5px;
  width: auto;
  border-radius: 0;
}

// font
.container-fluid {
  font-family: "Montserrat", serif !important;
}

// Modals
.modal-backdrop {
  --bs-backdrop-zindex: 1; /* or any other desired value */
}

.modal {
  z-index: var(--bs-backdrop-zindex) + 10 !important;
}

// Dropdown
#navbarCollapse > ul > li:nth-child(1) > div {
  margin-top: 12px;
  margin-left: 0;
  border-left-width: 0;
  border-right-width: 0;
  margin-right: 0;
}

#navbarCollapse > ul > li:nth-child(1) > div {
  border-left-width: 1px;
  border-right-width: 1px;
}

// Hove to trigger dropdown
</style>
