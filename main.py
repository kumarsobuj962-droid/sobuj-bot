import threading
import telebot
from telebot import types
from flask import Flask

# ===== BOSS SETTINGS =====
import os
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 7310026950
COURSE_LINK = "https://t.me/+KbQkJl5WDGNmMDQ1"
BKASH_NUMBER = "01770885382"
COURSE_FEE = "199 Tk"
# =========================

app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

# Pending payments memory
pending = {}

@app.route('/')
def home():
    return "BOSS Bot Live 24/7!"

@bot.message_handler(commands=['start'])
def start(m):
    text = f"""👋 স্বাগতম Sobuj Boss Course এ!

💰 কোর্স ফি: {COURSE_FEE}
📱 bKash Personal: {BKASH_NUMBER}

👉 টাকা পাঠিয়ে bKash TrxID টা এখানে পাঠাও
যেমন: DIR30PK1GV

✅ TrxID পাঠালে Admin Check করে Approve করবে, তারপর Auto Course Link পাবে!
"""
    bot.reply_to(m, text)

@bot.message_handler(func=lambda m: True)
def handle_trx(m):
    user_id = m.from_user.id
    trx = m.text.strip()

    if len(trx) < 8:
        bot.reply_to(m, "❌ সঠিক TrxID দাও বস! 10 অক্ষরের হবে। যেমন: DIR30PK1GV")
        return

    pending[user_id] = trx

    # User কে জানানো
    bot.reply_to(m, f"✅ TrxID পেয়েছি: `{trx}`\n⏳ Admin Approve এর জন্য অপেক্ষা করো, 2 মিনিটে Link পাবে!", parse_mode="Markdown")

    # Admin এর কাছে পাঠানো - Approval Button সহ
    username = f"@{m.from_user.username}" if m.from_user.username else "No Username"
    markup = types.InlineKeyboardMarkup()
    btn_approve = types.InlineKeyboardButton("✅ APPROVE", callback_data=f"approve_{user_id}")
    btn_reject = types.InlineKeyboardButton("❌ REJECT", callback_data=f"reject_{user_id}")
    markup.add(btn_approve, btn_reject)

    admin_text = f"""💰 New Payment Request!

👤 User: {username}
🆔 ID: {user_id}
💳 TrxID: {trx}
💵 Amount: {COURSE_FEE}

Approve করলে User Course Link পাবে!"""

    try:
        bot.send_message(ADMIN_ID, admin_text, reply_markup=markup)
    except Exception as e:
        print(f"Admin send error: {e}")

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.from_user.id!= ADMIN_ID:
        bot.answer_callback_query(call.id, "❌ তুমি Admin না!")
        return

    data = call.data
    target_id = int(data.split("_")[1])
    trx = pending.get(target_id, "Unknown")

    if data.startswith("approve_"):
        # User কে Course Link দেওয়া
        try:
            bot.send_message(target_id, f"""🎉 Payment Approved BOSS!

✅ তোমার TrxID: {trx} Confirm হয়েছে!

📚 তোমার Private Course Link:
👉 {COURSE_LINK}

⚠️ Link এ Click করে Join হয়ে যাও, 2 মিনিটের মধ্যে!""")
            bot.answer_callback_query(call.id, "✅ Approved!")
            bot.edit_message_text(f"✅ APPROVED: User {target_id} | TrxID: {trx}", call.message.chat.id, call.message.message_id)
            del pending[target_id]
        except Exception as e:
            bot.answer_callback_query(call.id, f"Error: {e}")

    elif data.startswith("reject_"):
        try:
            bot.send_message(target_id, f"❌ Payment Reject! TrxID {trx} সঠিক নয়। আবার সঠিক TrxID দাও বা Admin কে Contact করো: @SobujBoss")
            bot.answer_callback_query(call.id, "❌ Rejected!")
            bot.edit_message_text(f"❌ REJECTED: User {target_id} | TrxID: {trx}", call.message.chat.id, call.message.message_id)
            del pending[target_id]
        except:
            pass

def run_bot():
    print("BOSS Bot Starting...")
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
