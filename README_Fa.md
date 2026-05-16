🔍 IP Ping Checker Pro

یک ابزار سریع و چندنخی برای بررسی IP ها که آدرس‌های IP را از متن، فایل یا ورودی مستقیم استخراج می‌کند، به صورت همزمان (multi-thread) آن‌ها را پینگ می‌کند و مشخص می‌کند کدام IP ها آنلاین یا آفلاین هستند. همچنین امکان کپی IP های فعال را دارد.


---

✨ ویژگی‌ها

استخراج خودکار IP از متن، فایل یا ورودی مستقیم

بررسی سریع با چندنخی (Multi-threading)

پشتیبانی از ویندوز، لینوکس و ترموکس

سبک و بدون وابستگی خاص (به جز clipboard اختیاری)



---

📦 نیازمندی‌ها

Python 3.8 یا بالاتر

(اختیاری برای کپی در کلیپ‌بورد)

```
pip install pyperclip
```

---

🚀 نصب

📌 کلون کردن پروژه
```
git clone https://github.com/your-username/ip-ping-checker.git
cd ip-ping-checker
```

---

🪟 اجرا در ویندوز

▶ اجرای مستقیم:
```
python main.py
```
▶ اجرای با فایل:
```
python main.py ips.txt
```

---

🐧 اجرا در لینوکس

▶ نصب پایتون:
```
sudo apt update
sudo apt install python3 python3-pip -y
```
▶ نصب وابستگی:
```
pip3 install pyperclip
```
▶ اجرا:
```
python3 main.py
```
▶ اجرا با فایل:
```
python3 main.py ips.txt
```

---

📱 اجرا در ترموکس (اندروید)

▶ نصب:
```
pkg update && pkg upgrade -y
pkg install python -y
```
▶ نصب اختیاری:
```
pip install pyperclip
```
▶ اجرا:
```
python main.py
```
▶ اجرا با فایل:
```
python main.py ips.txt
```

---

📥 روش‌های ورودی

1. ورودی دستی

IP ها را خط به خط وارد کنید:

192.168.1.1
8.8.8.8


---

2. ورودی از فایل
```
python main.py file.txt
```

---

3. ورودی پایپ
```
cat file.txt | python main.py
```

---

📤 نمونه خروجی

⏱ 15.94s
📡 13
🟢 11
🔴 2


---

📋 نکات

این ابزار از دستور داخلی سیستم ping استفاده می‌کند

نیاز به اینترنت یا API ندارد

قابلیت کپی کردن IP های آنلاین (در صورت فعال بودن pyperclip)



---

⚠️ ترموکس

اگر کلیپ‌بورد کار نکرد:
```
termux-setup-storage
```

---

📄 لایسنس

این پروژه تحت لایسنس MIT منتشر شده و استفاده از آن آزاد است، فقط ذکر نام سازنده الزامی است.
