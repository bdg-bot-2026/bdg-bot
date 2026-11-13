import os
import random
from datetime import datetime, timedelta
import pytz
import asyncio
import threading
from collections import deque
from flask import Flask
from telegram.ext import ApplicationBuilder
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode


# ==========================================
# 🌐 Flask Web Server (For Render / Keep-Alive)
# ==========================================
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot status: ONLINE (Raxi Win 24/7 Testing Mode Active)"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)


# ==========================================
# 🤖 Telegram Bot Configurations
# ==========================================
TOKEN = "8937609482:AAFpxFnCk7ZI38QYnUNbUST2A6eZHnWuAHQ"
CHANNEL_ID = "@RexiWinAIPrediction"

current_pattern = []
pattern_index = 0

# 🧠 Stateful Trend Memory Buffer (Stores last 100 predictions for analysis)
prediction_history = deque(maxlen=100)


# ==========================================
# ⏰ Time & Live Game Period Synchronization
# ==========================================
def get_bd_time():
    try:
        bd_tz = pytz.timezone('Asia/Dhaka')
        return datetime.now(bd_tz)
    except Exception:
        return datetime.utcnow() + timedelta(hours=6)

def get_current_1min_period():
    now_utc = datetime.now(pytz.utc)
    date_str = now_utc.strftime("%Y%m%d")
    total_minutes_utc = (now_utc.hour * 60) + now_utc.minute
    period_count = 10000 + total_minutes_utc + 1
    return f"{date_str}1000{period_count}"


# ==========================================
# 📊 Advanced Stateful AI Trend Evaluator (100-Period Memory Analysis)
# ==========================================
def analytical_ai_trend_evaluator():
    recent_big_count = sum(1 for p in prediction_history if p == "BIG")
    recent_small_count = sum(1 for p in prediction_history if p == "SMALL")

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

    if len(prediction_history) >= 5:
        last_five = list(prediction_history)[-5:]
        if all(x == "BIG" for x in last_five) or all(x == "SMALL" for x in last_five):
            strategies_weights["DRAGON_TREND"] += 15

    strategies = list(strategies_weights.keys())
    weights = list(strategies_weights.values())
    selected_strategy = random.choices(strategies, weights=weights, k=1)[0]

    start = random.choice(["BIG", "SMALL"])
    if len(prediction_history) > 5:
        if recent_big_count > recent_small_count + 4:
            start = "SMALL"
        elif recent_small_count > recent_big_count + 4:
            start = "BIG"

    opposite = "SMALL" if start == "BIG" else "BIG"
    pattern = []
    
    if selected_strategy == "DRAGON_TREND":
        dragon_len = random.randint(4, 6)
        pattern = [start] * dragon_len
    elif selected_strategy == "THREE_BY_THREE":
        pattern = [start, start, start, opposite, opposite, opposite]
    elif selected_strategy == "CROSS_WAVE":
        pattern = [start, start, opposite, opposite, opposite, start]
    elif selected_strategy == "TWO_BY_TWO_ZONE":
        pattern = [start, start, opposite, opposite, start, start, opposite, opposite]
    elif selected_strategy == "STABLE_ZIGZAG":
        pattern = [start, opposite, start, opposite, start, opposite, start]
    elif selected_strategy == "MIRROR_REFLECTION":
        pattern = [start, opposite, start, start, opposite, start]
    elif selected_strategy == "FIBONACCI_STEP":
        pattern = [start, start, opposite, start, opposite, opposite]
    elif selected_strategy == "MOMENTUM_WAVE":
        pattern = [start, opposite, opposite, start, start, opposite]
    elif selected_strategy == "ALTERNATE_CLUSTER":
        pattern = [start, start, opposite, opposite, start, opposite]
    else:
        pattern = [start, opposite, start, start, opposite, start]

    return pattern

def get_high_tech_ai_prediction():
    global current_pattern, pattern_index, prediction_history
    if not current_pattern or pattern_index >= len(current_pattern):
        current_pattern = analytical_ai_trend_evaluator()
        pattern_index = 0
    
    raw_prediction = current_pattern[pattern_index]
    pattern_index += 1
    
    prediction_history.append(raw_prediction)
    return raw_prediction


# ==========================================
# 🎨 Smart Color Evaluator Logic
# ==========================================
def get_smart_trend_color(pred_text):
    if pred_text == "BIG":
        return random.choice(["GREEN 🟢", "GREEN 🟢", "RED 🔴"])
    else:
        return random.choice(["RED 🔴", "RED 🔴", "GREEN 🟢"])


# ==========================================
# 🚀 Telegram Automation Main Loop (24/7 Testing Mode Active)
# ==========================================
async def send_auto_prediction(app):
    last_sent_period = ""

    keyboard = [
        [InlineKeyboardButton("🎮 Play Raxi Win 🏆", url="https://raxiwin.com")],
        [InlineKeyboardButton("📊 Join VIP Channel", url="https://t.me/RexiWinAIPrediction")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    print("Raxi Win 24/7 Testing Mode Loop started... (Sending signals for every new period)")

    while True:
        try:
            # টাইম রেস্ট্রিকশন হাটিয়ে সরাসরি ট্রু করে দেওয়া হয়েছে যাতে ২৪ ঘণ্টা সিগন্যাল যায়
            period_num = get_current_1min_period()
            
            if period_num != last_sent_period:
                pred = get_high_tech_ai_prediction()
                pred_text = "SMALL" if pred == "SMALL" else "BIG"
                color_text = get_smart_trend_color(pred_text)
                
                msg = (
                    f"💎 <b>RAXI WIN 24/7 TESTING AI PREDICTION</b> 💎\n"
                    f"💎 <b>RAXI WIN VIP PREDICTION 1 Min</b> 💎\n\n"
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
                
                print(f"Test Signal sent successfully with 100-Period Memory Analysis for period: {period_num}")
                last_sent_period = period_num

        except Exception as e:
            print(f"Loop Error: {e}")

        await asyncio.sleep(2)


# ==========================================
# ⚙️ Main Application Launcher
# ==========================================
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    await app.initialize()
    await app.start()
    
    threading.Thread(target=run_web, daemon=True).start()
    
    print("Raxi Win 24/7 Testing Bot is fully running and active...")
    
    await send_auto_prediction(app)

if __name__ == "__main__":
    asyncio.run(main())
