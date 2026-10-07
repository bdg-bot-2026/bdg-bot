import os
import random
from datetime import datetime, timedelta
import pytz
import asyncio
import threading
from flask import Flask
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

# ==========================================
# 🌐 Flask Web Server (Render Keep-Alive)
# ==========================================
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot status: ONLINE (Exact Screen Match Period Loop)"

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
# ⏰ 100% Exact Screen Match Period Generator
# ==========================================
def get_ist_time():
    try:
        ist = pytz.timezone('Asia/Kolkata')
        return datetime.now(ist)
    except Exception:
        return datetime.utcnow() + timedelta(hours=5, minutes=30)

def generate_exact_game_period():
    now = get_ist_time()
    date_str = now.strftime("%Y%m%d")
    
    # আজকের দিন শুরুর পর থেকে মোট কত মিনিট পার হয়েছে তা নিখুঁতভাবে বের করা
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    total_minutes = int((now - midnight).total_seconds() / 60)
    
    # আপনার স্ক্রিনশটের লেটেস্ট পিরিয়ড (10540) অনুযায়ী বেস কাউন্টার সেট করা হয়েছে
    current_minutes_today = (now.hour * 60) + now.minute
    base_counter = 10540 + (total_minutes - current_minutes_today)
    
    return f"{date_str}1000{base_counter}"


# ==========================================
# 📊 AI Trend Evaluator
# ==========================================
def high_tech_ai_trend_evaluator():
    strategies = ["DRAGON_TREND", "THREE_BY_THREE", "CROSS_WAVE", "STABLE_ZIGZAG"]
    selected_strategy = random.choice(strategies)

    start = random.choice(["BIG", "SMALL"])
    opposite = "SMALL" if start == "BIG" else "BIG"
    
    if selected_strategy == "DRAGON_TREND":
        pattern = [start] * 4
    elif selected_strategy == "THREE_BY_THREE":
        pattern = [start, start, opposite, opposite]
    elif selected_strategy == "CROSS_WAVE":
        pattern = [start, opposite, start, opposite]
    else:
        pattern = [start, start, opposite, start]

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
        return random.choice(["GREEN 🟢", "RED 🔴"])
    else:
        return random.choice(["RED 🔴", "GREEN 🟢"])


# ==========================================
# 🚀 Direct Async Message Sender Loop
# ==========================================
async def main_bot_loop():
    bot = Bot(token=TOKEN)
    last_sent_period = ""
    
    keyboard = [
        [InlineKeyboardButton("🎮 Play BDG Win 🏆", url="https://bdgwin.com")],
        [InlineKeyboardButton("📊 Join VIP Channel", url="https://t.me/bdgplayvipwin")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    print("BDG Win Signal Sender is active with exact screen match...")

    while True:
        try:
            period_num = generate_exact_game_period()
            
            # প্রতি মিনিটে নতুন পিরিয়ড শুরু হওয়া মাত্র সিগন্যাল পাঠাবে
            if period_num != last_sent_period:
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
                
                await bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=msg,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup
                )
                
                print(f"Signal successfully sent for period: {period_num}")
                last_sent_period = period_num

        except Exception as e:
            print(f"Error in sending message: {e}")

        # প্রতি ২ সেকেন্ড পর পর লুপ চেক করবে যাতে কোনো মিনিট মিস না হয়
        await asyncio.sleep(2)


# ==========================================
# ⚙️ Main Application Launcher
# ==========================================
if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    asyncio.run(main_bot_loop())
    
