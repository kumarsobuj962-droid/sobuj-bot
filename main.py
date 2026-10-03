import os, re, threading
import telebot
from flask import Flask
import requests, urllib.parse

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
print(f"BOT_TOKEN Loaded: {bool(BOT_TOKEN)}")

def is_bangla(text):
    return bool(re.search(r'[\u0980-\u09FF]', text))

def ai_reply(question):
    q = question.lower()
    # Boss Credit
    if any(x in q for x in ["ke baniyeche", "কে বানিয়েছে", "ke toiri", "কে তৈরি", "who made you", "who created you"]):
        return "আমাকে তৈরি করেছেন আমার Boss ITz Sobuj! 🔥" if is_bangla(question) else "I was created by my Boss ITz Sobuj! 🔥"
    
    try:
        system_prompt = "You are ITz Sobuj Bot, created by ITz Sobuj. Reply short and friendly. Reply in same language as user (Bangla if user uses Bangla)."
        full_prompt = f"{system_prompt} Question: {question}"
        encoded = urllib.parse.quote(full_prompt)
        url = f"https://text.pollinations.ai/{encoded}"
        res = requests.get(url, timeout=20)
        if res.status_code == 200 and res.text:
            return res.text.strip()[:1500]
    except Exception as e:
        print(f"AI Error: {e}")
    
    return "হ্যাঁ Boss বলো, শুনছি! 🚀"

@app.route('/')
def home():
    return "ITz Sobuj Bot is Live! Boss ITz Sobuj 🔥"

# Bot Setup
if BOT_TOKEN:
    bot = telebot.TeleBot(BOT_TOKEN)
    
    @bot.message_handler(func=lambda m: True)
    def handle_all(m):
        try:
            reply = ai_reply(m.text)
            bot.reply_to(m, reply)
        except Exception as e:
            print(f"Bot Error: {e}")

    def run_bot():
        print("Bot Polling Started...")
        bot.infinity_polling()

    def run_flask():
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

    if __name__ == "__main__":
        threading.Thread(target=run_bot).start()
        run_flask()
else:
    print("ERROR: BOT_TOKEN is None! Please set in Render Environment")
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
