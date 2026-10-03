import os, re, threading, telebot
from flask import Flask
import requests, urllib.parse, time

app = Flask(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")

def is_bangla(t):
    return bool(re.search(r'[\u0980-\u09FF]', t))

def ai_reply(q):
    q_low = q.lower()
    if any(x in q_low for x in ["ke baniyeche","কে বানিয়েছে","ke toiri","who made you"]):
        return "আমাকে তৈরি করেছেন আমার Boss ITz Sobuj! 🔥"
    if any(x in q_low for x in ["tomar nam ki","তোমার নাম কি","who are you"]):
        return "আমি ITz Sobuj Bot! Boss Sobuj আমাকে বানিয়েছে তোমাকে help করার জন্য! 🚀"
    try:
        prompt = f"You are ITz Sobuj Bot. Reply in same language as user. User: {q}"
        enc = urllib.parse.quote(prompt)
        r = requests.get(f"https://text.pollinations.ai/{enc}?model=openai", timeout=20)
        text = r.text.strip()
        if text and text != "{}" and len(text) > 3 and '"{}"' not in text:
            return text[:1500]
    except Exception as e:
        print(e)
    return "হ্যাঁ Boss বলো! কি help লাগবে? 🚀" if is_bangla(q) else "Yes Boss, tell me! How can I help? 🚀"

@app.route('/')
def home():
    return "ITz Sobuj Bot is Live!"

if BOT_TOKEN:
    bot = telebot.TeleBot(BOT_TOKEN)
    @bot.message_handler(func=lambda m: True)
    def handle(m):
        if not m.text: return
        try:
            bot.reply_to(m, ai_reply(m.text))
        except Exception as e:
            print(e)
    def run_bot():
        bot.remove_webhook()
        time.sleep(2)
        bot.infinity_polling(skip_pending=True)
    def run_flask():
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    if __name__ == "__main__":
        threading.Thread(target=run_bot, daemon=True).start()
        run_flask()
