import telebot, requests, os
from flask import Flask
from datetime import datetime, timedelta

BOT_TOKEN = "8783164981:AAF96LkEQ-K-uD7RM_h4aOg0XruYPfX5jcs"
WEATHER_API = "9338fbe75f37359424935e8c383e80cc"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "BOSS Bot 24/7 Live!"

def get_weather(city="Niamatpur"):
    if city.lower() in ["niamatpur", "niamatpur"]:
        city = "Naogaon"
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric&lang=bn"
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
    bot.reply_to(m, "🔥 **BOSS Nimatpur Seba Bot Online 24/7!**\n\n👇 সব সেবা:\n/weather Dhaka\n/time\n/photo\n/contact\n/help", parse_mode="Markdown")

@bot.message_handler(commands=['weather'])
def weather_cmd(m):
    parts = m.text.split()
    city = parts[1] if len(parts) > 1 else "Naogaon"
    bot.reply_to(m, get_weather(city))

@bot.message_handler(commands=['time'])
def time_cmd(m):
    bd_time = datetime.utcnow() + timedelta(hours=6)
    now = bd_time.strftime("%d/%m/%Y %I:%M %p")
    bot.reply_to(m, f"⏰ **BOSS এখন সময়:**\n{now}")

@bot.message_handler(commands=['contact'])
def contact_cmd(m):
    bot.reply_to(m, "📞 **যোগাযোগ / Contact**\n\n👤 Sobuj Kumar\n📍 Niamatpur, Naogaon\n🤖 Bot: ITz Sobuj")

@bot.message_handler(commands=['help', 'services'])
def help_cmd(m):
    bot.reply_to(m, "🆘 **সেবাসমূহ / Services**\n\n/weather [city] - আবহাওয়া\n/time - সময়\n/photo - ছবি\n/contact - যোগাযোগ")

@bot.message_handler(commands=['photo'])
def photo_cmd(m):
    try:
        photo_url = "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=800"
        bot.send_photo(m.chat.id, photo_url, caption="📸 **BOSS Niamatpur Seba**\n📍 Niamatpur, Naogaon - The Beauty of Bangladesh ❤️\n🤖 ITz Sobuj Bot 24/7 Live!")
    except Exception as e:
        bot.reply_to(m, f"📸 Photo Error BOSS: {e}")

@bot.message_handler(func=lambda m: True)
def any_text(m):
    if m.text.startswith('/'):
        return
    if len(m.text) < 20:
        bot.reply_to(m, get_weather(m.text.strip()))
    else:
        bot.reply_to(m, "BOSS /help লিখো!")

def run_bot():
    print("BOSS Bot Online...")
    bot.infinity_polling()

if __name__ == "__main__":
    import threading
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
