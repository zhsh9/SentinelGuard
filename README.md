<p align="center">
<img src="./frontend/src/assets/logo-font2.png" alt="logo" style="width:300px; height: auto">
</p>
<p align="center"><i>An Integrated Real-time HTTP Intrusion Detection System.</i></p>
<div align="center">
  <a href="https://github.com/zhsh9/SentinelGuard/stargazers"><img src="https://img.shields.io/github/stars/zhsh9/SentinelGuard" alt="Stars Badge"/></a>
<a href="https://github.com/zhsh9/SentinelGuard/network/members"><img src="https://img.shields.io/github/forks/zhsh9/SentinelGuard" alt="Forks Badge"/></a>
<a href="https://github.com/zhsh9/SentinelGuard/pulls"><img src="https://img.shields.io/github/issues-pr/zhsh9/SentinelGuard" alt="Pull Requests Badge"/></a>
<a href="https://github.com/zhsh9/SentinelGuard/issues"><img src="https://img.shields.io/github/issues/zhsh9/SentinelGuard" alt="Issues Badge"/></a>
<a href="https://github.com/zhsh9/SentinelGuard/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/zhsh9/SentinelGuard?color=2b9348"></a>
<a href="https://github.com/zhsh9/SentinelGuard/blob/master/LICENSE"><img src="https://img.shields.io/github/license/zhsh9/SentinelGuard?color=2b9348" alt="License Badge"/></a>
</div>

## Installation

- Flask3, Vue3, Bootstrap 5.3.3

```bash
cd frontend; yarn install
cd backend; pip install -r requirement.txt
```

## Configuration

- Backend: `./backend/config.py`
- Frontend: `./frontend/vue.config.js`

## Usage

```bash
python backend/app.py
cd frontend; npm run serve
cd frontend; yarn serve
```

## To-Do

- [x] Export function (csv, pcap)
- [x] Environment checking script
- [ ] release v0.0.2 publish
- [ ] uploading pcap: support zip & tar with multiple pcap files
- [ ] backend: drop table by name, drop all tables
- [ ] backend: update http record category using id
- [ ] backend & frontend: update frontend_tb_name
- [ ] frontend: design webpage for managing whitelist & blacklist
- [ ] frontend: design webpage for managing detection rules

## Screenshot

<table style="width: 100%;">
  <tr>
    <td style="width: 50%; text-align: center;">
      <img src="./static/login.jpeg" alt="Login Page" style="max-height: 200px; width: auto;" />
      <p>Login Page</p>
    </td>
    <td style="width: 50%; text-align: center;">
      <img src="./static/upload.jpeg" alt="Upload Page" style="max-height: 200px; width: auto;" />
      <p>Upload Page</p>
    </td>
  </tr>
  <tr>
    <td style="width: 50%; text-align: center;">
      <img src="./static/sniff.jpeg" alt="Sniff Page" style="max-height: 200px; width: auto;" />
      <p>Sniff Page</p>
    </td>
    <td style="width: 50%; text-align: center;">
      <img src="./static/stop_sniff.jpeg" alt="Stop Sniff Page" style="max-height: 200px; width: auto;" />
      <p>Stop Sniff Page</p>
    </td>
  </tr>
  <tr>
    <td style="width: 50%; text-align: center;">
      <img src="./static/dashboard_light.png" alt="Dashboard Light Theme" style="max-height: 200px; width: auto;" />
      <p>Dashboard Light Theme</p>
    </td>
    <td style="width: 50%; text-align: center;">
      <img src="./static/dashboard_dark.png" alt="Dashboard Dark Theme" style="max-height: 200px; width: auto;" />
      <p>Dashboard Dark Theme</p>
    </td>
  </tr>
</table>