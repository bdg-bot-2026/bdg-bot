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
# 🌐 Flask Web Server (Render বা ক্লাউডে লাইভ রাখার জন্য)
# ==========================================
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot status: ONLINE (1-Min Professional Signal Mode with Pre-Alerts & Summaries)"

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
    """প্যাটার্ন থেকে পরবর্তী অরিজিনাল প্রেডিকশন ফেচ করে (রিভার্স ছাড়া)"""
    global current_pattern, pattern_index
    if not current_pattern or pattern_index >= len(current_pattern):
        current_pattern = high_tech_ai_trend_evaluator()
        pattern_index = 0
    
    raw_prediction = current_pattern[pattern_index]
    pattern_index += 1
    return raw_prediction

def get_current_1min_period():
    """১ মিনিটের গেম পিরিয়ড আইডি জেনারেট করে (WinGo 1 Min)"""
    now = get_ist_time()
    start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elapsed_seconds = int((now - start_time).total_seconds())
    interval_index = (elapsed_seconds // 60) + 1
    date_str = now.strftime('%Y%m%d')
    return f"{date_str}10001{interval_index:04d}"


# ==========================================
# 🚀 Telegram Automation Functions (Scheduled Time)
# ==========================================
async def send_auto_prediction(app):
    """নির্দিষ্ট সময়ে সিগন্যাল, সেশনের ৫ মিনিট আগে অ্যালার্ট এবং সেশন শেষে রেফারেল মেসেজ পাঠাবে"""
    last_sent_period = ""
    last_alert_date_session = ""    # সেশন শুরুর আগের অ্যালার্ট ট্র্যাক করার জন্য
    last_summary_date_session = ""  # সেশন শেষের প্রমোশন ট্র্যাক করার জন্য
    
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

            # ১. সেশন শুরুর আগের ৫ মিনিটের অ্যালার্ট (সকাল ৬:৫৫, দুপুর ১:৫৫, রাত ৭:৫৫)
            alert_markup = [
                [InlineKeyboardButton("🚀 Ready & Deposit", url="https://bdgwin.com")],
                [InlineKeyboardButton("📢 Channel Link", url="https://t.me/bdgplayvipwin")]
            ]
            alert_reply_markup = InlineKeyboardMarkup(alert_markup)

            if hour == 6 and 55 <= minute < 60:
                alert_key = f"{current_date_str}_MORNING_ALERT"
                if last_alert_date_session != alert_key:
                    await send_ready_alert(app, "Morning Session (7:00 AM)", alert_reply_markup)
                    last_alert_date_session = alert_key

            elif hour == 13 and 55 <= minute < 60:
                alert_key = f"{current_date_str}_AFTERNOON_ALERT"
                if last_alert_date_session != alert_key:
                    await send_ready_alert(app, "Afternoon Session (2:00 PM)", alert_reply_markup)
                    last_alert_date_session = alert_key

            elif hour == 19 and 55 <= minute < 60:
                alert_key = f"{current_date_str}_NIGHT_ALERT"
                if last_alert_date_session != alert_key:
                    await send_ready_alert(app, "Night Session (8:00 PM)", alert_reply_markup)
                    last_alert_date_session = alert_key


            # ২. মূল সিগন্যাল পাঠানোর অংশ (৭:০০-৭:৩৫, ১৪:০০-১৪:৩৫, ২০:০০-২০:৩৫)
            is_morning = (hour == 7 and 0 <= minute < 35)
            is_afternoon = (hour == 14 and 0 <= minute < 35)
            is_night = (hour == 20 and 0 <= minute < 35)

            if is_morning or is_afternoon or is_night:
                period_num = get_current_1min_period()
                if period_num != last_sent_period:
                    pred = high_tech_ai_trend_evaluator() if not current_pattern else get_high_tech_ai_prediction()
                    
                    if pred == "SMALL":
                        pred_display = "🔵 <b>[ SMALL ]</b> 🔵"
                    else:
                        pred_display = "🟢 <b>[ BIG ]</b> 🟢"
                    
                    msg = (
                        f"💎 <b>⚡ BDG WIN VIP 1-MIN SIGNAL ⚡</b> 💎\n"
                        f"═════════════════════\n"
                        f"📌 <b>GAME:</b> <code>Win Go 1 Min</code>\n"
                        f"🆔 <b>PERIOD:</b> <code>{period_num}</code>\n"
                        f"🎯 <b>TARGET:</b> {pred_display}\n"
                        f"═════════════════════\n"
                        f"⚠️ <b>RULE:</b> <i>Safe 1-10 Level Martingale</i>\n"
                        f"🚀 <i>Play Smart, Earn Big!</i>"
                    )
                    
                    await app.bot.send_message(
                        chat_id=CHANNEL_ID,
                        text=msg,
                        parse_mode=ParseMode.HTML,
                        reply_markup=reply_markup
                    )
                    last_sent_period = period_num


            # ৩. সেশন শেষ হওয়ার পর রেফারেল প্রমোশন মেসেজ (৭:৩৫, ২:৩৫, ৮:৩৫ এর পরের ৫ মিনিটে)
            promo_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Join & Start Refer", url="https://bdgwin.com")],
                [InlineKeyboardButton("💎 Contact For Support", url="https://t.me/bdgplayvipwin")]
            ])

            if hour == 7 and 35 <= minute < 40:
                session_key = f"{current_date_str}_MORNING_SUMMARY"
                if last_summary_date_session != session_key:
                    await send_referral_promo(app, promo_markup)
                    last_summary_date_session = session_key

            elif hour == 14 and 35 <= minute < 40:
                session_key = f"{current_date_str}_AFTERNOON_SUMMARY"
                if last_summary_date_session != session_key:
                    await send_referral_promo(app, promo_markup)
                    last_summary_date_session = session_key

            elif hour == 20 and 35 <= minute < 40:
                session_key = f"{current_date_str}_NIGHT_SUMMARY"
                if last_summary_date_session != session_key:
                    await send_referral_promo(app, promo_markup)
                    last_summary_date_session = session_key

        except Exception as e:
            print(f"Error: {e}")

        await asyncio.sleep(1)

async def send_ready_alert(app, session_name, markup):
    """সেশন শুরু হওয়ার ৫ মিনিট আগে রুলস ও ব্যালেন্স মেইনটেইন করার এলার্ট মেসেজ পাঠাবে"""
    alert_msg = (
        f"🚨 🔥 <b>ATTENTION: {session_name} IS ABOUT TO START!</b> 🔥 🚨\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 <b>Are you ready? Get your game account prepared right now!</b>\n\n"
        f"💰 <b>IMPORTANT GUIDELINES & RULES:</b>\n"
        f"• <b>Maintain Balance:</b> Keep sufficient funds to safely follow up to <b>10-Level Martingale</b>. 📈\n"
        f"• <b>Strictly No Illegal Bets:</b> Do NOT place opposite bets (Big & Small together) at the same time! ❌\n"
        f"• <b>No Red/Green Mix:</b> Never place conflicting bets on Red and Green simultaneously. ⛔\n"
        f"• <b>Single Device Rule:</b> Do NOT log in with two accounts on the same phone. 📱\n"
        f"• <b>Network Warning:</b> Avoid public Wi-Fi sharing to prevent IP conflicts or account bans. 🌐\n\n"
        f"⚠️ <i>Follow company rules strictly to protect your account and ensure smooth profits. Let's make huge gains today!</i>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    await app.bot.send_message(
        chat_id=CHANNEL_ID,
        text=alert_msg,
        parse_mode=ParseMode.HTML,
        reply_markup=markup
    )

async def send_referral_promo(app, markup):
    """সেশন শেষ হওয়ার পর রেফারেল ও কমিশন প্রমোশন মেসেজ পাঠাবে"""
    promo_msg = (
        f"🌟 🔥 <b>MAXIMIZE YOUR EARNINGS WITH BDG WIN!</b> 🔥 🌟\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 <i>Don't just play alone—build your powerful team and generate passive income every single day!</i>\n\n"
        f"💸 <b>WHY BUILD A TEAM?</b>\n"
        f"• <b>Daily Commission:</b> Earn lifetime commission from every single trade your team makes! 📈\n"
        f"• <b>Daily Salary:</b> Unlock fixed daily salary rewards based on your active team performance! 💰\n"
        f"• <b>Instant Referral Bonus:</b> Invite your friends, grow your network, and watch your wallet grow automatically! 🚀\n\n"
        f"🎯 <i>The bigger your team, the bigger your daily profit! Start sharing your referral link right now and secure your financial freedom.</i>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    await app.bot.send_message(
        chat_id=CHANNEL_ID,
        text=promo_msg,
        parse_mode=ParseMode.HTML,
        reply_markup=markup
    )

async def post_init(app):
    asyncio.create_task(send_auto_prediction(app))


# ==========================================
# 🏁 Main Function
# ==========================================
main_called = False

def main():
    global main_called
    if main_called:
        return
    main_called = True
    
    # ব্যাকগ্রাউন্ডে Flask সার্ভার রান করার জন্য Thread শুরু করা হলো
    threading.Thread(target=run_web, daemon=True).start()
    
    # টেলিগ্রাম বট অ্যাপ ইনিশিয়ালাইজ এবং রান করা
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    app.run_polling()

if __name__ == '__main__':
    main()
            
