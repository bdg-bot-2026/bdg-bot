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
# 🌐 Flask Web Server
# ==========================================
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot status: ONLINE (Period Fixed & Continuous Testing Mode)"

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
# ⏰ Time & Live Game Period Synchronization Function (Fixed)
# ==========================================
def get_ist_time():
    try:
        ist = pytz.timezone('Asia/Kolkata')
        return datetime.now(ist)
    except Exception:
        return datetime.utcnow() + timedelta(hours=5, minutes=30)

def get_current_1min_period():
    now = get_ist_time()
    date_str = now.strftime("%Y%m%d")
    
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    total_minutes = int((now - midnight).total_seconds() // 60)
    
    # সঠিক BDG Win 1-min পিরিয়ড ফরম্যাট (YYYYMMDD1000 + ৪ ডিজিট সিরিয়াল)
    period_no = 1000 + total_minutes + 1
    return f"{date_str}1000{period_no}"


# ==========================================
# 📊 Advanced AI Trend Evaluator (10 Strategies)
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
        dragon_len = random.randint(5, 7)
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
    global current_pattern, pattern_index
    if not current_pattern or pattern_index >= len(current_pattern):
        current_pattern = high_tech_ai_trend_evaluator()
        pattern_index = 0
    
    raw_prediction = current_pattern[pattern_index]
    pattern_index += 1
    return raw_prediction


# ==========================================
# 🎨 Smart Color Evaluator Logic (Only Green & Red)
# ==========================================
def get_smart_trend_color(pred_text):
    if pred_text == "BIG":
        return random.choice(["GREEN 🟢", "GREEN 🟢", "RED 🔴"])
    else:
        return random.choice(["RED 🔴", "RED 🔴", "GREEN 🟢"])


# ==========================================
# 📢 Extra Supporting Message Functions
# ==========================================
async def send_ready_alert(bot, session_name, markup):
    alert_msg = (
        f"<b>BDG VIP PREDICTION 1 Min:</b>\n"
        f"🚨 🔥 <b>ATTENTION: {session_name} IS ABOUT TO START!</b> 🔥 🚨\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 <b>Get ready & prepare your account! / तैयार हो जाइए! / সবাই রেডি থাকুন!</b>"
    )
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=alert_msg, parse_mode=ParseMode.HTML, reply_markup=markup)
    except Exception as e:
        print(f"Alert Error: {e}")

async def send_referral_promo(bot, markup):
    promo_msg = (
        f"💎 ✨ <b>MAXIMIZE YOUR EARNINGS WITH BDG WIN!</b> ✨ 💎\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Build your powerful team and generate passive daily income!"
    )
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=promo_msg, parse_mode=ParseMode.HTML, reply_markup=markup)
    except Exception as e:
        print(f"Promo Error: {e}")


# ==========================================
# 🚀 Telegram Automation Main Loop
# ==========================================
async def main_bot_loop():
    bot = Bot(token=TOKEN)
    last_sent_period = ""
    last_alert_date_session = ""    
    last_promo_date_session = ""    
    
    keyboard = [
        [InlineKeyboardButton("🎮 Play BDG Win 🏆", url="https://bdgwin.com")],
        [InlineKeyboardButton("📊 Join VIP Channel", url="https://t.me/bdgplayvipwin")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    print("BDG Win Stable Direct Bot Loop started successfully...")

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

            if hour == 6 and 55 <= minute < 60:
                alert_key = f"{current_date_str}_MORNING_ALERT"
                if last_alert_date_session != alert_key:
                    await send_ready_alert(bot, "Morning Session (7:00 AM)", alert_markup)
                    last_alert_date_session = alert_key

            # কন্টিনিউয়াস টেস্টিং মোড চালু রাখা হয়েছে
            is_active_testing_mode = True

            if is_active_testing_mode:
                period_num = get_current_1min_period()
                if period_num != last_sent_period:
                    pred = get_high_tech_ai_prediction()
                    pred_text = "SMALL" if pred == "SMALL" else "BIG"
                    color_text = get_smart_trend_color(pred_text)
                    
                    msg = (
                        f"💎 <b>BDG WIN ULTRA AI VIP PREDICTION</b> 💎\n"
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
                        parse_mode=ParseMode.HTML,
                        reply_markup=reply_markup
                    )
                    
                    print(f"Signal sent successfully for period: {period_num}")
                    last_sent_period = period_num

            promo_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Join & Start Refer", url="https://bdgwin.com")],
                [InlineKeyboardButton("💎 Contact For Support", url="https://t.me/bdgplayvipwin")]
            ])

            if (hour == 7 and minute == 36) or (hour == 14 and minute == 36) or (hour == 20 and minute == 36):
                promo_key = f"{current_date_str}_{hour}_PROMO"
                if last_promo_date_session != promo_key:
                    await send_referral_promo(bot, promo_promo_markup if 'promo_promo_markup' in locals() else promo_markup)
                    last_promo_date_session = promo_key

        except Exception as e:
            print(f"Loop Error: {e}")

        await asyncio.sleep(2)


# ==========================================
# ⚙️ Main Application Launcher
# ==========================================
if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    asyncio.run(main_bot_loop())
