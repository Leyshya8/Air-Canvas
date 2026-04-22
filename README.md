# ✋ Air Canvas — Real-Time Gesture-Based Drawing

> Draw in the air using only your hand. No stylus, no touch screen — just a webcam.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10%2B-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

Air Canvas is a computer vision application that transforms a standard webcam into a virtual drawing board. It uses **MediaPipe** for high-fidelity hand landmark detection and **OpenCV** for real-time frame processing and canvas overlay.

---

## 📸 Demo

> *(Add a GIF or screenshot here — e.g., `docs/demo.gif`)*

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Gesture Reference](#gesture-reference)
- [Project Structure](#project-structure)
- [Known Limitations](#known-limitations)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

- **Hand Gesture Recognition** — Detects hand landmarks in real time using MediaPipe.
- **Selection Mode** _(2 fingers up)_ — Navigate the top toolbar to pick colors (Blue, Green, Red, Yellow), activate the Eraser, or clear the canvas.
- **Drawing Mode** _(1 finger up)_ — Draw smooth, continuous strokes in the active color.
- **Eraser Tool** — Select from the toolbar and paint over strokes to erase.
- **Live Canvas Overlay** — Uses bitwise operations to merge the persistent drawing layer onto the live webcam feed without flickering.
- **Visual HUD** — On-screen display of current tool, color, and mode at all times.

---

## 🛠 Tech Stack

| Component       | Library / Tool              |
|-----------------|-----------------------------|
| Language        | Python 3.10+ *(3.14.4 latest)*      |
| Computer Vision | OpenCV (`cv2`)              |
| Hand Tracking   | MediaPipe (`Hands` module)  |
| State Management| Deques & Dictionaries       |

---

## ✅ Prerequisites

Ensure the following are installed before proceeding:

- Python **3.10** or higher *(3.13 / 3.14 recommended — 3.8 and 3.9 are EOL)*
- A working **webcam**
- `pip` package manager

---

## 🚀 Installation

```bash
# 1. Clone the repository
git clone https://github.com/Leyshya8/Air-Canvas.git
cd Air-Canvas

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install opencv-python mediapipe
```

> **Note:** On some systems you may need `opencv-python-headless` instead of `opencv-python` if running without a display.

---

## ▶️ Usage

```bash
python air-canvas.py
```

1. Allow webcam access when prompted.
2. Your webcam feed will open with the toolbar visible at the top.
3. Use the gestures below to interact.
4. Press **`Q`** to exit.

---

## 🤚 Gesture Reference

| Gesture                   | Action                                              |
|---------------------------|-----------------------------------------------------|
| ☝️ **1 finger up**        | Drawing mode — move finger to draw on the canvas    |
| ✌️ **2 fingers up**       | Selection mode — hover over toolbar buttons         |
| Hover over color button   | Switch active drawing color                         |
| Hover over **Eraser**     | Switch to eraser tool                               |
| Hover over **Clear**      | Reset the entire canvas                             |

---

## 📁 Project Structure

```
Air-Canvas/
├── air-canvas.py       # Main application entry point
├── README.md           # Project documentation
└── docs/               # (Optional) Screenshots and demo assets
```

---

## ⚠️ Known Limitations

- Performance may degrade in **low-light** conditions — ensure adequate lighting for reliable hand detection.
- Optimized for **single-hand** use; multi-hand scenarios are not explicitly handled.
- Webcam resolution directly impacts tracking accuracy; **720p or higher** is recommended.
- No persistent canvas saving — drawings are lost on exit (press `Q`).

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

Please open an issue first for significant changes to discuss the approach.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
