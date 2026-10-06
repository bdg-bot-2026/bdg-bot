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

# ==========================================
# 🌐 Flask Web Server
# ==========================================
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot status: ONLINE (Random Green & Red Only)"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)


# ==========================================
# 🤖 Telegram Bot Configurations
# ==========================================
RAW_TOKEN = "8752459278:AAGbwu4j7JqT3R4Auwhj2PLMidKzhRaSkS0"
TOKEN = RAW_TOKEN.strip()
CHANNEL_ID = "@bdgplayvipwin"


# ==========================================
# ⏰ Exact Real-time Period Synchronization
# ==========================================
def get_ist_time():
    try:
        ist = pytz.timezone('Asia/Kolkata')
        return datetime.now(ist)
    except Exception:
        return datetime.utcnow() + timedelta(hours=5, minutes=30)

def get_current_1min_period():
    now = get_ist_time()
    date_str = now.strftime('%Y%m%d')
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    total_minutes = int((now - start_of_day).total_seconds() // 60)
    
    current_period = int(f"{date_str}1000") + total_minutes
    return str(current_period)


# ==========================================
# 🎲 Random Big/Small & Green/Red Only Generator
# ==========================================
def get_fully_random_prediction():
    pred_text = random.choice(["BIG", "SMALL"])
    
    # শুধুমাত্র Green এবং Red রাখা হলো (কোনো Violet নেই)
    colors = [
        "GREEN 🟢", 
        "RED 🔴"
    ]
    color_text = random.choice(colors)
    
    return pred_text, color_text


# ==========================================
# 🚀 Telegram Automation Functions
# ==========================================
async def send_auto_prediction(application):
    last_sent_period = ""
    
    keyboard = [
        [InlineKeyboardButton("🎮 Play BDG Win 🏆", url="https://bdgwin.com")],
        [InlineKeyboardButton("📊 Join VIP Channel", url="https://t.me/bdgplayvipwin")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    while True:
        try:
            period_num = get_current_1min_period()
            if period_num != last_sent_period:
                pred_text, color_text = get_fully_random_prediction()
                
                msg = (
                    f"💎 <b>BDG WIN 1 Min PREDICTION</b> 💎\n\n"
                    f"🔹 <b>PERIOD:</b> {period_num}\n"
                    f"🎯 <b>PREDICTION:</b> {pred_text}\n"
                    f"🎨 <b>SUGGESTED COLOR:</b> {color_text}\n"
                    f"───────────────────\n"
                    f"💡 <i>Rule: Safe 1-10 Level Martingale (Testing Active)</i>"
                )
                
                await application.bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=msg,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup
                )
                
                await asyncio.sleep(50)
                
                post_msg = (
                    f"📢 <b>PERIOD RESULT UPDATE</b> 📢\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"📌 <b>Period:</b> {period_num}\n"
                    f"🎯 <b>Our Prediction was:</b> {pred_text} ({color_text})\n"
                    f"✅ <i>Check your game history. If Level 1 win, great! If not, proceed safely up to 10-Level Martingale.</i>\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━"
                )
                await application.bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=post_msg,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup
                )
                
                last_sent_period = period_num

        except Exception as e:
            print(f"Error in loop: {e}")

        await asyncio.sleep(1)

async def main_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    asyncio.create_task(send_auto_prediction(application))
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    while True:
        await asyncio.sleep(3600)


# ==========================================
# 🏁 Main Function
# ==========================================
if __name__ == '__main__':
    threading.Thread(target=run_web, daemon=True).start()
    try:
        asyncio.run(main_bot())
    except (KeyboardInterrupt, SystemExit):
        pass
        
