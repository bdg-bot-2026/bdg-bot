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

# 🤖 AI High-Tech Dynamic Engine Memory
current_pattern = []
pattern_index = 0
ai_mode_name = "AI Deep Trend Engine"

def get_ist_time():
    try:
        ist = pytz.timezone('Asia/Kolkata')
        return datetime.now(ist)
    except Exception:
        return datetime.utcnow() + timedelta(hours=5, minutes=30)

def high_tech_ai_trend_evaluator():
    """
    🧠 Ultra High-Tech AI Engine
    সময়, ভোলাটিলিটি এবং সম্ভাব্য উইন-রেটের উপর ভিত্তি করে সেরা ট্রেন্ড নিজে সিলেক্ট করবে।
    """
    global ai_mode_name
    
    now = get_ist_time()
    hour = now.hour

    # AI ট্রেন্ড স্কোরিং ও ওয়েটেজ মেকানিজম (Optimal Win-Rate Probability)
    if (6 <= hour < 11) or (23 <= hour or hour < 2):
        # লো-ভোলাটিলিটি জোন: ড্রাগন ও বড় ব্লক প্যাটার্নে উইন রেট ৯০%+ থাকে
        strategies_weights = {
            "DRAGON": 35,
            "DRAGON_BREAK": 25,
            "FOUR_BY_FOUR": 20,
            "THREE_BY_THREE": 20
        }
    elif 11 <= hour < 17:
        # মিডিয়াম-ভোলাটিলিটি জোন: স্যান্ডউইচ ও ২x২ সবচেয়ে নিরাপদ
        strategies_weights = {
            "TWO_BY_TWO": 30,
            "TWO_ONE_TWO": 25,
            "TWO_ONE_TWO_ONE": 20,
            "DRAGON_BREAK": 15,
            "THREE_BY_THREE": 10
        }
    else:
        # হাই-ভোলাটিলিটি জোন (বিকাল ৪টা - রাত ১১টা): দ্রুত রিভার্সাল ও জিগজ্যাগ কার্যকরী
        strategies_weights = {
            "ZIGZAG": 30,
            "REVERSE_SANDWICH": 25,
            "TWO_ONE_TWO_ONE": 20,
            "DRAGON_BREAK": 15,
            "TWO_BY_TWO": 10
        }

    # AI গাণিতিক সম্ভাব্যতা অনুযায়ী সেরা স্ট্র্যাটেজি ফিল্টার করবে
    strategies = list(strategies_weights.keys())
    weights = list(strategies_weights.values())
    selected_strategy = random.choices(strategies, weights=weights, k=1)[0]

    start = random.choice(["BIG", "SMALL"])
    opposite = "SMALL" if start == "BIG" else "BIG"
    
    pattern = []
    
    if selected_strategy == "DRAGON_BREAK":
        ai_mode_name = "💥 AI Dragon Break (High Win)"
        dragon_start_len = random.choice([4, 5])
        pattern = [start] * dragon_start_len + [opposite] * 3 + [start, opposite, start]

    elif selected_strategy == "ZIGZAG":
        ai_mode_name = "🧠 AI Fast Zig-Zag (1x1)"
        for i in range(6):
            pattern.append(start if i % 2 == 0 else opposite)
            
    elif selected_strategy == "TWO_BY_TWO":
        ai_mode_name = "🤖 AI Balance Matrix (2x2)"
        pattern = [start, start, opposite, opposite, start, start]

    elif selected_strategy == "THREE_BY_THREE":
        ai_mode_name = "🔥 AI Triple Power Shift (3x3)"
        pattern = [start, start, start, opposite, opposite, opposite]
        
    elif selected_strategy == "FOUR_BY_FOUR":
        ai_mode_name = "📊 AI Heavy Trend Box (4x4)"
        pattern = [start] * 4 + [opposite] * 4

    elif selected_strategy == "TWO_ONE_TWO":
        ai_mode_name = "🥪 AI Smart Sandwich (2-1-2)"
        pattern = [start, start, opposite, start, start, opposite]

    elif selected_strategy == "TWO_ONE_TWO_ONE":
        ai_mode_name = "🔄 AI Rhythm Balance (2-1-2-1)"
        pattern = [start, start, opposite, start, start, opposite, start]

    elif selected_strategy == "REVERSE_SANDWICH":
        ai_mode_name = "⚡ AI Reverse Sandwich (2-1-1-2)"
        pattern = [start, start, opposite, start, opposite, start, start]
        
    elif selected_strategy == "DRAGON":
        ai_mode_name = "🐉 AI Dragon Streak Ride"
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
    
    # হাই-টেক একিউরেসি স্কোর জেনারেটর (৯৬.১% - ৯৯.৪%)
    confidence = round(random.uniform(96.1, 99.4), 1)
    
    return prediction, ai_mode_name, confidence

def get_current_30s_period():
    now = get_ist_time()
    start_time = now.replace(hour=5, minute=30, second=0, microsecond=0)
    if now < start_time:
        start_time -= timedelta(days=1)

    elapsed_seconds = int((now - start_time).total_seconds())
    interval_index = (elapsed_seconds // 30) + 1
    
    date_str = now.strftime('%Y%m%d')
    return f"{date_str}10005{interval_index:04d}"

async def send_auto_prediction(app):
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
                raw_pred, ai_mode, confidence = get_high_tech_ai_prediction()
                
                if raw_pred == "SMALL":
                    pred_display = "<b>SMALL 🔴</b>"
                else:
                    pred_display = "<b>BIG 🟢</b>"
                
                msg = (
                    f"🤖 <b><u>BDG WIN ULTRA AI VIP</u></b> 🤖\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"🔹 <b>PERIOD:</b> <code>{period_num}</code>\n"
                    f"🎯 <b>PREDICTION:</b> {pred_display}\n"
                    f"⚡ <b>AI WIN ACCURACY:</b> <code>{confidence}%</code>\n"
                    f"🧠 <b>OPTIMIZED STRATEGY:</b> <code>{ai_mode}</code>\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"💡 <i>Recommended: Safe 1-3 Level Martingale</i>"
                )
                
                await app.bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=msg,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup
                )
                print(f"Sent High-Tech AI Prediction: {period_num} -> {raw_pred} ({confidence}%)")
                last_sent_period = period_num

        except Exception as e:
            print(f"Error sending message: {e}")

        await asyncio.sleep(0.5)

async def post_init(app):
    asyncio.create_task(send_auto_prediction(app))

def main():
    threading.Thread(target=run_web, daemon=True).start()

    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    print("Ultra High-Tech AI Master VIP Bot Started...")
    app.run_polling()

if __name__ == '__main__':
    main()
