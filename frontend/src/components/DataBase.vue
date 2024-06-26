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
          <p>The database path: {{ cur_db_path }}</p>
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
            id="databaseName"
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
            <label for="exampleSelect2" class="form-label"
              >Example multiple select</label
            >
            <select
              multiple=""
              class="form-select"
              id="exampleSelect2"
              style="height: 300px"
            >
              <option>db1</option>
              <option>db2</option>
              <option>db3</option>
              <option>db4</option>
              <option>db5</option>
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
            ❗️Are you sure to empty the current dabatase?❗️
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
export default {
  name: "DataBase",
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
