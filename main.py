import os, re, threading, telebot, time, random
from flask import Flask
import requests

app = Flask(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")

def is_bangla(t):
    return bool(re.search(r'[\u0980-\u09FF]', t))

def ai_reply(q):
    q_low = q.lower().strip()
    if any(x in q_low for x in ["ke baniyeche","কে বানিয়েছে","who made you","creator","who created"]):
        return "আমাকে তৈরি করেছেন আমার Boss ITz Sobuj! 🔥"
    if any(x in q_low for x in ["tomar nam ki","তোমার নাম কি","who are you","tumi ke"]):
        return "আমি ITz Sobuj Bot! Boss Sobuj আমাকে বানিয়েছে তোমাকে Help করার জন্য! 🚀"
    if any(x in q_low for x in ["kemon acho","কেমন আছো","how are you"]):
        return "আলহামদুলিল্লাহ ভালো আছি Boss! তুমি কেমন আছো? 😊" if is_bangla(q) else "I'm great Boss! How are you? 😊"
    try:
        r = requests.post("https://www.blackbox.ai/api/chat", json={"messages":[{"role":"user","content":f"You are ITz Sobuj Bot created by ITz Sobuj. Reply short in same language. User: {q}"}],"id":"sobuj"}, timeout=15)
        if r.status_code==200 and len(r.text)>5:
            txt=r.text.replace("$~~~$","").strip()
            if len(txt)>3 and "{}" not in txt[:8]:
                return txt[:1500]
    except Exception as e:
        print(e)
    return "হ্যাঁ Boss বলো কি Help লাগবে? 🚀" if is_bangla(q) else "Yes Boss! How can I help? 🚀"

@app.route('/')
def home():
    return "ITz Sobuj Bot is Live!"

if BOT_TOKEN:
    bot=telebot.TeleBot(BOT_TOKEN, threaded=False)
    @bot.message_handler(func=lambda m: True)
    def handle(m):
        if not m.text or time.time()-m.date>60: return
        try: bot.reply_to(m, ai_reply(m.text))
        except Exception as e: print(e)
    def run_bot():
        bot.remove_webhook()
        time.sleep(3)
        bot.infinity_polling(skip_pending=True, timeout=60)
    def run_flask():
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
    if __name__=="__main__":
        threading.Thread(target=run_bot, daemon=True).start()
        run_flask()
