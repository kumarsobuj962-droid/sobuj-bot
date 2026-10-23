import telebot
import requests
import os

BOT_TOKEN = "8783164981:AAF96LkEQ-K-uD7RM_h4aOg0XruYPfX5jcs"
WEATHER_API = "9338fbe75f37359424935e8c383e80cc"

bot = telebot.TeleBot(BOT_TOKEN)

def get_weather(city="Niamatpur"):
    # 1. OpenWeather Try করবে
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric&lang=bn"
        data = requests.get(url, timeout=10).json()
        if data.get("cod") == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            humid = data['main']['humidity']
            msg = f"📍 **{city}**\n🌡️ {temp}°C | {desc}\n💧 Humidity: {humid}%\n\n"
            if temp >= 36: msg += "🔴 ALERT: প্রচন্ড গরম!"
            elif "rain" in desc or "বৃষ্টি" in desc: msg += "🟡 ALERT: বৃষ্টি আসছে!"
            else: msg += "🟢 আবহাওয়া ঠিক আছে BOSS!"
            return msg
    except:
        pass

    # 2. যদি OpenWeather Fail করে, Backup API চলবে (এটা এখনই কাজ করবে)
    try:
        url = f"https://wttr.in/{city}?format=j1"
        data = requests.get(url, timeout=10).json()
        curr = data['current_condition'][0]
        temp = curr['temp_C']
        desc = curr['weatherDesc'][0]['value']
        humid = curr['humidity']
        return f"📍 **{city}**\n🌡️ {temp}°C | {desc}\n💧 {humid}%\n\n🟢 Live Data BOSS!"
    except Exception as e:
        return f"❌ Error BOSS: {e}"

@bot.message_handler(commands=['start', 'weather'])
def start(m):
    bot.reply_to(m, get_weather("Niamatpur"), parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def any_text(m):
    bot.reply_to(m, get_weather(m.text.strip()), parse_mode="Markdown")

print("BOSS Bot 24/7 Online...")
bot.infinity_polling()
