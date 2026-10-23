import telebot, requests, os
from flask import Flask

BOT_TOKEN = "8783164981:AAF96LkEQ-K-uD7RM_h4aOg0XruYPfX5jcs"
WEATHER_API = "9338fbe75f37359424935e8c383e80cc"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "BOSS Bot 24/7 Live!"

def get_weather(city="Niamatpur"):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric"
        data = requests.get(url, timeout=10).json()
        if data.get("cod") == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            return f"📍 {city}\n🌡️ {temp}°C\n☁️ {desc}"
    except Exception as e:
        print(e)
        pass
    return "❌ Error BOSS, City পাওয়া যায়নি! API Key চেক করো!"

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🔥 BOSS Nimatpur Seba Bot Online!\n\n/weather লিখে City দাও\nEx: /weather Rajshahi\n\nঅথবা শুধু City Name লিখো: Niamatpur", parse_mode="Markdown")

@bot.message_handler(commands=['weather'])
def weather_cmd(m):
    parts = m.text.split()
    city = parts[1] if len(parts) > 1 else "Niamatpur"
    bot.reply_to(m, get_weather(city))

@bot.message_handler(func=lambda m: True)
def any_text(m):
    if m.text.startswith('/'):
        return
    bot.reply_to(m, get_weather(m.text.strip()))

def run_bot():
    print("BOSS Bot 24/7 Online...")
    bot.infinity_polling()

if __name__ == "__main__":
    import threading
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
