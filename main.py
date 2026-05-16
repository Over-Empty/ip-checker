import os
import re
import subprocess
import sys
import threading
import time
from queue import Queue
from typing import List, Set
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBS_DIR = os.path.join(BASE_DIR, "libs")

if LIBS_DIR not in sys.path:
    sys.path.insert(0, LIBS_DIR)

try:
    import pyperclip
    CLIP_AVAILABLE = True
except Exception:
    pyperclip = None
    CLIP_AVAILABLE = False


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    PURPLE = '\033[35m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'


def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║     ██████╗ ██╗███╗   ██╗ ██████╗ ███████╗██████╗                     ║
║     ██╔══██╗██║████╗  ██║██╔════╝ ██╔════╝██╔══██╗                    ║
║     ██████╔╝██║██╔██╗ ██║██║  ███╗█████╗  ██████╔╝                    ║
║     ██╔═══╝ ██║██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗                    ║
║     ██║     ██║██║ ╚████║╚██████╔╝███████╗██║  ██║                    ║
║     ╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝                    ║
║                                                                      ║
║                    🔍 IP PING CHECKER PRO v2.0 🔍                     ║
║                                                                      ║
║              👨‍🍳 AI Chef Empty 🫙 Presents...                         ║
║                                                                      ║
║              🌱 به امید روز بهتر برای ایران 🌞🦁                     ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
{Colors.RESET}
"""
    print(banner)


def print_footer():
    print(f"""
{Colors.DIM}{'═' * 66}{Colors.RESET}
{Colors.PURPLE}✨ اینترنت آزاد برای همه، یا هیچکس ✨{Colors.RESET}
{Colors.DIM}{'═' * 66}{Colors.RESET}
""")


def loading(stop_event):
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    while not stop_event.is_set():
        for c in chars:
            if stop_event.is_set():
                break
            sys.stdout.write(f"\r{Colors.YELLOW}{c} در حال بررسی...{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(0.05)
    sys.stdout.write("\r" + " " * 50 + "\r")


def extract_ips(text: str) -> Set[str]:
    ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', text)
    valid = set()
    for ip in ips:
        try:
            if all(0 <= int(p) <= 255 for p in ip.split(".")):
                valid.add(ip)
        except:
            pass
    return valid


def ping(ip: str):
    try:
        if sys.platform == "win32":
            cmd = ["ping", "-n", "1", "-w", "1000", ip]
        else:
            cmd = ["ping", "-c", "1", "-W", "1", ip]

        r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return r.returncode == 0
    except:
        return False


def worker(queue, results):
    while not queue.empty():
        try:
            ip = queue.get_nowait()
            results[ip] = ping(ip)
            queue.task_done()
        except:
            break


def check_ips(ips):
    q = Queue()
    results = {}

    for ip in ips:
        q.put(ip)

    threads = []
    for _ in range(min(20, len(ips))):
        t = threading.Thread(target=worker, args=(q, results))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return results


def get_input():
    data = []
    if not sys.stdin.isatty():
        for l in sys.stdin:
            data.append(l.strip())

    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], "r", encoding="utf-8") as f:
                data += [x.strip() for x in f]
        except:
            data += sys.argv[1:]

    if not data:
        while True:
            x = input("➜ ")
            if not x:
                break
            data.append(x)

    return "\n".join(data)


def copy(text):
    if CLIP_AVAILABLE:
        try:
            pyperclip.copy(text)
            return True
        except:
            return False
    return False


def main():
    print_banner()

    start = datetime.now()

    raw = get_input()
    ips = sorted(extract_ips(raw))

    if not ips:
        print(f"{Colors.RED}❌ هیچ IP پیدا نشد{Colors.RESET}")
        print_footer()
        return

    print(f"{Colors.CYAN}🔍 IP ها: {', '.join(ips)}{Colors.RESET}")
    print(f"{Colors.YELLOW}🚀 شروع بررسی {len(ips)} IP{Colors.RESET}")

    stop = threading.Event()
    t = threading.Thread(target=loading, args=(stop,), daemon=True)
    t.start()

    results = check_ips(ips)

    stop.set()
    t.join()

    up = []
    down = []

    for ip, ok in results.items():
        if ok:
            up.append(ip)
        else:
            down.append(ip)

    for ip, ok in results.items():
        if ok:
            print(f"{Colors.GREEN}✅ {ip}{Colors.RESET}")
        else:
            print(f"{Colors.RED}❌ {ip}{Colors.RESET}")

    total = (datetime.now() - start).total_seconds()

    print(f"""
{Colors.BOLD}
┌────────────────────────────────────────────┐
│ ⏱ {total:.2f}s
│ 📡 {len(ips)}
│ 🟢 {len(up)}
│ 🔴 {len(down)}
└────────────────────────────────────────────┘
{Colors.RESET}
""")

    if up:
        input("Enter برای کپی IP های آنلاین...")
        text = "\n".join(up)

        if copy(text):
            print(f"{Colors.GREEN}✅ کپی شد{Colors.RESET}")
        else:
            print(f"{Colors.RED}❌ نتونست کپی کنه (clipboard فعال نیست){Colors.RESET}")

        print(f"\n{text}")

    print_footer()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSTOP")
        print_footer()
