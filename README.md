# 💡 Interactive Pull-Cord Light Bulb (Python Tkinter)

An interactive desktop GUI simulation built with **Python** and **Tkinter**, featuring a custom vector-drawn light bulb with a realistic spring-loaded pull cord. Drag the wire downward with your mouse to toggle the bulb **ON** with a warm ambient glow, and pull it down again to switch it **OFF**.

---

## ✨ Features

- **Interactive Drag-to-Toggle Physics:** Click and drag the pull wire downward past the threshold to switch the bulb ON or OFF.
- **Smooth Spring-Back Animation:** Releasing the mouse button smoothly snaps the cord back to its resting position.
- **Dynamic Lighting & Glow Effects:** Features multi-layered radial glow rings, an illuminated filament, and glass highlight reflections when powered ON.
- **Zero External Dependencies:** Built 100% using Python's standard `tkinter` library—no external images or third-party packages required.

---

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **GUI Framework:** Tkinter (`Canvas` vector graphics & mouse event bindings)

---

## 📂 Project Structure

```text
bulb-pull-toggle/
├── main.py       # Core application logic, Canvas drawing, and drag-physics engine
└── README.md     # Project documentation