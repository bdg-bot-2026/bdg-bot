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
    return "Bot status: ONLINE (All Logics, Alerts & Period Sync)"

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
# ⏰ Time & AI Trend Evaluator Functions
# ==========================================
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
    global current_pattern, pattern_index
    if not current_pattern or pattern_index >= len(current_pattern):
        current_pattern = high_tech_ai_trend_evaluator()
        pattern_index = 0
    
    raw_prediction = current_pattern[pattern_index]
    pattern_index += 1
    return raw_prediction

def get_current_1min_period():
    """১ মিনিটের গেমের রিয়েল পিরিয়ড আইডি জেনারেট করে"""
    now = get_ist_time()
    date_str = now.strftime('%Y%m%d')
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    total_minutes = int((now - start_of_day).total_seconds() // 60)
    
    base_period = int(f"{date_str}100000000")
    current_period = base_period + total_minutes + 1090
    return str(current_period)


# ==========================================
# 🚀 Telegram Automation Functions
# ==========================================
async def send_auto_prediction(app):
    last_sent_period = ""
    last_alert_date_session = ""    
    last_promo_date_session = ""    
    last_next_date_session = ""     
    
    keyboard = [
        [InlineKeyboardButton("🎮 Play BDG Win 🏆", url="https://bdgwin.com")],
        [InlineKeyboardButton("📊 Join VIP Channel", url="https://t.me/bdgplayvipwin")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    while True:
        try:
            now = get_ist_time()
            hour = now.hour
            minute = now.minute
            current_date_str = now.strftime('%Y-%m-%d')

            alert_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Ready & Deposit", url="https://bdgwin.com")],
                [InlineKeyboardButton("📢 Channel Link", url="https://t.me/bdgplayvipwin")]
            ])

            # ১. সেশন শুরুর আগের ৫ মিনিটের অ্যালার্ট
            if hour == 6 and 55 <= minute < 60:
                alert_key = f"{current_date_str}_MORNING_ALERT"
                if last_alert_date_session != alert_key:
                    await send_ready_alert(app, "Morning Session (7:00 AM)", alert_markup)
                    last_alert_date_session = alert_key

            elif hour == 13 and 55 <= minute < 60:
                alert_key = f"{current_date_str}_AFTERNOON_ALERT"
                if last_alert_date_session != alert_key:
                    await send_ready_alert(app, "Afternoon Session (2:00 PM)", alert_markup)
                    last_alert_date_session = alert_key

            elif hour == 19 and 55 <= minute < 60:
                alert_key = f"{current_date_str}_NIGHT_ALERT"
                if last_alert_date_session != alert_key:
                    await send_ready_alert(app, "Night Session (8:00 PM)", alert_markup)
                    last_alert_date_session = alert_key


            # ২. মূল সিগন্যাল পাঠানোর অংশ (সকাল ৭-১০, দুপুর ২-৫, রাত ৮-১১ ইত্যাদি অথবা আপনার ইচ্ছামতো সময়)
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


            promo_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Join & Start Refer", url="https://bdgwin.com")],
                [InlineKeyboardButton("💎 Contact For Support", url="https://t.me/bdgplayvipwin")]
            ])

            # ৩. সেশন শেষ হওয়ার পরের প্রমোশন মেসেজ
            if (hour == 7 and minute == 36) or (hour == 14 and minute == 36) or (hour == 20 and minute == 36):
                promo_key = f"{current_date_str}_{hour}_PROMO"
                if last_promo_date_session != promo_key:
                    await send_referral_promo(app, promo_markup)
                    last_promo_date_session = promo_key

            # ৪. পরবর্তী সেশনের আপডেট মেসেজ
            if hour == 7 and minute == 37:
                next_key = f"{current_date_str}_MORNING_NEXT"
                if last_next_date_session != next_key:
                    await send_next_session_info(app, "Afternoon Session", "2:00 PM")
                    last_next_date_session = next_key

            elif hour == 14 and minute == 37:
                next_key = f"{current_date_str}_AFTERNOON_NEXT"
                if last_next_date_session != next_key:
                    await send_next_session_info(app, "Night Session", "8:00 PM")
                    last_next_date_session = next_key

            elif hour == 20 and minute == 37:
                next_key = f"{current_date_str}_NIGHT_NEXT"
                if last_next_date_session != next_key:
                    await send_next_session_info(app, "Morning Session", "7:00 AM (Tomorrow)")
                    last_next_date_session = next_key

        except Exception as e:
            print(f"Error: {e}")

        await asyncio.sleep(0.5)

async def send_ready_alert(app, session_name, markup):
    alert_msg = (
        f"🚨 🔥 <b>ATTENTION: {session_name} IS ABOUT TO START!</b> 🔥 🚨\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 <b>Get ready & prepare your account! / तैयार हो जाइए! / সবাই রেডি থাকুন!</b>\n\n"
        f"🇬🇧 <b>ENGLISH:</b> Maintain balance & follow safe 10-Level Martingale.\n"
        f"🇮🇳 <b>हिंदी (HINDI):</b> सुरक्षित 10-लेवल मार्टिंगेल फॉलो करें।\n"
        f"🇧🇩 <b>বাংলা (BANGLA):</b> নিরাপদ ১০ লেভেল মার্টিনগেল ফলো করুন।\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    await app.bot.send_message(chat_id=CHANNEL_ID, text=alert_msg, parse_mode=ParseMode.HTML, reply_markup=markup)

async def send_referral_promo(app, markup):
    promo_msg = (
        f"🌟 🔥 <b>MAXIMIZE YOUR EARNINGS WITH BDG WIN!</b> 🔥 🌟\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>Build your team and generate passive daily income! Earn lifetime commissions and referral bonuses. Share your link now!</i>"
    )
    await app.bot.send_message(chat_id=CHANNEL_ID, text=promo_msg, parse_mode=ParseMode.HTML, reply_markup=markup)

async def send_next_session_info(app, next_session_name, next_time_str):
    next_msg = (
        f"⏰ 🔔 <b>NEXT SESSION UPDATE</b> 🔔 ⏰\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 <b>Upcoming Session:</b> {next_session_name}\n"
        f"🕒 <b>Start Time:</b> {next_time_str} Sharp"
    )
    next_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 Play BDG Win 🏆", url="https://bdgwin.com")],
        [InlineKeyboardButton("📢 Join VIP Channel", url="https://t.me/bdgplayvipwin")]
    ])
    await app.bot.send_message(chat_id=CHANNEL_ID, text=next_msg, parse_mode=ParseMode.HTML, reply_markup=next_markup)

async def post_init(app):
    asyncio.create_task(send_auto_prediction(app))


# ==========================================
# 🏁 Main Function
# ==========================================
def main():
    threading.Thread(target=run_web, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    app.run_polling()

if __name__ == '__main__':
    main()
                
