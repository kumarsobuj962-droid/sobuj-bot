import telebot, requests, os
from flask import Flask
import threading
from datetime import datetime

BOT_TOKEN ="8783164981:AAFZ-mX7GSxoznnk2IrPpc-gQno1nQBucJA"
WEATHER_API ="9338fbe75f37359424935e8c383e80cc"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Niamatpur Seba Bot 24/7 Live BOSS!"

def get_weather(city="Niamatpur"):
    if city.lower() in ["niamatpur"]:
        city = "Naogaon"
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric"
        data = requests.get(url, timeout=10).json()
        if data.get("cod") == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            return f"📍 {city}\n🌡️ {temp}°C\n☁️ {desc}"
    except:
        pass
    return "❌ City পাওয়া যায়নি BOSS!"

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🔥 BOSS Niamatpur Seba Bot Live!\n\n/weather - আবহাওয়া দেখো\n/photo - ফটো\n\nNo Channel Join Needed!")

@bot.message_handler(commands=['weather'])
def weather_cmd(m):
    parts = m.text.split(maxsplit=1)
    city = parts[1] if len(parts) > 1 else "Niamatpur"
    bot.reply_to(m, get_weather(city))

@bot.message_handler(commands=['photo'])
def photo_cmd(m):
    bot.reply_to(m, "📸 Photo Feature Coming Soon BOSS!")

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
