# 📡 NetWatch Pro

```{=html}
<p align="center">
```
`<img src="your-demo-image.png" width="900" alt="NetWatch Pro Demo Screenshot">`{=html}
```{=html}
</p>
```
```{=html}
<p align="center">
```
`<strong>`{=html}Real-Time Camera Monitoring
System`</strong>`{=html}`<br>`{=html} `<em>`{=html}Educational CCTV
Architecture Simulation`</em>`{=html}
```{=html}
</p>
```

------------------------------------------------------------------------

```{=html}
<p align="center">
```
`<img src="https://img.shields.io/badge/Version-v1.0.3-1677ff?style=for-the-badge" />`{=html}
`<img src="https://img.shields.io/badge/Status-Educational-22c55e?style=for-the-badge" />`{=html}
`<img src="https://img.shields.io/badge/Backend-Flask-black?style=for-the-badge" />`{=html}
`<img src="https://img.shields.io/badge/Frontend-React%2018-61dafb?style=for-the-badge" />`{=html}
`<img src="https://img.shields.io/badge/WebSocket-Socket.IO-orange?style=for-the-badge" />`{=html}
```{=html}
</p>
```

------------------------------------------------------------------------

## 🧠 About The Project

**NetWatch Pro** is a lightweight real-time camera streaming system
built to understand how CCTV and IP camera systems work internally.

This project simulates:

-   🎥 Camera capture\
-   🔁 Live frame transmission\
-   🖥 Real-time monitoring\
-   🔐 Basic authentication\
-   🌍 Global sharing via Cloudflare Tunnel

> This is an educational prototype --- not a production CCTV system.

------------------------------------------------------------------------

## 🚀 Release Information

  Field             Value
  ----------------- -----------------------------------
  📦 Version        **v1.0.3**
  👨‍💻 Owner          **Kanchan Maji**
  🌐 Website        https://kanchanmaji.in
  📅 Release Year   2026
  🎯 Objective      Learn CCTV Streaming Architecture

------------------------------------------------------------------------

## ⚙️ How It Works

1.  Browser captures live video using `getUserMedia()`
2.  Frames are drawn to a hidden `<canvas>`
3.  Converted into base64 JPEG format
4.  Sent to backend using WebSocket
5.  Flask broadcasts frames to monitor clients
6.  Monitor renders frames in real-time

------------------------------------------------------------------------

## 🛠 Tech Stack

-   Python 3
-   Flask
-   Flask-SocketIO
-   React 18 (CDN)
-   Ant Design
-   Socket.IO
-   HTML5 MediaDevices API
-   Cloudflare Tunnel

------------------------------------------------------------------------

# 📦 Installation

## 1️⃣ Clone Repository

``` bash
git clone https://github.com/yourusername/netwatch-pro.git
cd netwatch-pro
```

------------------------------------------------------------------------

## 2️⃣ Create Virtual Environment

``` bash
python -m venv venv
```

Activate:

Linux / Mac:

``` bash
source venv/bin/activate
```

Windows:

``` bash
venv\Scripts\activate
```

------------------------------------------------------------------------

## 3️⃣ Install Dependencies

``` bash
pip install flask flask-socketio
```

For Windows:

``` bash
pip install eventlet
```

------------------------------------------------------------------------

# ▶ Running The Application

``` bash
python app.py
```

------------------------------------------------------------------------

# 🌍 Global Sharing with Cloudflare Tunnel

Install Cloudflared and run:

``` bash
cloudflared tunnel --url http://localhost:5000
```

You will receive a public HTTPS URL to share globally.

------------------------------------------------------------------------

# 👨‍💻 Author

**Kanchan Maji**\
Software Developer & Technology Explorer

🌐 https://kanchanmaji.in

------------------------------------------------------------------------

# 📄 License

MIT License\
Open-source for educational use.
