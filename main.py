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

# Flask Web Server (Render বা অন্য ক্লাউডে লাইভ রাখার জন্য)
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot status: ONLINE (Reverse Signal Mode)"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

# Telegram Bot Configurations
RAW_TOKEN = "8752459278:AAGbwu4j7JqT3R4Auwhj2PLMidKzhRaSkS0"
TOKEN = RAW_TOKEN.strip()
CHANNEL_ID = "@bdgplayvipwin"

current_pattern = []
pattern_index = 0

def get_ist_time():
    """IST (Indian Standard Time) বা UTC টাইম রিটার্ন করে"""
    try:
        ist = pytz.timezone('Asia/Kolkata')
        return datetime.now(ist)
    except Exception:
        return datetime.utcnow() + timedelta(hours=5, minutes=30)

def high_tech_ai_trend_evaluator():
    """সময় অনুযায়ী বিভিন্ন স্ট্র্যাটেজি এবং প্যাটার্ন জেনারেট করে"""
    now = get_ist_time()
    hour = now.hour

    if (6 <= hour < 11) or (23 <= hour or hour < 2):
        strategies_weights = {
            "DRAGON_CONTROL": 30,
            "THREE_ONE_THREE": 25,
            "WAVE_UP_DOWN": 20,
            "FOUR_BY_FOUR": 15,
            "THREE_BY_THREE": 10
        }
    elif 11 <= hour < 17:
        strategies_weights = {
            "DOUBLE_PAIR_ZONE": 25,
            "THREE_ONE_THREE": 25,
            "ZIGZAG_MIXED": 20,
            "TWO_ONE_TWO_ONE": 15,
            "DRAGON_CONTROL": 15
        }
    else:
        strategies_weights = {
            "ZIGZAG_MIXED": 25,
            "THREE_ONE_THREE": 25,
            "DOUBLE_PAIR_ZONE": 20,
            "TWO_ONE_TWO_ONE": 15,
            "WAVE_UP_DOWN": 15
        }

    strategies = list(strategies_weights.keys())
    weights = list(strategies_weights.values())
    selected_strategy = random.choices(strategies, weights=weights, k=1)[0]

    start = random.choice(["BIG", "SMALL"])
    opposite = "SMALL" if start == "BIG" else "BIG"
    pattern = []
    
    if selected_strategy == "THREE_ONE_THREE":
        pattern = [start, start, start, opposite, start, start, start]
    elif selected_strategy == "DRAGON_CONTROL":
        dragon_len = random.choice([5, 6])
        pattern = [start] * dragon_len + [opposite, start]
    elif selected_strategy == "ZIGZAG_MIXED":
        for i in range(6):
            pattern.append(start if i % 2 == 0 else opposite)
    elif selected_strategy == "DOUBLE_PAIR_ZONE":
        pattern = [start, start, opposite, opposite, start, start]
    elif selected_strategy == "THREE_BY_THREE":
        pattern = [start, start, start, opposite, opposite, opposite]
    elif selected_strategy == "FOUR_BY_FOUR":
        pattern = [start] * 4 + [opposite] * 4
    elif selected_strategy == "WAVE_UP_DOWN":
        pattern = [start, start, opposite, start, opposite, opposite, start]
    elif selected_strategy == "TWO_ONE_TWO_ONE":
        pattern = [start, start, opposite, start, start, opposite, start]
    else:
        pattern = [start, start, opposite, start, opposite, start, start]

    return pattern

def get_high_tech_ai_prediction():
    """প্যাটার্ন থেকে পরবর্তী প্রেডিকশন ফেচ করে এবং তা রিভার্স (উল্টো) করে দেয়"""
    global current_pattern, pattern_index
    if not current_pattern or pattern_index >= len(current_pattern):
        current_pattern = high_tech_ai_trend_evaluator()
        pattern_index = 0
    
    raw_prediction = current_pattern[pattern_index]
    pattern_index += 1
    
    # রিভার্স লজিক: BIG হলে SMALL এবং SMALL হলে BIG রিটার্ন করবে
    reversed_prediction = "SMALL" if raw_prediction == "BIG" else "BIG"
    return reversed_prediction

def get_current_30s_period():
    """৩০ সেকেন্ডের গেম পিরিয়ড আইডি জেনারেট করে"""
    now = get_ist_time()
    start_time = now.replace(hour=5, minute=30, second=0, microsecond=0)
    if now < start_time:
        start_time -= timedelta(days=1)
    elapsed_seconds = int((now - start_time).total_seconds())
    interval_index = (elapsed_seconds // 30) + 1
    date_str = now.strftime('%Y%m%d')
    return f"{date_str}10005{interval_index:04d}"

async def send_auto_prediction(app):
    """স্বয়ংক্রিয়ভাবে টেলিগ্রাম চ্যানেলে রিভার্স সিগন্যাল পাঠাতে থাকে"""
    last_sent_period = ""
    keyboard = [
        [InlineKeyboardButton("🎮 Play BDG Win 🏆", url="https://bdgwin.com")],
        [InlineKeyboardButton("📊 Join VIP Channel", url="https://t.me/bdgplayvipwin")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    while True:
        try:
            period_num = get_current_30s_period()
            if period_num != last_sent_period:
                pred = get_high_tech_ai_prediction()
                pred_display = "<b>SMALL 🔴</b>" if pred == "SMALL" else "<b>BIG 🟢</b>"
                
                msg = (
                    f"🤖 <b><u>BDG WIN ULTRA AI VIP (REVERSE)</u></b> 🤖\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"🔹 <b>PERIOD:</b> <code>{period_num}</code>\n"
                    f"🎯 <b>PREDICTION:</b> {pred_display}\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"💡 <i>Recommended: Safe 1-6 Level Martingale</i>"
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

        await asyncio.sleep(0.5)

async def post_init(app):
    asyncio.create_task(send_auto_prediction(app))

def main():
    # ব্যাকগ্রাউন্ডে Flask সার্ভার রান করার জন্য Thread শুরু করা হলো
    threading.Thread(target=run_web, daemon=True).start()
    
    # টেলিগ্রাম বট অ্যাপ ইনিশিয়ালাইজ এবং রান করা
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    app.run_polling()

if __name__ == '__main__':
    main()
    
