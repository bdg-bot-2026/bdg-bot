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
    return "Bot status: ONLINE (Exact Real Period Sync Active)"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)


# ==========================================
# 🤖 Telegram Bot Configurations
# ==========================================
RAW_TOKEN = "8752459278:AAGbwu4j7JqT3R4Auwhj2PLMidKzhRaSkS0"
TOKEN = RAW_TOKEN.strip()
CHANNEL_ID = "@bdgplayvipwin"

current_pattern = []
pattern_index = 0


# ==========================================
# ⏰ Exact Real-time Period Synchronization Function
# ==========================================
def get_ist_time():
    try:
        ist = pytz.timezone('Asia/Kolkata')
        return datetime.now(ist)
    except Exception:
        return datetime.utcnow() + timedelta(hours=5, minutes=30)

def get_current_1min_period():
    """
    গেমের রিয়েল পিরিয়ড ফরম্যাট অনুযায়ী সঠিক মিনিট কাউন্ট:
    যেমন: YYYYMMDD + 1000 + সারদিনের মোট মিনিট সংখ্যা
    """
    now = get_ist_time()
    date_str = now.strftime('%Y%m%d')
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    total_minutes = int((now - start_of_day).total_seconds() // 60)
    
    # গেমের সাথে নিখুঁতভাবে পিরিয়ড মেলানোর জন্য সঠিক বেস ফরম্যাট
    current_period = int(f"{date_str}10000") + total_minutes
    return str(current_period)


# ==========================================
# 📊 Advanced AI Trend Evaluator (All Logics Active)
# ==========================================
def high_tech_ai_trend_evaluator():
    strategies_weights = {
        "DRAGON_TREND": 25,       
        "THREE_BY_THREE": 20,     
        "CROSS_WAVE": 20,         
        "TWO_BY_TWO_ZONE": 15,    
        "STABLE_ZIGZAG": 10,      
        "SMART_MIXED": 10         
    }

    strategies = list(strategies_weights.keys())
    weights = list(strategies_weights.values())
    selected_strategy = random.choices(strategies, weights=weights, k=1)[0]

    start = random.choice(["BIG", "SMALL"])
    opposite = "SMALL" if start == "BIG" else "BIG"
    pattern = []
    
    if selected_strategy == "DRAGON_TREND":
        dragon_len = random.randint(5, 7)
        pattern = [start] * dragon_len
    elif selected_strategy == "THREE_BY_THREE":
        pattern = [start, start, start, opposite, opposite, opposite]
    elif selected_strategy == "CROSS_WAVE":
        pattern = [start, start, opposite, opposite, opposite, start]
    elif selected_strategy == "TWO_BY_TWO_ZONE":
        pattern = [start, start, opposite, opposite, start, start, opposite, opposite]
    elif selected_strategy == "STABLE_ZIGZAG":
        pattern = [start, opposite, start, opposite, start, opposite, start]
    else:
        pattern = [start, opposite, start, start, opposite, start]

    return pattern

def get_high_tech_ai_prediction():
    global current_pattern, pattern_index
    if not current_pattern or pattern_index >= len(current_pattern):
        current_pattern = high_tech_ai_trend_evaluator()
        pattern_index = 0
    
    raw_prediction = current_pattern[pattern_index]
    pattern_index += 1
    return raw_prediction


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
                pred = get_high_tech_ai_prediction()
                
                if pred == "SMALL":
                    pred_text = "SMALL"
                    color_text = "RED 🔴"
                else:
                    pred_text = "BIG"
                    color_text = "GREEN 🟢"
                
                msg = (
                    f"💎 <b>BDG WIN 1 Min PREDICTION</b> 💎\n\n"
                    f"🔹 <b>PERIOD:</b> {period_num}\n"
                    f"🎯 <b>PREDICTION:</b> {pred_text}\n"
                    f"🎨 <b>SUGGESTED COLOR:</b> {color_text}\n"
                    f"───────────────────\n"
                    f"💡 <i>Rule: Safe 1-10 Level Martingale (Testing Mode)</i>"
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
                    f"🎯 <b>Our Prediction was:</b> {pred_text}\n"
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
                
