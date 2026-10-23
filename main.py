import telebot
import requests
from flask import Flask
import threading
import os

BOT_TOKEN = "8783164981:AAF96LkEQ-K-uD7RM_h4aOg0XruYPfX5jcs"
WEATHER_API = "9338fbe75f37359424935e8c383e80cc"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "BOSS Bot 24/7 Live!"

def get_weather(city="Niamatpur"):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric&lang=bn"
        data = requests.get(url, timeout=10).json()
        if data.get("cod") == 200:
            return f"📍 {city}\n🌡️ {data['main']['temp']}°C | {data['weather'][0]['description']}\n💧 {data['main']['humidity']}%"
    except:
        pass
    return "❌ Error BOSS, City পাওয়া যায়নি!"

@bot.message_handler(commands=['start', 'weather'])
def start(m):
    bot.reply_to(m, get_weather("Niamatpur"), parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def any_text(m):
    bot.reply_to(m, get_weather(m.text.strip()), parse_mode="Markdown")

def run_bot():
    print("BOSS Bot 24/7 Online...")
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
