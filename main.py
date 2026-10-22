import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")

CONTACT_TEXT = """🇧🇩 নিয়ামতপুর সেবা - অফিসিয়াল যোগাযোগ

📧 UNO নিয়ামতপুর (Verified সরকারি):
unoniamatpur@mopa.gov.bd

🏥 উপজেলা স্বাস্থ্য কমপ্লেক্স (Verified):
neyamatpur@uhfpo.dghs.gov.bd

🚨 জরুরি: জাতীয় জরুরি সেবা 999
"""

SERVICE_TEXT = """🇧🇩 নিয়ামতপুর উপজেলা - ৮টি ইউনিয়ন

1. বাহাদুরপুর - 34,670 জন
2. ভাবিচা - 32,107 জন  
3. চন্দননগর - 25,894 জন
4. হাজীনগর - 28,455 জন
5. নিয়ামতপুর সদর - 28,313 জন
6. পারইল - 31,152 জন
7. রসুলপুর - 38,232 জন
8. শ্রীমন্তপুর - 29,528 জন

সেবা: জন্ম নিবন্ধন, নাগরিক সনদ, ভূমি সেবা
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("আসসালামু আলাইকুম! 🙏\nআমি নিয়ামতপুর সেবা বট।\n\n/services - সেবা\n/contact - যোগাযোগ\n/help - সাহায্য")

async def services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(SERVICE_TEXT)

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(CONTACT_TEXT)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("যেকোনো সমস্যায় /contact - জরুরি 999")

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "Niamatpur Bot is Live!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host='0.0.0.0', port=port)

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("services", services))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CommandHandler("help", help_cmd))
    print("Bot Starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
