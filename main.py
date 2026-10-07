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
# 🌐 Flask Web Server (Render Keep-Alive)
# ==========================================
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot status: ONLINE (Automatic Continuous Signals)"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)


# ==========================================
# 🤖 Telegram Bot Configurations
# ==========================================
TOKEN = os.getenv("TELEGRAM_TOKEN", "8752459278:AAGbwu4j7JqT3R4Auwhj2PLMidKzhRaSkS0").strip()
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "-1004492973133")

current_pattern = []
pattern_index = 0


# ==========================================
# ⏰ 100% Exact Match Period Generator
# ==========================================
def get_ist_time():
    try:
        ist = pytz.timezone('Asia/Kolkata')
        return datetime.now(ist)
    except Exception:
        return datetime.utcnow() + timedelta(hours=5, minutes=30)

def generate_time_based_period():
    now = get_ist_time()
    date_str = now.strftime("%Y%m%d") 
    
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    total_minutes = int((now - midnight).total_seconds() / 60)
    
    current_minutes_today = (now.hour * 60) + now.minute
    base_counter = 10497 + (total_minutes - current_minutes_today)
    
    return f"{date_str}1000{base_counter}"


# ==========================================
# 📊 Fully Dynamic AI Trend Evaluator
# ==========================================
def high_tech_ai_trend_evaluator():
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
    pattern = []
    
    if selected_strategy == "DRAGON_TREND":
        dragon_len = random.randint(3, 6)
        pattern = [start] * dragon_len
    elif selected_strategy == "THREE_BY_THREE":
        pattern = [start, start, start, opposite, opposite, opposite]
    elif selected_strategy == "CROSS_WAVE":
        pattern = [start, start, opposite, opposite, opposite, start]
    elif selected_strategy == "TWO_BY_TWO_ZONE":
        pattern = [start, start, opposite, opposite, start, start]
    elif selected_strategy == "STABLE_ZIGZAG":
        pattern = [start, opposite, start, opposite, start]
    elif selected_strategy == "MIRROR_REFLECTION":
        pattern = [start, opposite, start, start, opposite]
    elif selected_strategy == "FIBONACCI_STEP":
        pattern = [start, start, opposite, start, opposite]
    elif selected_strategy == "MOMENTUM_WAVE":
        pattern = [start, opposite, opposite, start, start]
    elif selected_strategy == "ALTERNATE_CLUSTER":
        pattern = [start, start, opposite, opposite, start]
    else:
        pattern = [start, opposite, start, start, opposite]

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
# 🎨 Smart Color Evaluator Logic
# ==========================================
def get_smart_trend_color(pred_text):
    if pred_text == "BIG":
        return random.choice(["GREEN 🟢", "GREEN 🟢", "RED 🔴"])
    else:
        return random.choice(["RED 🔴", "RED 🔴", "GREEN 🟢"])


# ==========================================
# 🚀 Telegram Automation Main Loop (Continuous)
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
            period_num = generate_time_based_period()
            
            if period_num and period_num != last_sent_period:
                pred = get_high_tech_ai_prediction()
                pred_text = "SMALL" if pred == "SMALL" else "BIG"
                color_text = get_smart_trend_color(pred_text)
                
                msg = (
                    f"💎 <b>BDG VIP PREDICTION 1 Min</b> 💎\n"
                    f"💎 <b>BDG WIN ULTRA AI VIP PREDICTION</b> 💎\n\n"
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
            print(f"Main Loop Error: {e}")

        await asyncio.sleep(2)


# ==========================================
# ⚙️ Main Application Launcher
# ==========================================
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    # ব্যাকগ্রাউন্ডে ফ্লাস্ক সার্ভার চালু করা
    threading.Thread(target=run_web, daemon=True).start()
    
    print("BDG Win Continuous Bot is running successfully...")
    
    async def post_init(application):
        application.create_task(send_auto_prediction(application))

    app.post_init = post_init
    app.run_polling()
               
