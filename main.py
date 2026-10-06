import os
import random
from datetime import datetime
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
    return "Bot status: ONLINE (Absolute Period Match Fix)"

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
# ⏰ Direct Accurate Period Sync
# ==========================================
def get_current_1min_period():
    try:
        ist = pytz.timezone('Asia/Kolkata')
        now = datetime.now(ist)
    except Exception:
        now = datetime.utcnow()
        
    date_str = now.strftime('%Y%m%d')
    
    # আজকের দিনের শুরু থেকে কত মিনিট পার হয়েছে তার সঠিক হিসাব
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    total_minutes = int((now - midnight).total_seconds() // 60)
    
    # গেমের রিয়েল স্ট্রাকচার: YYYYMMDD + 1000 + total_minutes
    period = f"{date_str}1000{total_minutes}"
    return period


# ==========================================
# 🎲 Random Big/Small & Green/Red Generator
# ==========================================
def get_fully_random_prediction():
    pred_text = random.choice(["BIG", "SMALL"])
    color_text = random.choice(["GREEN 🟢", "RED 🔴"])
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
                    f"💡 <i>Rule: Safe 1-10 Level Martingale</i>"
                )
                
                await application.bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=msg,
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
        
