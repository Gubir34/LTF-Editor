# LTF Editor

A simple and feature-rich editor for **LTF (Language Translation File)** format. Built with Python and Tkinter.

---

## Features

- Open, edit, and save `.ltf` files.
- **Multi-language support** with radio buttons for switching languages.
- **Key/Value editor**:
  - Edit translations directly in the right panel.
  - Preview keys and their values.
- **Search** keys and translations in real-time.
- **Toolbar buttons**:
  - New File, Open File, Save File
  - New Key, Delete Key
  - Toggle Dark/Light Mode
- **Keyboard shortcuts**:
  - `Ctrl+N` → New File
  - `Ctrl+O` → Open File
  - `Ctrl+S` → Save File
  - `Ctrl+C`, `Ctrl+V`, `Ctrl+X` for copy/paste/cut in the translation editor
- **Dark Mode** with custom background colors.
- **Right-click context menu** on keys:
  - Delete Key
  - Rename Key
  - Select/Copy Key
- Display an **icon** (`ltf.png`) in the right panel.

---

## Installation

1. Make sure you have **Python 3.10+** installed.
2. Install Tkinter (usually comes with Python):

```bash
# On Debian/Ubuntu
sudo apt install python3-tk

# On Windows
# Tkinter comes preinstalled with Python
