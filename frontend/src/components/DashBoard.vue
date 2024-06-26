<template>
  <div class="container-fluid">
    <div class="row">
      <div
        class="sidebar border border-right col-md-4 col-lg-3 p-0 bg-body-tertiary rounded-bottom"
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
              <span class="badge bg-primary rounded-pill">2</span>
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
              Common Vulnerabilities and Exposures
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

      <main class="ms-sm-auto col-md-8 col-lg-9 px-md-4">
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
                <th scope="col">Source IP</th>
                <th scope="col">Src Port</th>
                <th scope="col">Destination IP</th>
                <th scope="col">Dst Port</th>
                <th scope="col">Timestamp</th>
                <th scope="col">Method</th>
                <th scope="col">Request URI</th>
                <th scope="col">HTTP Version</th>
                <th scope="col">Header</th>
                <th scope="col">Body</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>1</td>
                <td>192.168.100.100</td>
                <td>12345</td>
                <td>192.168.100.200</td>
                <td>80</td>
                <td>2024-06-26 10:00:00</td>
                <td>GET</td>
                <td>/home</td>
                <td>HTTP/1.1</td>
                <td>Accept: */*</td>
                <td></td>
              </tr>
              <tr>
                <td>2</td>
                <td>192.168.1.3</td>
                <td>54321</td>
                <td>192.168.1.4</td>
                <td>443</td>
                <td>2024-06-26 10:05:00</td>
                <td>POST</td>
                <td>/api/data</td>
                <td>HTTP/2</td>
                <td>Content-Type: application/json</td>
                <td>{"key":"value"}</td>
              </tr>
              <tr>
                <td>3</td>
                <td>10.0.0.1</td>
                <td>8080</td>
                <td>10.0.0.2</td>
                <td>80</td>
                <td>2024-06-26 10:10:00</td>
                <td>PUT</td>
                <td>/update</td>
                <td>HTTP/1.1</td>
                <td>
                  Host: www.example.com User-Agent: Mozilla/5.0 (Windows NT
                  10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
                  Chrome/91.0.4472.124 Safari/537.36 Accept: application/json
                  Accept-Language: en-US,en;q=0.5 Accept-Encoding: gzip,
                  deflate, br Connection: keep-alive Content-Type:
                  application/x-www-form-urlencoded Content-Length: 27 Cookie:
                  sessionId=abc123
                </td>
                <td>{"update":"data"}</td>
              </tr>
              <tr>
                <td>4</td>
                <td>172.16.0.1</td>
                <td>9090</td>
                <td>172.16.0.2</td>
                <td>443</td>
                <td>2024-06-26 10:15:00</td>
                <td>DELETE</td>
                <td>/delete</td>
                <td>HTTP/1.1</td>
                <td>Cache-Control: no-cache</td>
                <td></td>
              </tr>
              <tr>
                <td>5</td>
                <td>192.168.2.1</td>
                <td>9999</td>
                <td>192.168.2.2</td>
                <td>80</td>
                <td>2024-06-26 10:20:00</td>
                <td>HEAD</td>
                <td>/head</td>
                <td>HTTP/1.1</td>
                <td>User-Agent: CustomClient/1.0</td>
                <td></td>
              </tr>
              <tr>
                <td>6</td>
                <td>10.1.1.1</td>
                <td>1234</td>
                <td>10.1.1.2</td>
                <td>8080</td>
                <td>2024-06-26 10:25:00</td>
                <td>OPTIONS</td>
                <td>/options</td>
                <td>HTTP/1.1</td>
                <td>Allow: GET, POST</td>
                <td></td>
              </tr>
              <tr>
                <td>7</td>
                <td>172.16.1.1</td>
                <td>4444</td>
                <td>172.16.1.2</td>
                <td>443</td>
                <td>2024-06-26 10:30:00</td>
                <td>PATCH</td>
                <td>/patch</td>
                <td>HTTP/2</td>
                <td>Content-Type: application/json</td>
                <td>{"patch":"data"}</td>
              </tr>
              <tr>
                <td>8</td>
                <td>192.168.3.1</td>
                <td>5555</td>
                <td>192.168.3.2</td>
                <td>80</td>
                <td>2024-06-26 10:35:00</td>
                <td>TRACE</td>
                <td>/trace</td>
                <td>HTTP/1.1</td>
                <td>Referer: http://example.com</td>
                <td></td>
              </tr>
              <tr>
                <td>9</td>
                <td>10.2.2.1</td>
                <td>6666</td>
                <td>10.2.2.2</td>
                <td>8080</td>
                <td>2024-06-26 10:40:00</td>
                <td>CONNECT</td>
                <td>/connect</td>
                <td>HTTP/1.1</td>
                <td>Proxy-Authorization: Basic dXNlcjpwYXNz</td>
                <td></td>
              </tr>
              <tr>
                <td>10</td>
                <td>172.16.2.1</td>
                <td>7777</td>
                <td>172.16.2.2</td>
                <td>443</td>
                <td>2024-06-26 10:45:00</td>
                <td>GET</td>
                <td>/status</td>
                <td>HTTP/1.1</td>
                <td>Accept-Encoding: gzip</td>
                <td></td>
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
export default {
  name: "DashBoard",
  setup() {},
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
table th,
table td {
  word-wrap: break-word; /* Ensures content will wrap within the cell */
  white-space: normal; /* Allows wrapping */
  width: 100px; /* Fixed width for each column */
}
th:nth-child(1),
td:nth-child(1) {
  width: 40px;
} /* # column, smaller width */
th:nth-child(2),
td:nth-child(2) {
  width: 120px;
} /* Source IP */
th:nth-child(3),
td:nth-child(3) {
  width: 80px;
} /* Source Port */
th:nth-child(4),
td:nth-child(4) {
  width: 120px;
} /* Destination IP */
th:nth-child(5),
td:nth-child(5) {
  width: 80px;
} /* Destination Port */
th:nth-child(6),
td:nth-child(6) {
  width: 160px;
} /* Timestamp */
th:nth-child(7),
td:nth-child(7) {
  width: 100px;
} /* Request Method */
th:nth-child(8),
td:nth-child(8) {
  width: 200px;
} /* Request URI */
th:nth-child(9),
td:nth-child(9) {
  width: 100px;
} /* HTTP Version */
th:nth-child(10),
td:nth-child(10) {
  width: 400px;
} /* Header */
th:nth-child(11),
td:nth-child(11) {
  width: 200px;
} /* Body */

/* Sidebar hover */
.list-group-item {
  transition: all 0.3s ease;
}

.list-group-item:hover {
  font-weight: bold;
  filter: brightness(90%);
}
</style>
