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
    return "Bot status: ONLINE (Advanced AI Dynamic Random Trend & Live Matched Period Active)"

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
# ⏰ Time & Live Game Period Synchronization Function
# ==========================================
def get_ist_time():
    try:
        ist = pytz.timezone('Asia/Kolkata')
        return datetime.now(ist)
    except Exception:
        return datetime.utcnow() + timedelta(hours=5, minutes=30)

def get_current_1min_period():
    now = get_ist_time()
    # স্ক্রিনশট এবং লাইভ সময়ের হিসাব অনুযায়ী সিঙ্ক করা বেস টাইম ও পিরিয়ড
    base_time = datetime(2026, 10, 7, 7, 14, 0, tzinfo=pytz.timezone('Asia/Kolkata'))
    base_period = 10104
    total_minutes = int((now - base_time).total_seconds() // 60)
    current_period_count = base_period + total_minutes
    date_prefix = now.strftime('%Y%m%d')
    return f"{date_prefix}1000{current_period_count}"


# ==========================================
# 📊 Advanced AI Fully Random Trend Evaluator (10 Strategies)
# ==========================================
def get_high_tech_ai_prediction():
    """
    আপনার কোডের সেই ১০টি আসল স্ট্র্যাটেজি এখানে রাখা হয়েছে। 
    তবে এখন এটি কোনো ফিক্সড সিরিয়ালে চলবে না। প্রতি মিনিটে ১০০% রেন্ডমলি 
    যেকোনো একটি স্ট্র্যাটেজি পিক করে তার ভেতর থেকে যেকোনো একটি মান দিয়ে দিবে, 
    যাতে ট্রেন্ড যেকোনো সময় সম্পূর্ণ অনির্দিষ্টভাবে বদলাতে থাকে।
    """
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
    
    # প্রতি মিনিটে সম্পূর্ণ রেন্ডমলি যেকোনো একটি স্ট্র্যাটেজি সিলেক্ট হবে
    selected_strategy = random.choices(strategies, weights=weights, k=1)[0]

    start = random.choice(["BIG", "SMALL"])
    opposite = "SMALL" if start == "BIG" else "BIG"
    
    # স্ট্র্যাটেজি অনুযায়ী রেন্ডম প্যাটার্ন বা তালিকা তৈরি করে তাৎক্ষণিকভাবে একটি রেন্ডম মান পিক করা
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

    # নির্বাচিত প্যাটার্ন থেকে রেন্ডমলি যেকোনো একটি রেজাল্ট আউটপুট হবে
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
# 📢 Extra Supporting Message Functions
# ==========================================
async def send_ready_alert(app, session_name, markup):
    alert_msg = (
        f"<b>BDG VIP PREDICTION 1 Min:</b>\n"
        f"🚨 🔥 <b>ATTENTION: {session_name} IS ABOUT TO START!</b> 🔥 🚨\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 <b>Get ready & prepare your account! / तैयार हो जाइए! / সবাই রেডি থাকুন!</b>\n\n"
        f"🇬🇧 <b>ENGLISH:</b>\n"
        f"💎 <b>Maintain Balance:</b> Follow safe 10-Level Martingale.\n"
        f"🛡️ <b>3x Turnover Rule:</b> Complete 3x betting before withdrawal.\n"
        f"🚫 <b>No Illegal Bets:</b> Do NOT place Big & Small together.\n\n"
        f"🇮🇳 <b>हिंदी (HINDI):</b>\n"
        f"💎 <b>बैलेंस बनाए रखें:</b> सुरक्षित 10-लेवल मार्टिंगेल फॉलो करें।\n\n"
        f"🇧🇩 <b>বাংলা (BANGLA):</b>\n"
        f"💎 <b>ব্যালেন্স মেইনটেইন করুন:</b> নিরাপদ ১০ লেভেল মার্টিনগেল ফলো করুন।"
    )
    try:
        await app.bot.send_message(chat_id=CHANNEL_ID, text=alert_msg, parse_mode=ParseMode.HTML, reply_markup=markup)
    except Exception as e:
        print(f"Alert Error: {e}")

async def send_referral_promo(app, markup):
    promo_msg = (
        f"💎 ✨ <b>MAXIMIZE YOUR EARNINGS WITH BDG WIN!</b> ✨ 💎\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🇬🇧 Build your powerful team and generate passive daily income!\n"
        f"🇮🇳 अपनी खुद की मजबूत टीम बनाएं और रोजाना पैसिव इनकम कमाएं!\n"
        f"🇧🇩 একটি শক্তিশালী টিম তৈরি করুন এবং প্রতিদিন প্যাসিভ ইনকাম করুন!\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    try:
        await app.bot.send_message(chat_id=CHANNEL_ID, text=promo_msg, parse_mode=ParseMode.HTML, reply_markup=markup)
    except Exception as e:
        print(f"Promo Error: {e}")

async def send_next_session_info(app, next_session_name, time_str):
    next_msg = (
        f"💎 ⏰ <b>NEXT SESSION INFO / अगली सेशन की जानकारी / পরবর্তী সেশনের তথ্য</b> ⏰ 💎\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Next VIP Session: {next_session_name} at {time_str}. Get ready for the next profit wave!\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 Play BDG Win 🏆", url="https://bdgwin.com")],
        [InlineKeyboardButton("📊 Join VIP Channel", url="https://t.me/bdgplayvipwin")]
    ])
    try:
        await app.bot.send_message(chat_id=CHANNEL_ID, text=next_msg, parse_mode=ParseMode.HTML, reply_markup=markup)
    except Exception as e:
        print(f"Next Session Error: {e}")


# ==========================================
# 🚀 Telegram Automation Main Loop
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

            # ১. অ্যালার্ট মেসেজ (সেশন শুরুর ৫ মিনিট আগে)
            if hour == 6 and 55 <= minute < 60:
                if last_alert_date_session != f"{current_date_str}_MORNING_ALERT":
                    await send_ready_alert(app, "Morning Session (7:00 AM)", alert_markup)
                    last_alert_date_session = f"{current_date_str}_MORNING_ALERT"

            elif hour == 13 and 55 <= minute < 60:
                if last_alert_date_session != f"{current_date_str}_AFTERNOON_ALERT":
                    await send_ready_alert(app, "Afternoon Session (2:00 PM)", alert_markup)
                    last_alert_date_session = f"{current_date_str}_AFTERNOON_ALERT"

            elif hour == 19 and 55 <= minute < 60:
                if last_alert_date_session != f"{current_date_str}_NIGHT_ALERT":
                    await send_ready_alert(app, "Night Session (8:00 PM)", alert_markup)
                    last_alert_date_session = f"{current_date_str}_NIGHT_ALERT"

            # ২. মূল সিগন্যাল সেশন (৭:০০-৭:৩৫, ২:০০-২:৩৫, ৮:০০-৮:৩৫)
            is_morning_session = (hour == 7 and minute <= 35)
            is_afternoon_session = (hour == 14 and minute <= 35)
            is_night_session = (hour == 20 and minute <= 35)

            if is_morning_session or is_afternoon_session or is_night_session:
                period_num = get_current_1min_period()
                if period_num != last_sent_period:
                    pred_text = get_high_tech_ai_prediction()
                    color_text = get_smart_trend_color(pred_text)
                    
                    # হেডার এক লাইনে রাখার জন্য আগের মতো সুন্দর ও সংক্ষিপ্ত ফরম্যাট
                    msg = (
                        f"💎 <b>BDG ULTRA AI VIP PREDICTION</b> 💎\n"
                        f"💎 <b>BDG VIP PREDICTION 1 Min</b> 💎\n\n"
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

            # ৪. প্রমোশন মেসেজ
            if (hour == 7 and minute == 36) or (hour == 14 and minute == 36) or (hour == 20 and minute == 36):
                promo_key = f"{current_date_str}_{hour}_PROMO"
                if last_promo_date_session != promo_key:
                    await send_referral_promo(app, promo_markup)
                    last_promo_date_session = promo_key

            # ৫. পরবর্তী সেশন ইনফো
            if hour == 7 and minute == 37:
                if last_next_date_session != f"{current_date_str}_MORNING_NEXT":
                    await send_next_session_info(app, "Afternoon Session", "2:00 PM")
                    last_next_date_session = f"{current_date_str}_MORNING_NEXT"

            elif hour == 14 and minute == 37:
                if last_next_date_session != f"{current_date_str}_AFTERNOON_NEXT":
                    await send_next_session_info(app, "Night Session", "8:00 PM")
                    last_next_date_session = f"{current_date_str}_AFTERNOON_NEXT"

            elif hour == 20 and minute == 37:
                if last_next_date_session != f"{current_date_str}_NIGHT_NEXT":
                    await send_next_session_info(app, "Morning Session", "7:00 AM (Tomorrow)")
                    last_next_date_session = f"{current_date_str}_NIGHT_NEXT"

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
    
    print("BDG Win Advanced AI Dynamic Random Bot is running successfully...")
    
    await send_auto_prediction(app)

if __name__ == "__main__":
    asyncio.run(main())
    
