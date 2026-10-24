import telebot, requests, os
from flask import Flask
import threading
from datetime import datetime
import pytz

BOT_TOKEN ="8783164981:AAGhXqg3iXEG5NoA3sEinyEGw0ChugH3sd8"
WEATHER_API ="9338fbe75f37359424935e8c383e80cc"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Niamatpur Seba Bot 24/7 Live BOSS!"

def get_weather(city="Niamatpur"):
    display_city = city
    if city.lower() in ["niamatpur", "niamatpur"]:
        city = "Naogaon"
        display_city = "Niamatpur (Naogaon)"
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric"
        data = requests.get(url, timeout=10).json()
        if data.get("cod") == 200:
            temp = data['main']['temp']
            feels = data['main']['feels_like']
            hum = data['main']['humidity']
            desc = data['weather'][0]['description']
            return f"📍 {display_city}\n🌡️ তাপমাত্রা: {temp}°C (অনুভব {feels}°C)\n💧 আর্দ্রতা: {hum}%\n☁️ {desc}\n\nBOSS Niamatpur Seba"
    except:
        pass
    return f"❌ {city} শহর পাওয়া যায়নি BOSS! লেখো: /weather Dhaka"

@bot.message_handler(commands=['start', 'help'])
def start(m):
    text = """🔥 BOSS Nimatpur Seba Bot Online 24/7!

👇 সব সেবা:
 /weather Dhaka - আবহাওয়া দেখো (যেকোনো শহর)
/time - সময় দেখো
/photo - নিয়ামতপুরের ফটো
/contact - যোগাযোগ
/help - সাহায্য

No Channel Join Needed! BOSS"""
    bot.reply_to(m, text)

@bot.message_handler(commands=['weather'])
def weather_cmd(m):
    parts = m.text.split(maxsplit=1)
    city = parts[1] if len(parts) > 1 else "Niamatpur"
    bot.send_chat_action(m.chat.id, 'typing')
    bot.reply_to(m, get_weather(city))

@bot.message_handler(commands=['time'])
def time_cmd(m):
    tz = pytz.timezone('Asia/Dhaka')
    now = datetime.now(tz)
    time_str = now.strftime("%d %B %Y, %I:%M:%S %p")
    bot.reply_to(m, f"⏰ বাংলাদেশ সময়:\n{time_str}\n\n📍 Asia/Dhaka\nBOSS")

@bot.message_handler(commands=['photo'])
def photo_cmd(m):
    try:
        # Random beautiful photo
        bot.send_photo(m.chat.id, "https://picsum.photos/800/600", caption="📸 Niamatpur Seba - Random View BOSS!\nপরে এখানে Niamatpur এর Real Photo দেবো!")
    except:
        bot.reply_to(m, "📸 Photo Feature - Coming Soon BOSS!")

@bot.message_handler(commands=['contact'])
def contact_cmd(m):
    bot.reply_to(m, "📞 যোগাযোগ:\n\n👤 Sobuj Kumar\n📍 Niamatpur, Naogaon\n💬 Telegram: @SobujKumar\n\nBOSS যেকোনো সমস্যায় Message দাও!")

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
