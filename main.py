import os
import requests
import urllib.parse
import threading
import telebot
from flask import Flask

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

def ai_reply(q):
    try:
        q_low = q.lower()
        if "ke baniyeche" in q_low or "who made" in q_low or "kisne" in q_low or "tomake ke" in q_low:
            return "Amake Sobuj baniyeche Boss! Ami ITz Sobuj Bot!"
        system = "You are ITz Sobuj Bot made by Sobuj. Reply Bengali short. Always say Amake Sobuj baniyeche if asked who made you."
        enc = urllib.parse.quote(f"{system} User:{q}"[:500])
        r = requests.get(f"https://text.pollinations.ai/{enc}", timeout=20)
        return r.text.strip()[:1000]
    except:
        return "Amake Sobuj baniyeche Boss!"

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        bot.reply_to(m, ai_reply(m.text))
    except:
        pass

@app.route('/')
def home():
    return "Sobuj Bot is Running! Boss"

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
