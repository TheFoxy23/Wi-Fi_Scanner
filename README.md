# 🔍 Network Scanner with GUI

A modern, elegant, and beginner-friendly IP/Port network scanner with a custom GUI.  
Built using **Python** and **Tkinter**, with enhanced visuals and a loading screen.

---

## 🚀 Features

- ✨ Loading screen with animated progress bar and custom background
- 🖼️ Background images and graphical interface designed in Photopea
- ✅ IP reachability check (Ping)
- 🌐 Hostname resolution
- 🔓 Common port scanning (22, 80, 443, 8080)
- 📜 Real-time terminal-like output
- 💾 Saves scan results in timestamped `.json` files
- 🖥️ Fixed-size non-resizable window
- 🎨 Gradient styling and custom "Scan" button color

---

## 🧪 Technologies Used

- **Python 3**
- **Tkinter** – GUI library
- **socket**, **subprocess**, **ipaddress** – for networking
- **PIL (Pillow)** – image support in Tkinter
- **Visual Studio Code** – development environment
- **GitHub Copilot** – code suggestion and error correction
- **Photopea** – for custom background, logo and UI elements

---

## 🎯 Project Goals

- Create a simple and good-looking Python GUI project for network diagnostics
- Combine network functionality (ping + port scan) in a single visual interface
- Learn to manage threads, progress bars and file outputs with Python
- Experiment with GUI design: custom loading screen, styles and background images

---

## 🌱 Future Features

- 🔍 Add custom port range selection (e.g., 1–65535)
- 💡 Light/Dark mode toggle
- 📂 Option to export results in `.txt` or `.csv` as well
- 🧠 Basic fingerprinting (OS detection or MAC vendor via ARP)
- 🛜 WiFi network scanner version (using `scapy`)

---

## 🛠️ How to Run

1. Clone the repository:

```bash
git clone https://github.com/yourusername/network-scanner-gui.git
cd network-scanner-gui
```
2. Install dependecies (reccomended: use a virtual environment)
```bash
pip3 install pillow
```
Pillow is required for image handling. Tkinter is built-in with most Python distributions.
3. Run the app:
```bash
python3 network_scanner_gui.py
```
Make sure your assets/ folder contains:
loading_background.png
logo.png

scribble dribble