import os
import re
import subprocess
import sys
import threading
import time
from queue import Queue
from typing import Set
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBS_DIR = os.path.join(BASE_DIR, "libs")

if os.path.isdir(LIBS_DIR) and LIBS_DIR not in sys.path:
    sys.path.insert(0, LIBS_DIR)

CLIP_AVAILABLE = False

try:
    import pyperclip
    CLIP_AVAILABLE = True
except ImportError:
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "pyperclip"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

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
║                    🔍 IP PING CHECKER PRO 🔍                          ║
║                                                                      ║
║                 👨‍🍳 AI Chef Empty 🫙                                  ║
║                                                                      ║
║              🌱 به امید روز بهتر برای ایران 🌞                       ║
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

            sys.stdout.write(
                f"\r{Colors.YELLOW}{c} در حال بررسی IP ها...{Colors.RESET}"
            )
            sys.stdout.flush()
            time.sleep(0.05)

    sys.stdout.write("\r" + " " * 60 + "\r")


def extract_ips(text: str) -> Set[str]:
    ips = re.findall(
        r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
        text
    )

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

        result = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return result.returncode == 0

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
        t = threading.Thread(
            target=worker,
            args=(q, results)
        )

        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return results


def get_input():
    data = []

    if not sys.stdin.isatty():
        for line in sys.stdin:
            data.append(line.strip())

    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], "r", encoding="utf-8") as f:
                data += [x.strip() for x in f]
        except:
            data += sys.argv[1:]

    if not data:
        print(f"{Colors.CYAN}IP ها را وارد کنید:{Colors.RESET}")

        while True:
            x = input("➜ ")

            if not x:
                break

            data.append(x)

    return "\n".join(data)


def copy(text):
    if not CLIP_AVAILABLE:
        return False

    try:
        pyperclip.copy(text)
        return True
    except:
        return False


def main():
    print_banner()

    start = datetime.now()

    raw = get_input()

    ips = sorted(extract_ips(raw))

    if not ips:
        print(f"{Colors.RED}❌ هیچ IP معتبری پیدا نشد{Colors.RESET}")
        print_footer()
        return

    print(
        f"{Colors.CYAN}🔍 تعداد IP پیدا شده: "
        f"{len(ips)}{Colors.RESET}"
    )

    stop = threading.Event()

    loader = threading.Thread(
        target=loading,
        args=(stop,),
        daemon=True
    )

    loader.start()

    results = check_ips(ips)

    stop.set()
    loader.join()

    up = []
    down = []

    print()

    for ip, ok in results.items():
        if ok:
            up.append(ip)
            print(f"{Colors.GREEN}✅ {ip}{Colors.RESET}")
        else:
            down.append(ip)
            print(f"{Colors.RED}❌ {ip}{Colors.RESET}")

    total = (datetime.now() - start).total_seconds()

    print(f"""
{Colors.BOLD}
┌────────────────────────────────────┐
│ ⏱ Time: {total:.2f}s
│ 📡 Total: {len(ips)}
│ 🟢 Online: {len(up)}
│ 🔴 Offline: {len(down)}
└────────────────────────────────────┘
{Colors.RESET}
""")

    if up:
        print(
            f"{Colors.YELLOW}"
            f"برای کپی IP های آنلاین Enter بزنید"
            f"{Colors.RESET}"
        )

        input()

        text = "\n".join(up)

        if copy(text):
            print(f"{Colors.GREEN}✅ کپی شد{Colors.RESET}")
        else:
            print(
                f"{Colors.RED}"
                f"❌ clipboard در دسترس نیست"
                f"{Colors.RESET}"
            )

        print(f"\n{Colors.CYAN}{text}{Colors.RESET}")

    print_footer()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}STOPPED{Colors.RESET}")
        print_footer()          f"{Colors.GREEN}{Colors.BOLD}"
                f"✅ آی‌پی‌ها در کلیپ‌بورد کپی شدند!"
                f"{Colors.RESET}"
            )

        else:
            print(
                f"{Colors.YELLOW}"
                f"⚠️ کپی خودکار انجام نشد."
                f"{Colors.RESET}"
            )

        print(f"\n{Colors.DIM}📋 محتوای کپی شده:{Colors.RESET}")

        print(f"{Colors.GREEN}{ips_text}{Colors.RESET}")

    print_footer()


# =========================
# Start
# =========================

if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:

        print(
            f"\n\n{Colors.YELLOW}{Colors.BOLD}"
            f"⚠️ عملیات توسط کاربر متوقف شد."
            f"{Colors.RESET}"
        )

        print_footer()

        sys.exit(0)

    except Exception as e:

        print(
            f"\n\n{Colors.RED}{Colors.BOLD}"
            f"❌ خطا: {e}"
            f"{Colors.RESET}"
        )

        print_footer()

        sys.exit(1)
