# 🔍 IP Ping Checker Pro 🌞🦁

یک ابزار سریع و چندنخی (Multi-threaded) برای بررسی IP ها که می‌تواند آدرس‌های IP را از متن، فایل یا ورودی مستقیم استخراج کند، آن‌ها را به صورت همزمان پینگ بگیرد و مشخص کند کدام IP ها آنلاین یا آفلاین هستند.


---

# ✨ ویژگی‌ها

- استخراج خودکار IP از متن، فایل یا ورودی مستقیم
- بررسی سریع IP ها با استفاده از Multi-threading
- نمایش IP های آنلاین و آفلاین
- پشتیبانی از ویندوز، لینوکس و ترموکس
- بدون نیاز به کتابخانه‌های اضافی
- سبک، سریع و قابل حمل

---

# 📦 نیازمندی‌ها

- Python 3.8 یا بالاتر
- Git

## پشتیبانی اختیاری از کلیپ‌بورد

برای فعال شدن قابلیت کپی خودکار:

```bash
pip install pyperclip
```

یا فایل `pyperclip.py` را داخل پوشه `libs` قرار دهید.

---

# 🪟 نصب و اجرا روی ویندوز

## 1. نصب Python

دانلود از:

https://www.python.org/downloads/

هنگام نصب حتما گزینه زیر را فعال کنید:

```text
Add Python to PATH
```

---

## 2. نصب Git

دانلود از:

https://git-scm.com/download/win

تمام مراحل نصب را روی Next بگذارید.

---

## 3. باز کردن CMD

در منوی استارت عبارت زیر را جستجو کنید:

```text
cmd
```

---

## 4. دانلود پروژه

```bash
git clone https://github.com/Over-Empty/ip-checker.git
```

---

## 5. ورود به پوشه پروژه

```bash
cd ip-checker
```

---

## 6. نصب کلیپ‌بورد (اختیاری)

```bash
pip install pyperclip
```

---

## 7. اجرای برنامه

```bash
python main.py
```

---

## اجرا با فایل

```bash
python main.py ips.txt
```

---

# 🐧 نصب و اجرا روی لینوکس

## اوبونتو / دبیان

```bash
sudo apt update
sudo apt install python3 python3-pip git -y
```

---

## آرچ لینوکس

```bash
sudo pacman -S python python-pip git
```

---

## دانلود پروژه

```bash
git clone https://github.com/Over-Empty/ip-checker.git
```

---

## ورود به پوشه پروژه

```bash
cd ip-checker
```

---

## نصب کلیپ‌بورد (اختیاری)

```bash
pip install pyperclip
```

---

## اجرای برنامه

```bash
python3 main.py
```

---

## اجرا با فایل

```bash
python3 main.py ips.txt
```

---

# 📱 نصب و اجرا روی ترموکس (اندروید)

## 1. نصب Python و Git

```bash
pkg update -y
pkg install python git -y
```

---

## 2. دانلود پروژه

```bash
git clone https://github.com/Over-Empty/ip-checker.git
```

---

## 3. ورود به پوشه پروژه

```bash
cd ip-checker
```

---

## 4. نصب کلیپ‌بورد (اختیاری)

```bash
pip install pyperclip
```

---

## 5. اجرای برنامه

```bash
python main.py
```

---

## اجرا با فایل

```bash
python main.py ips.txt
```

---

# 📋 نکات

- این ابزار از دستور داخلی `ping` سیستم استفاده می‌کند
- نیاز به اینترنت یا API خارجی ندارد
- سرعت بررسی به کیفیت اینترنت و سیستم بستگی دارد
- قابلیت کپی IP های آنلاین در صورت فعال بودن کلیپ‌بورد در دسترس است

---

# ⚠️ نکات مربوط به ترموکس

اگر کلیپ‌بورد در ترموکس کار نکرد:

```bash
termux-setup-storage
```

سپس یک‌بار ترموکس را ببندید و دوباره باز کنید.

---

# 📄 لایسنس

این پروژه تحت لایسنس MIT منتشر شده است.

استفاده، ویرایش و انتشار آن آزاد است، اما ذکر نام سازنده الزامی می‌باشد.

---

# 👨‍🍳 سازنده

AI Chef Empty 🫙

🌞🦁
