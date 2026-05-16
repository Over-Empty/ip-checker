[نسخه فارسی توضیحات](README_Fa.md) 
# 🔍 IP Ping Checker Pro 🌞🦁

A fast multi-threaded IP checker that extracts IP addresses from text, files, or direct input, pings them simultaneously, and shows which IPs are online or offline.

The tool also supports copying active IPs directly to the clipboard.

---

# ✨ Features

- Automatic IP extraction from text, files, or direct input
- Fast multi-threaded IP checking
- Displays online and offline IPs separately
- Supports Windows, Linux, and Termux
- Lightweight and portable
- No required external dependencies
- Optional clipboard support

---

# 📦 Requirements

- Python 3.8 or higher
- Git

## Optional Clipboard Support

To enable automatic clipboard copy:

```bash
pip install pyperclip
```

Or place `pyperclip.py` inside the `libs` folder.

---

# 🪟 Installation & Usage on Windows

## 1. Install Python

Download from:

https://www.python.org/downloads/

During installation, make sure to enable:

```text
Add Python to PATH
```

---

## 2. Install Git

Download from:

https://git-scm.com/download/win

You can keep all installation options as default.

---

## 3. Open CMD

Search for:

```text
cmd
```

from the Windows Start Menu.

---

## 4. Clone the Project

```bash
git clone https://github.com/Over-Empty/ip-checker.git
```

---

## 5. Enter the Project Directory

```bash
cd ip-checker
```

---

## 6. Install Clipboard Support (Optional)

```bash
pip install pyperclip
```

---

## 7. Run the Program

```bash
python main.py
```

---

## Run with File Input

```bash
python main.py ips.txt
```

---

# 🐧 Installation & Usage on Linux

## Ubuntu / Debian

```bash
sudo apt update
sudo apt install python3 python3-pip git -y
```

---

## Arch Linux

```bash
sudo pacman -S python python-pip git
```

---

## Clone the Project

```bash
git clone https://github.com/Over-Empty/ip-checker.git
```

---

## Enter the Project Directory

```bash
cd ip-checker
```

---

## Install Clipboard Support (Optional)

```bash
pip install pyperclip
```

---

## Run the Program

```bash
python3 main.py
```

---

## Run with File Input

```bash
python3 main.py ips.txt
```

---

# 📱 Installation & Usage on Termux (Android)

## 1. Install Python and Git

```bash
pkg update -y
pkg install python git -y
```

---

## 2. Clone the Project

```bash
git clone https://github.com/Over-Empty/ip-checker.git
```

---

## 3. Enter the Project Directory

```bash
cd ip-checker
```

---

## 4. Install Clipboard Support (Optional)

```bash
pip install pyperclip
```

---

## 5. Run the Program

```bash
python main.py
```

---

## Run with File Input

```bash
python main.py ips.txt
```

---

# 📋 Notes

- This tool uses the system's built-in `ping` command
- No external API or internet service is required
- Performance depends on your system and network
- Clipboard functionality works only if clipboard support is available

---

# ⚠️ Termux Notes

If clipboard functionality does not work in Termux:

```bash
termux-setup-storage
```

Then restart Termux once.

---

# 📄 License

This project is released under the MIT License.

You are free to use, modify, and distribute it, but crediting the original author is appreciated.

---

# 👨‍🍳 Author

AI Chef Empty 🫙

🌞🦁
