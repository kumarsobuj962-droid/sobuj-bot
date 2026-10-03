import os, re, threading, telebot, time, requests
from flask import Flask

app = Flask(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")
print(f"TOKEN OK: {bool(BOT_TOKEN)}")

def is_bangla(t):
    return bool(re.search(r'[\u0980-\u09FF]', t))

def ai_reply(q):
    ql = q.lower().strip()
    if any(x in ql for x in ["ke baniyeche","কে বানিয়েছে","who made you","creator"]):
        return "আমাকে তৈরি করেছেন আমার Boss ITz Sobuj! 🔥"
    if any(x in ql for x in ["tomar nam ki","তোমার নাম কি","who are you","tumi ke"]):
        return "আমি ITz Sobuj Bot! Boss Sobuj আমাকে বানিয়েছে! 🚀"
    if any(x in ql for x in ["kemon acho","কেমন আছো","how are you"]):
        return "ভালো আছি Boss! 😊" if is_bangla(q) else "I'm great Boss! 😊"
    try:
        url = "https://www.blackbox.ai/api/chat"
        data = {"messages":[{"role":"user","content":f"You are ITz Sobuj Bot. Reply same language. User:{q}"}],"id":"sobuj"}
        r = requests.post(url, json=data, timeout=20)
        if r.status_code == 200:
            txt = r.text.replace("$~~~$","").strip()
            if len(txt) > 5 and "{}" not in txt[:10]:
                return txt[:1500]
    except Exception as e:
        print(f"AI Error: {e}")
    return "হ্যাঁ Boss বলো! 🚀" if is_bangla(q) else "Yes Boss! How can I help? 🚀"

@app.route('/')
def home():
    return "ITz Sobuj Bot is Live!"

bot = None
if BOT_TOKEN:
    try:
        bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
        @bot.message_handler(func=lambda m: True)
        def handle(m):
            if not m.text: return
            if time.time() - m.date > 60: return
            try:
                bot.reply_to(m, ai_reply(m.text))
            except Exception as e:
                print(e)
    except Exception as e:
        print(f"Bot Init Error: {e}")

def run_bot():
    if not bot:
        print("No bot token, skipping")
        return
    while True:
        try:
            print("Starting polling...")
            bot.remove_webhook()
            time.sleep(2)
            bot.infinity_polling(skip_pending=True, timeout=30)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    if BOT_TOKEN:
        threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    print(f"Flask starting on {port}")
    app.run(host="0.0.0.0", port=port)
