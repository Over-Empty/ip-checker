import os
import re
import subprocess
import sys
import threading
import time

from queue import Queue
from typing import List, Set
from datetime import datetime

# =========================
# اضافه کردن پوشه libs
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBS_DIR = os.path.join(BASE_DIR, "libs")

if LIBS_DIR not in sys.path:
    sys.path.insert(0, LIBS_DIR)

try:
    import pyperclip
except ImportError:
    print("❌ Missing dependency: libs/pyperclip.py")
    sys.exit(1)


# =========================
# Colors
# =========================

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


# =========================
# UI
# =========================

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
║              🌱 به امید روز بهتر برای ایران 🇮🇷                       ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
{Colors.RESET}
"""
    print(banner)


def print_footer():
    footer = f"""
{Colors.DIM}{'═' * 66}{Colors.RESET}
{Colors.PURPLE}✨ اینترنت آزاد برای همه، یا هیچکس ✨{Colors.RESET}
{Colors.DIM}{'═' * 66}{Colors.RESET}
"""
    print(footer)


def print_loading_animation(stop_event):
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"

    while not stop_event.is_set():
        for char in chars:
            if stop_event.is_set():
                break

            sys.stdout.write(
                f"\r{Colors.YELLOW}{char} در حال بررسی آی‌پی‌ها...{Colors.RESET}"
            )
            sys.stdout.flush()
            time.sleep(0.05)

    sys.stdout.write("\r" + " " * 60 + "\r")


# =========================
# Logic
# =========================

def extract_ips_from_text(text: str) -> Set[str]:
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    found_ips = re.findall(ip_pattern, text)

    valid_ips = set()

    for ip in found_ips:
        try:
            parts = ip.split('.')

            if all(0 <= int(part) <= 255 for part in parts):
                valid_ips.add(ip)

        except ValueError:
            pass

    return valid_ips


def ping_ip(ip: str, timeout: int = 1) -> bool:
    try:
        if sys.platform == "win32":
            command = ["ping", "-n", "1", "-w", str(timeout * 1000), ip]
        else:
            command = ["ping", "-c", "1", "-W", str(timeout), ip]

        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout + 1
        )

        return result.returncode == 0

    except subprocess.TimeoutExpired:
        return False

    except Exception:
        return False


def check_ips_parallel(ips: List[str], max_workers: int = 20) -> dict:
    results = {}
    queue = Queue()
    lock = threading.Lock()

    for ip in ips:
        queue.put(ip)

    def worker():
        while not queue.empty():
            try:
                ip = queue.get_nowait()

                is_up = ping_ip(ip)

                with lock:
                    results[ip] = is_up

                queue.task_done()

            except Exception:
                break

    threads = []

    for _ in range(min(max_workers, len(ips))):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return results


# =========================
# Input
# =========================

def get_input_from_multiple_sources():
    all_text = []

    # Pipe input
    if not sys.stdin.isatty():
        for line in sys.stdin:
            all_text.append(line.strip())

    # File or CLI args
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                all_text.extend([line.strip() for line in f])

        except Exception:
            all_text.extend(sys.argv[1:])

    # Manual input
    if not all_text:
        print(f"{Colors.YELLOW}{Colors.BOLD}📝 لطفاً آی‌پی‌ها را وارد کنید:{Colors.RESET}")
        print(f"{Colors.DIM}(می‌توانید با فاصله، کاما یا خط جدید جدا کنید){Colors.RESET}")
        print(f"{Colors.CYAN}برای پایان، Enter خالی بزنید:{Colors.RESET}")

        user_input = []

        while True:
            line = input(f"{Colors.GREEN}➜ {Colors.RESET}")

            if not line:
                break

            user_input.append(line)

        all_text = user_input

    return '\n'.join(all_text)


# =========================
# Clipboard
# =========================

def copy_to_clipboard(text):
    try:
        pyperclip.copy(text)
        return True

    except Exception:
        return False


# =========================
# Result UI
# =========================

def print_result_box(up_ips, down_ips, total_time):
    print(f"\n{Colors.BOLD}{Colors.HEADER}┌{'─' * 60}┐{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.HEADER}│{'📊 گزارش نهایی بررسی آی‌پی':^60}│{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.HEADER}├{'─' * 60}┤{Colors.RESET}")

    total = len(up_ips) + len(down_ips)

    up_percent = (len(up_ips) / total * 100) if total else 0
    down_percent = (len(down_ips) / total * 100) if total else 0

    print(
        f"{Colors.BOLD}│ "
        f"{Colors.CYAN}⏱️ زمان اجرا:{Colors.RESET} "
        f"{total_time:.2f} ثانیه"
        f"{' ' * 39}│"
    )

    print(
        f"{Colors.BOLD}│ "
        f"{Colors.CYAN}📡 کل آی‌پی‌ها:{Colors.RESET} "
        f"{total:<45}│"
    )

    print(
        f"{Colors.BOLD}│ "
        f"{Colors.GREEN}✅ آنلاین:{Colors.RESET} "
        f"{len(up_ips)} ({up_percent:.1f}%)"
        f"{' ' * 38}│"
    )

    print(
        f"{Colors.BOLD}│ "
        f"{Colors.RED}❌ آفلاین:{Colors.RESET} "
        f"{len(down_ips)} ({down_percent:.1f}%)"
        f"{' ' * 37}│"
    )

    print(f"{Colors.BOLD}{Colors.HEADER}├{'─' * 60}┤{Colors.RESET}")

    if up_ips:
        print(f"{Colors.BOLD}{Colors.GREEN}│ 🟢 آی‌پی‌های آنلاین:{' ' * 38}│{Colors.RESET}")

        for ip in up_ips:
            print(f"{Colors.GREEN}│    ✅ {ip:<54}│{Colors.RESET}")

    if down_ips:
        print(f"{Colors.BOLD}{Colors.RED}│ 🔴 آی‌پی‌های آفلاین:{' ' * 37}│{Colors.RESET}")

        for ip in down_ips:
            print(f"{Colors.RED}│    ❌ {ip:<54}│{Colors.RESET}")

    print(f"{Colors.BOLD}{Colors.HEADER}└{'─' * 60}┘{Colors.RESET}")


def print_progress_bar(current, total, width=40):
    percent = current / total

    filled = int(width * percent)

    bar = (
        f"{Colors.GREEN}{'█' * filled}{Colors.RESET}"
        f"{Colors.DIM}{'░' * (width - filled)}{Colors.RESET}"
    )

    sys.stdout.write(
        f"\r{Colors.CYAN}⏳ "
        f"{bar} "
        f"{percent * 100:.1f}% "
        f"({current}/{total})"
        f"{Colors.RESET}"
    )

    sys.stdout.flush()


# =========================
# Main
# =========================

def main():
    print_banner()

    start_time = datetime.now()

    raw_input = get_input_from_multiple_sources()

    unique_ips = sorted(extract_ips_from_text(raw_input))

    if not unique_ips:
        print(
            f"\n{Colors.RED}{Colors.BOLD}"
            f"❌ هیچ آی‌پی معتبری پیدا نشد!"
            f"{Colors.RESET}"
        )

        print_footer()
        return

    print(f"\n{Colors.CYAN}{Colors.BOLD}🔍 آی‌پی‌های شناسایی شده:{Colors.RESET}")

    print(f"{Colors.DIM}   {', '.join(unique_ips)}{Colors.RESET}")

    print(
        f"\n{Colors.YELLOW}{Colors.BOLD}"
        f"🚀 شروع بررسی {len(unique_ips)} آی‌پی..."
        f"{Colors.RESET}\n"
    )

    stop_event = threading.Event()

    loading_thread = threading.Thread(
        target=print_loading_animation,
        args=(stop_event,),
        daemon=True
    )

    loading_thread.start()

    results = check_ips_parallel(unique_ips)

    stop_event.set()

    loading_thread.join()

    up_ips = []
    down_ips = []

    print(f"\n{Colors.BOLD}{Colors.CYAN}📡 نتایج بررسی:{Colors.RESET}\n")

    for idx, (ip, is_up) in enumerate(results.items(), 1):

        if is_up:
            up_ips.append(ip)

            print(
                f"{Colors.GREEN}"
                f"✅ {ip:<16} ✨ آنلاین ✨"
                f"{Colors.RESET}"
            )

        else:
            down_ips.append(ip)

            print(
                f"{Colors.RED}"
                f"❌ {ip:<16} 💀 آفلاین 💀"
                f"{Colors.RESET}"
            )

        print_progress_bar(idx, len(unique_ips))

    print()

    total_time = (datetime.now() - start_time).total_seconds()

    print_result_box(up_ips, down_ips, total_time)

    # Copy online IPs
    if up_ips:

        print(
            f"\n{Colors.CYAN}{Colors.BOLD}"
            f"💾 برای کپی آی‌پی‌های آنلاین Enter بزنید..."
            f"{Colors.RESET}"
        )

        input()

        ips_text = '\n'.join(up_ips)

        if copy_to_clipboard(ips_text):

            print(
                f"{Colors.GREEN}{Colors.BOLD}"
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