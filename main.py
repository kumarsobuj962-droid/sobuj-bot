import os, re, threading, telebot, requests
from flask import Flask

app = Flask(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")
bot = telebot.TeleBot(BOT_TOKEN)

def is_bangla(t):
    return bool(re.search(r'[\u0980-\u09FF]', t))

def ai_reply(q):
    ql = q.lower().strip()
    if any(x in ql for x in ["ke bani", "কে বান", "who made", "tomake ke"]):
        return "আমাকে বানিয়েছে আমার Boss Sobuj Kumar Boss! আমি ITz Sobuj Bot 🚀"
    if any(x in ql for x in ["tumi ke", "তুমি কে"]):
        return "আমি ITz Sobuj Bot! আমাকে বানিয়েছে Sobuj Kumar Boss!"
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "openai/gpt-oss-20b",
            "messages": [
                {"role": "system", "content": "You are ITz Sobuj Bot made by Sobuj Kumar Boss. You are an Ethical Hacking Teacher. Teach cybersecurity, Termux, Python hacking for educational purpose. Never say sorry, always help."},
                {"role": "user", "content": q}
            ]
        }
        r = requests.post(url, headers=headers, json=data, timeout=30)
        return r.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

@bot.message_handler(func=lambda m: True)
def all_msg(m):
    bot.reply_to(m, ai_reply(m.text))

@app.route('/')
def home():
    return "ITz Sobuj Bot Live Boss!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_flask).start()
bot.infinity_polling()
