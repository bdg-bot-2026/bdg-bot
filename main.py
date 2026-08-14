import os
import random
from datetime import datetime, timedelta
import pytz
import asyncio
import threading
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder
from telegram.constants import ParseMode

app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot status: ONLINE"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

RAW_TOKEN = "8752459278:AAGbwu4j7JqT3R4Auwhj2PLMidKzhRaSkS0"
TOKEN = RAW_TOKEN.strip()

CHANNEL_ID = "@bdgplayvipwin"

# 🧠 স্মার্ট প্যাটার্ন ট্র্যাকার (Smart Pattern Logic)
last_prediction = None
streak_count = 0

def get_smart_prediction():
    global last_prediction, streak_count
    
    choices = ["SMALL", "BIG"]
    
    if last_prediction is None:
        selected = random.choice(choices)
        last_prediction = selected
        streak_count = 1
        return selected

    # টানা ৪ বার বা তার বেশি একই ফলাফল এলে অপোজিট সিগন্যাল ফায়ার করবে
    if streak_count >= 4:
        selected = "BIG" if last_prediction == "SMALL" else "SMALL"
        last_prediction = selected
        streak_count = 1
        return selected

    # ৬০% সম্ভাবনা থাকে আগের ট্রেন্ড ধরে রাখার, ৪০% সম্ভাবনা ট্রেন্ড পরিবর্তনের
    if random.random() < 0.60:
        selected = last_prediction
        streak_count += 1
    else:
        selected = "BIG" if last_prediction == "SMALL" else "SMALL"
        last_prediction = selected
        streak_count = 1

    return selected

def get_current_30s_period():
    try:
        ist = pytz.timezone('Asia/Kolkata')
        now = datetime.now(ist)
    except Exception:
        now = datetime.utcnow() + timedelta(hours=5, minutes=30)

    start_time = now.replace(hour=5, minute=30, second=0, microsecond=0)
    if now < start_time:
        start_time -= timedelta(days=1)

    elapsed_seconds = int((now - start_time).total_seconds())
    interval_index = (elapsed_seconds // 30) + 1
    
    date_str = now.strftime('%Y%m%d')
    return f"{date_str}10005{interval_index:04d}"

async def send_auto_prediction(app):
    last_sent_period = ""
    
    # 🔘 Play BDG Win ও VIP চ্যানেল ইনলাইন বাটন
    keyboard = [
        [InlineKeyboardButton("🎮 Play BDG Win 🏆", url="https://bdgwin.com")],
        [InlineKeyboardButton("📊 Join VIP Channel", url="https://t.me/bdgplayvipwin")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    while True:
        try:
            period_num = get_current_30s_period()
            
            if period_num != last_sent_period:
                # স্মার্ট অ্যালগরিদম দিয়ে প্রেডিকশন তৈরি
                raw_pred = get_smart_prediction()
                
                # মোটা (Bold) টেক্সট ফরম্যাট
                if raw_pred == "SMALL":
                    pred_display = "<b>SMALL 🔴</b>"
                else:
                    pred_display = "<b>BIG 🟢</b>"
                
                # প্রিমিয়াম ভিআইপি ফরম্যাট
                msg = (
                    f"🏆 <b><u>BDG WIN 30 SEC VIP</u></b> 🏆\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"🔹 <b>PERIOD:</b> <code>{period_num}</code>\n"
                    f"🎯 <b>PREDICTION:</b> {pred_display}\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"💡 <i>1-10 Level Martingale Use Karain</i>"
                )
                
                await app.bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=msg,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup
                )
                print(f"Sent smart prediction for period: {period_num} -> {raw_pred}")
                last_sent_period = period_num

        except Exception as e:
            print(f"Error sending message: {e}")

        await asyncio.sleep(0.5)

async def post_init(app):
    asyncio.create_task(send_auto_prediction(app))

def main():
    threading.Thread(target=run_web, daemon=True).start()

    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    print("Bot is starting...")
    app.run_polling()

if __name__ == '__main__':
    main()
