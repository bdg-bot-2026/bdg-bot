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
    return "Bot status: ONLINE (24/7 Exact Real-Time Synced Period Active)"

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
# ⏰ Exact Real-Time Synced Period Logic
# ==========================================
def get_ist_time():
    try:
        ist = pytz.timezone('Asia/Kolkata')
        return datetime.now(ist)
    except Exception:
        return datetime.utcnow() + timedelta(hours=5, minutes=30)

def get_current_1min_period():
    now = get_ist_time()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    total_minutes_today = int((now - midnight).total_seconds() // 60)
    
    date_prefix = now.strftime('%Y%m%d')
    base_game_period = 1000000 + total_minutes_today
    
    return f"{date_prefix}{base_game_period}"


# ==========================================
# 📊 Advanced AI Fully Random Trend Evaluator (10 Strategies)
# ==========================================
def get_high_tech_ai_prediction():
    strategies_weights = {
        "DRAGON_TREND": 15,       
        "THREE_BY_THREE": 12,     
        "CROSS_WAVE": 12,         
        "TWO_BY_TWO_ZONE": 10,    
        "STABLE_ZIGZAG": 10,      
        "SMART_MIXED": 10,
        "MIRROR_REFLECTION": 8,
        "FIBONACCI_STEP": 8,
        "MOMENTUM_WAVE": 8,
        "ALTERNATE_CLUSTER": 7
    }

    strategies = list(strategies_weights.keys())
    weights = list(strategies_weights.values())
    
    selected_strategy = random.choices(strategies, weights=weights, k=1)[0]

    start = random.choice(["BIG", "SMALL"])
    opposite = "SMALL" if start == "BIG" else "BIG"
    
    if selected_strategy == "DRAGON_TREND":
        pattern = [start] * random.randint(3, 5)
    elif selected_strategy == "THREE_BY_THREE":
        pattern = [start, start, opposite, opposite]
    elif selected_strategy == "CROSS_WAVE":
        pattern = [start, opposite, start, opposite]
    elif selected_strategy == "TWO_BY_TWO_ZONE":
        pattern = [start, start, opposite, opposite]
    elif selected_strategy == "STABLE_ZIGZAG":
        pattern = [start, opposite, start, opposite]
    elif selected_strategy == "MIRROR_REFLECTION":
        pattern = [start, opposite, opposite, start]
    elif selected_strategy == "FIBONACCI_STEP":
        pattern = [start, start, opposite, start]
    elif selected_strategy == "MOMENTUM_WAVE":
        pattern = [start, opposite, start, start]
    elif selected_strategy == "ALTERNATE_CLUSTER":
        pattern = [start, opposite, opposite, start]
    else:
        pattern = [start, opposite, start, opposite]

    return random.choice(pattern)


# ==========================================
# 🎨 Smart Color Evaluator Logic (Green & Red)
# ==========================================
def get_smart_trend_color(pred_text):
    if pred_text == "BIG":
        return random.choice(["GREEN 🟢", "GREEN 🟢", "RED 🔴"])
    else:
        return random.choice(["RED 🔴", "RED 🔴", "GREEN 🟢"])


# ==========================================
# 🚀 Telegram Automation 24/7 Main Loop
# ==========================================
async def send_auto_prediction(app):
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
                pred_text = get_high_tech_ai_prediction()
                color_text = get_smart_trend_color(pred_text)
                
                # এখানে হেডারটি এক লাইনে রাখার জন্য সংক্ষিপ্ত ও নিখুঁত করা হয়েছে
                msg = (
                    f"💎 <b>BDG WIN ULTRA AI VIP</b> 💎\n\n"
                    f"🔹 <b>PERIOD:</b> {period_num}\n"
                    f"🎯 <b>PREDICTION:</b> {pred_text}\n"
                    f"🎨 <b>COLOR:</b> {color_text}\n"
                    f"───────────────────\n"
                    f"💡 <i>Recommended: Safe 1-10 Level Martingale</i>"
                )
                
                await app.bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=msg,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup
                )
                
                last_sent_period = period_num

        except Exception as e:
            print(f"Error: {e}")

        await asyncio.sleep(1)


# ==========================================
# ⚙️ Main Application Launcher
# ==========================================
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    web_thread = threading.Thread(target=run_web, daemon=True)
    web_thread.start()
    
    print("BDG Win Exact Synced 24/7 AI Bot is running successfully...")
    
    await send_auto_prediction(app)

if __name__ == "__main__":
    asyncio.run(main())
    
