import os
import re
import threading
import telebot
from flask import Flask
import requests
import urllib.parse

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

def is_bangla(text):
    return bool(re.search(r'[\u0980-\u09FF]', text))

def ai_reply(q):
    q_low = q.lower()
    bangla = is_bangla(q)

    # 1. তোমাকে কে তৈরি করেছে - এটা সবচেয়ে গুরুত্বপূর্ণ
    if "ke baniyeche" in q_low or "কে বানিয়েছে" in q_low or "ke toiri" in q_low or "কে তৈরি" in q_low or "who made you" in q_low or "who created you" in q_low or "creator" in q_low or "owner" in q_low or "tomake ke" in q_low:
        if bangla:
            return "আমাকে তৈরি করেছেন আমার Boss ITz Sobuj! 🔥 উনিই আমার মালিক!"
        else:
            return "I was created by my Boss ITz Sobuj! 🔥 He is my owner!"

    # 2. অন্য সব প্রশ্নের উত্তর AI দিবে
    try:
        if bangla:
            system = "Tumi ITz Sobuj Bot. Tomake toiri koreche ITz Sobuj. Tumi Banglay uttor dibe. Tumi khub helpful."
        else:
            system = "You are ITz Sobuj Bot. You were created by ITz Sobuj. You are very helpful. Answer in English."
        
        full_prompt = f"{system} User question: {q}"
        enc = urllib.parse.quote(full_prompt)
        r = requests.get(f"https://text.pollinations.ai/{enc}", timeout=15)
        ans = r.text.strip()
        if ans:
            return ans[:1500]
        else:
            raise Exception("empty")
    except:
        if bangla:
            return f"বলো Boss, '{q}' নিয়ে সুন্দর করে বলছি, একটু সমস্যা হচ্ছে, আবার বলো? 🚀"
        else:
            return f"Tell me Boss, I'm having a little trouble answering '{q}', please ask again? 🚀"

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        bot.reply_to(m, ai_reply(m.text))
    except:
        pass

@app.route('/')
def home():
    return "ITz Sobuj Bot is Live!"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.infinity_polling()
