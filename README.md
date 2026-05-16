[نسخه فارسی توضیحات](README_Fa.md) 

🔍 IP Ping Checker Pro

A fast, multi-threaded IP checker tool that extracts IP addresses from input text, pings them concurrently, and shows which IPs are online or offline. It also supports clipboard copying for active IPs.


---

✨ Features

Automatic IP extraction from text, files, or input

Multi-threaded ping checker (fast scanning)

Cross-platform support (Windows / Linux / Termux)

Lightweight and dependency-free (except optional clipboard support)



---

📦 Requirements

Python 3.8+

Optional (for clipboard support):
```
pip install pyperclip
```

---

🚀 Installation

📌 1. Clone the repository

```
git clone https://github.com/your-username/ip-ping-checker.git
cd ip-ping-checker
```

---

🪟 Windows Setup & Run

▶ Run directly:
```
python main.py
```
▶ Or run with a file:
```
python main.py ips.txt
```

---

🐧 Linux Setup & Run

▶ Install Python (if not installed)
```
sudo apt update
sudo apt install python3 python3-pip -y
```
▶ Install optional dependency
```
pip3 install pyperclip
```
▶ Run the tool
```
python3 main.py
```
▶ Run with file input
```
python3 main.py ips.txt
```

---

📱 Termux (Android) Setup

▶ Install dependencies
```
pkg update && pkg upgrade -y
pkg install python -y
```
▶ Optional clipboard support
```
pip install pyperclip
```
▶ Run the tool
```
python main.py
```
▶ Run with file
```
python main.py ips.txt
```

---

📥 Input Methods

You can provide IPs in 3 ways:

1. Interactive input

Just run the script and type IPs line by line:

192.168.1.1
8.8.8.8

2. File input
```
python main.py file.txt
```
3. Piped input
```
cat file.txt | python main.py
```

---

📤 Output Example

⏱ 15.94s
📡 13
🟢 11
🔴 2

---

📋 Notes

Requires system ping command (pre-installed on most systems)

Clipboard feature is optional and may not work in all environments


---

⚠️ Permissions (Termux)

If clipboard doesn’t work in Termux:

termux-setup-storage


---

📄 License

This project is released under the MIT License and is free to use, with attribution to the author required. 

