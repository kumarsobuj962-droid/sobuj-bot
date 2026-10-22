import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN", "তোমার Token এখানেও বসিয়ে রাখো")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🙏 নমস্কার! আমি *নিয়ামতপুর সেবা বট*\n\n"
        "⚠️ এটি বেসরকারি সহায়ক বট, সরকারি বট নয়।\n\n"
        "👇 নিচে ক্লিক করো:\n"
        "/nid - NID সেবা\n"
        "/birth - জন্ম নিবন্ধন\n"
        "/nagad - নগদ সেবা\n"
        "/upazila - উপজেলা তথ্য\n"
        "/bazar - শালবাড়ী বাজার",
        parse_mode='Markdown'
    )

async def nid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📄 NID করতে: জন্ম নিবন্ধন, বাবা-মায়ের NID, চেয়ারম্যান সার্টিফিকেট লাগবে। যাবেন: নিয়ামতপুর নির্বাচন অফিস।")
async def birth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📜 জন্ম নিবন্ধন: টিকা কার্ড, বাবা-মায়ের NID নিয়ে ইউনিয়ন পরিষদে যান। bdris.gov.bd")
async def nagad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💰 নগদ PIN Reset: *167# > 8 > NID দিন।")
async def upazila(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏛️ নিয়ামতপুর উপজেলা, নওগাঁ। সময়: 9AM-4PM। প্রচারে - ITz Sobuj")
async def bazar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛒 শালবাড়ী বাজার - সকল দোকান শীঘ্রই যুক্ত হবে।")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("nid", nid))
app.add_handler(CommandHandler("birth", birth))
app.add_handler(CommandHandler("nagad", nagad))
app.add_handler(CommandHandler("upazila", upazila))
app.add_handler(CommandHandler("bazar", bazar))

print("Bot Running...")
app.run_polling()
