# keep_alive.py
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive 🌸"  # این متن وقتی کسی URL رو باز کنه نشون داده میشه

def run():
    # Koyeb به پورت 8080 گوش میده
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
