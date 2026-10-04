import os, re, threading, telebot, time, requests, urllib.parse
from flask import Flask

app = Flask(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")

def is_bangla(t):
    return bool(re.search(r'[\u0980-\u09FF]', t))

def ai_reply(q):
    ql = q.lower().strip()
    
    # 1. Boss Custom Reply - আলাদা আলাদা
    if any(x in ql for x in ["ke baniyeche","কে বানিয়েছে","who made you","creator"]):
        return "আমাকে বানিয়েছে আমার Boss ITz Sobuj! 🔥"
    if any(x in ql for x in ["তুমি কে","tumi ke","tomar nam ki","who are you","what is your name"]):
        return "আমি ITz Sobuj Bot! আমাকে Boss Sobuj বানিয়েছে! 🚀"
    if "প্রশ্ন করতে পারি" in q or "proshno korte pari" in ql or "ask you" in ql:
        return "হ্যাঁ Boss! 100% পারো! যেকোনো প্রশ্ন করো! 😊"
    if ql in ["hobe","হবে","ok","oke","accha","আচ্ছা"]:
        return "হ্যাঁ Boss হবে! বলো কি করতে হবে? 😉"
    if ql in ["start","hi","hello","hey","হ্যালো","হাই"]:
        return "Hello Boss! আমি ITz Sobuj Bot! বলো কি Help লাগবে? 🚀"
    if "how" in ql:
        return "I'm doing great Boss! How can I help you today? 😊"

    # 2. Real AI - Pollinations
    try:
        prompt = f"You are ITz Sobuj Bot by ITz Sobuj. Friendly. Reply in {'Bengali' if is_bangla(q) else 'English'} in 2 lines. Q: {q}"
        url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
        r = requests.get(url, timeout=15)
        if r.status_code == 200 and len(r.text) > 3 and "Ami ITz Sobuj Bot, amake" not in r.text:
            return r.text.strip()[:1000]
    except Exception as e:
        print(f"AI Err: {e}")

    return "বলো Boss, তোমার প্রশ্নটা আবার বলো? আমি উত্তর দিচ্ছি! 🚀"

@app.route('/')
def home():
    return "ITz Sobuj Bot Live"

bot = None
if BOT_TOKEN:
    bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
    @bot.message_handler(func=lambda m: True)
    def handle(m):
        if not m.text: return
        if time.time() - m.date > 120: return
        bot.reply_to(m, ai_reply(m.text))

def run_bot():
    if not bot: return
    while True:
        try:
            bot.remove_webhook()
            time.sleep(1)
            bot.infinity_polling(skip_pending=True, timeout=30)
        except Exception as e:
            print(e)
            time.sleep(5)

if __name__ == "__main__":
    if BOT_TOKEN:
        threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
