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

current_pattern = []
pattern_index = 0

def get_ist_time():
    try:
        ist = pytz.timezone('Asia/Kolkata')
        return datetime.now(ist)
    except Exception:
        return datetime.utcnow() + timedelta(hours=5, minutes=30)

def high_tech_ai_trend_evaluator():
    now = get_ist_time()
    hour = now.hour

    if (6 <= hour < 11) or (23 <= hour or hour < 2):
        strategies_weights = {
            "DRAGON": 30,
            "THREE_ONE_THREE": 25,
            "DRAGON_BREAK": 20,
            "FOUR_BY_FOUR": 15,
            "THREE_BY_THREE": 10
        }
    elif 11 <= hour < 17:
        strategies_weights = {
            "TWO_BY_TWO": 25,
            "THREE_ONE_THREE": 25,
            "TWO_ONE_TWO": 20,
            "TWO_ONE_TWO_ONE": 15,
            "DRAGON_BREAK": 15
        }
    else:
        strategies_weights = {
            "ZIGZAG": 25,
            "THREE_ONE_THREE": 25,
            "REVERSE_SANDWICH": 20,
            "TWO_ONE_TWO_ONE": 15,
            "TWO_BY_TWO": 15
        }

    strategies = list(strategies_weights.keys())
    weights = list(strategies_weights.values())
    selected_strategy = random.choices(strategies, weights=weights, k=1)[0]

    start = random.choice(["BIG", "SMALL"])
    opposite = "SMALL" if start == "BIG" else "BIG"
    pattern = []
    
    if selected_strategy == "THREE_ONE_THREE":
        pattern = [start, start, start, opposite, start, start, start]
    elif selected_strategy == "DRAGON_BREAK":
        dragon_start_len = random.choice([4, 5])
        pattern = [start] * dragon_start_len + [opposite] * 3 + [start, opposite, start]
    elif selected_strategy == "ZIGZAG":
        for i in range(6):
            pattern.append(start if i % 2 == 0 else opposite)
    elif selected_strategy == "TWO_BY_TWO":
        pattern = [start, start, opposite, opposite, start, start]
    elif selected_strategy == "THREE_BY_THREE":
        pattern = [start, start, start, opposite, opposite, opposite]
    elif selected_strategy == "FOUR_BY_FOUR":
        pattern = [start] * 4 + [opposite] * 4
    elif selected_strategy == "TWO_ONE_TWO":
        pattern = [start, start, opposite, start, start, opposite]
    elif selected_strategy == "TWO_ONE_TWO_ONE":
        pattern = [start, start, opposite, start, start, opposite, start]
    elif selected_strategy == "REVERSE_SANDWICH":
        pattern = [start, start, opposite, start, opposite, start, start]
    elif selected_strategy == "DRAGON":
        dragon_len = random.choice([5, 6])
        pattern = [start] * dragon_len

    return pattern

def get_high_tech_ai_prediction():
    global current_pattern, pattern_index
    if not current_pattern or pattern_index >= len(current_pattern):
        current_pattern = high_tech_ai_trend_evaluator()
        pattern_index = 0
    prediction = current_pattern[pattern_index]
    pattern_index += 1
    return prediction

def get_current_30s_period():
    now = get_ist_time()
    start_time = now.replace(hour=5, minute=30, second=0, microsecond=0)
    if now < start_time:
        start_time -= timedelta(days=1)
    elapsed_seconds = int((now - start_time).total_seconds())
    interval_index = (elapsed_seconds // 30) + 1
    date_str = now.strftime('%Y%m%d')
    return f"{date_str}10005{interval_index:04d}"

# 🕒 ৫টি নির্দিষ্ট টাইম স্লট (প্রতিটি ১ ঘণ্টা করে চলবে)
def is_active_prediction_time():
    now = get_ist_time()
    current_hour = now.hour

    active_slots = [
        (7, 8),    # Slot 1: Morning 7:00 AM - 8:00 AM
        (10, 11),  # Slot 2: Morning 10:00 AM - 11:00 AM
        (14, 15),  # Slot 3: Afternoon 2:00 PM - 3:00 PM
        (19, 20),  # Slot 4: Evening 7:00 PM - 8:00 PM
        (22, 23)   # Slot 5: Night 10:00 PM - 11:00 PM
    ]

    for start_h, end_h in active_slots:
        if start_h <= current_hour < end_h:
            return True
            
    return False

async def send_auto_prediction(app):
    last_sent_period = ""
    keyboard = [
        [InlineKeyboardButton("🎮 Play BDG Win 🏆", url="https://bdgwin.com")],
        [InlineKeyboardButton("📊 Join VIP Channel", url="https://t.me/bdgplayvipwin")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    while True:
        try:
            if is_active_prediction_time():
                period_num = get_current_30s_period()
                if period_num != last_sent_period:
                    raw_pred = get_high_tech_ai_prediction()
                    pred_display = "<b>SMALL 🔴</b>" if raw_pred == "SMALL" else "<b>BIG 🟢</b>"
                    
                    msg = (
                        f"🤖 <b><u>BDG WIN ULTRA AI VIP</u></b> 🤖\n"
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
            else:
                await asyncio.sleep(10)

        except Exception as e:
            print(f"Error: {e}")

        await asyncio.sleep(0.5)

async def post_init(app):
    asyncio.create_task(send_auto_prediction(app))

def main():
    threading.Thread(target=run_web, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    app.run_polling()

if __name__ == '__main__':
    main()
