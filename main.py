import os
import random
from datetime import datetime, timedelta
import pytz
import asyncio
import threading
from flask import Flask
from telegram import Bot
from telegram.constants import ParseMode

# ==========================================
# 🌐 Flask Web Server (Keep-Alive)
# ==========================================
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot status: ONLINE (Clean & Direct Loop)"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)


# ==========================================
# 🤖 Telegram Configurations
# ==========================================
TOKEN = os.getenv("TELEGRAM_TOKEN", "8752459278:AAGbwu4j7JqT3R4Auwhj2PLMidKzhRaSkS0").strip()
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "-1004492973133")

current_pattern = []
pattern_index = 0


# ==========================================
# ⏰ Exact Period Generator Logic
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
    
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    total_minutes = int((now - midnight).total_seconds() / 60)
    
    current_minutes_today = (now.hour * 60) + now.minute
    base_counter = 10540 + (total_minutes - current_minutes_today)
    
    return f"{date_str}1000{base_counter}"


# ==========================================
# 📊 AI Prediction Logic
# ==========================================
def get_high_tech_ai_prediction():
    strategies = [["BIG", "SMALL"], ["SMALL", "BIG", "BIG"], ["BIG", "BIG", "SMALL"], ["SMALL", "SMALL"]]
    global current_pattern, pattern_index
    if not current_pattern or pattern_index >= len(current_pattern):
        current_pattern = random.choice(strategies)
        pattern_index = 0
    
    pred = current_pattern[pattern_index]
    pattern_index += 1
    return pred

def get_smart_trend_color(pred_text):
    if pred_text == "BIG":
        return "GREEN 🟢"
    else:
        return "RED 🔴"


# ==========================================
# 🚀 Direct Async Message Loop
# ==========================================
async def main_bot_loop():
    bot = Bot(token=TOKEN)
    last_sent_period = ""
    
    print("Bot loop started successfully. Waiting for exact period match...")

    while True:
        try:
            period_num = generate_exact_game_period()
            
            if period_num != last_sent_period:
                pred_text = get_high_tech_ai_prediction()
                color_text = get_smart_trend_color(pred_text)
                
                msg = (
                    f"💎 <b>BDG VIP PREDICTION 1 Min</b> 💎\n\n"
                    f"🔹 <b>PERIOD:</b> {period_num}\n"
                    f"🎯 <b>PREDICTION:</b> {pred_text}\n"
                    f"🎨 <b>COLOR:</b> {color_text}\n"
                    f"───────────────────\n"
                    f"💡 <i>Recommended: Safe 1-10 Level Martingale</i>"
                )
                
                await bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=msg,
                    parse_mode=ParseMode.HTML
                )
                
                print(f"Successfully sent signal for period: {period_num}")
                last_sent_period = period_num

        except Exception as e:
            print(f"Error occurred in loop: {e}")

        await asyncio.sleep(1)


# ==========================================
# ⚙️ Main Launcher
# ==========================================
if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    asyncio.run(main_bot_loop())
    
