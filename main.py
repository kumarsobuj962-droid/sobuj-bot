import os, re, threading, telebot, time, random
from flask import Flask
import requests, urllib.parse

app = Flask(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")

def is_bangla(t):
    return bool(re.search(r'[\u0980-\u09FF]', t))

def ai_reply(q):
    q_low = q.lower().strip()

    # 1. Boss Identity - Fixed Reply
    if any(x in q_low for x in ["ke baniyeche","কে বানিয়েছে","ke toiri","কে তৈরি","who made you","who created you","creator"]):
        return "আমাকে তৈরি করেছেন আমার Boss ITz Sobuj! 🔥"
    if any(x in q_low for x in ["tomar nam ki","তোমার নাম কি","who are you","tumi ke"]):
        return "আমি ITz Sobuj Bot! Boss Sobuj আমাকে বানিয়েছে তোমাকে Help করার জন্য! 🚀"
    if any(x in q_low for x in ["kemon acho","কেমন আছো","how are you"]):
        return "আলহামদুলিল্লাহ ভালো আছি Boss! তুমি কেমন আছো? 😊" if is_bangla(q) else "I'm great Boss! How are you? 😊"
    if any(x in q_low for x in ["valo","ভালো","love you","boss"]):
        return "Love you too Boss! ❤️ বলো কি Help লাগবে?"

    # 2. Try New Free AI API - BlackBox (Most Stable)
    apis_to_try = [
        {
            "url": "https://api.blackbox.ai/api/chat",
            "json": {"messages": [{"id":"1","content": q, "role":"user"}], "id":"0", "previewToken": None},
        }
    ]

    # Try Blackbox
    try:
        r = requests.post("https://www.blackbox.ai/api/chat", json={
            "messages": [{"role":"user","content": f"You are ITz Sobuj Bot created by ITz Sobuj. Reply short in same language as user. User says: {q}"}],
            "id": "abc"
        }, timeout=15, headers={"Content-Type":"application/json"})
        if r.status_code == 200 and len(r.text) > 5 and "{}" not in r.text[:10]:
            # Blackbox returns messy text, clean it
            txt = r.text.strip()
            # Remove $~~~$ markers if any
            txt = txt.replace("$~~~$", "").strip()
            if len(txt) > 3:
                return txt[:1500]
    except Exception as e:
        print(f"Blackbox Error: {e}")

    # 3. Try Pollinations with POST (Better)
    try:
        r = requests.post("https://text.pollinations.ai/openai",
            json={"model":"openai", "messages":[{"role":"user","content":q}]},
            timeout=15)
        if r.status_code == 200:
            data = r.json()
            text = data.get('choices', [{}])[0].get('message', {}).get('content', '')
            if text and text!= "{}" and len(text) > 3:
                return text[:1500]
    except Exception as e:
        print(f"Pollinations POST Error: {e}")

    # 4. Final Fallback - Smart Reply (No more {})
    fallbacks_bn = [
        "হ্যাঁ Boss বুঝেছি! বলো বিস্তারিত কি জানতে চাও? 🚀",
        "ওয়াও Boss! দারুন প্রশ্ন! আরেকটু বিস্তারিত বলো? 🔥",
        "হাজির Boss! তোমার জন্যই তো আছি! কি Help লাগবে?",
    ]
    fallbacks_en = [
        "Got it Boss! Tell me more details? 🚀",
        "Yes Boss! I'm here to help! What do you need? 🔥",
        "Nice Boss! Ask me anything!",
    ]
    return random.choice(fallbacks_bn if is_bangla(q) else fallbacks_en)

@app.route('/')
def home():
    return "ITz Sobuj Bot is Live!"

if BOT_TOKEN:
    bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

    @bot.message_handler(func=lambda m: True)
    def handle(m):
        if not m.text or len(m.text) > 2000:
            return
        # Anti-spam: ignore old messages
        if time.time() - m.date > 60:
            return
        print(f"USER: {m.text}")
        try:
            reply = ai_reply(m.text)
            bot.reply_to(m, reply)
        except Exception as e:
            print(f"Reply Error: {e}")

    def run_bot():
        try:
            bot.remove_webhook()
            time.sleep(3)
            bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=30)
        except Exception as e:
            print(f"Polling Error: {e}")
            time.sleep(5)
            run_bot()

    def run_flask():
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

    if __name__ == "__main__":
        threading.Thread(target=run_bot, daemon=True).start()
        run_flask()
