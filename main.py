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
    return "Bot status: ONLINE (Clean Custom Signal Mode)"

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
    """প্যাটার্ন থেকে পরবর্তী অরিজিনাল ফেচ করে"""
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
    """নির্দিষ্ট সময়ে সিগন্যাল, সেশনের আগের অ্যালার্ট এবং সেশন শেষের ১ মিনিট পরপর দুটি আলাদা মেসেজ পাঠাবে"""
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

            # ১. সেশন শুরুর আগের ৫ মিনিটের অ্যালার্ট (৬:৫৫, ১৩:৫৫, ১৯:৫৫)
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


            # ২. মূল সিগন্যাল পাঠানোর অংশ (৭:০০-৭:৩৫, ১৪:০০-১৪:৩৫, ২০:০০-২০:৩৫)
            is_morning = (hour == 7 and 0 <= minute < 35)
            is_afternoon = (hour == 14 and 0 <= minute < 35)
            is_night = (hour == 20 and 0 <= minute < 35)

            if is_morning or is_afternoon or is_night:
                period_num = get_current_1min_period()
                if period_num != last_sent_period:
                    pred = high_tech_ai_trend_evaluator() if not current_pattern else get_high_tech_ai_prediction()
                    
                    # প্রেডিকশন অনুযায়ী সাইজ এবং কালার সেটআপ
                    if pred == "SMALL":
                        pred_text = "SMALL"
                        color_text = "RED 🔴"
                    else:
                        pred_text = "BIG"
                        color_text = "GREEN 🟢"
                    
                    msg = (
                        f"❤️ <b>BDG WIN ULTRA AI VIP</b> ❤️️\n\n"
                        f"🔹 <b>PERIOD:</b> <code>{period_num}</code>\n"
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

            # ৩. সেশন শেষের ঠিক ১ মিনিট পর (৭:৩৬, ২:৩৬, ৮:৩৬) -> ৩ ভাষার প্রমোশন মেসেজ
            if (hour == 7 and minute == 36) or (hour == 14 and minute == 36) or (hour == 20 and minute == 36):
                promo_key = f"{current_date_str}_{hour}_PROMO"
                if last_promo_date_session != promo_key:
                    await send_referral_promo(app, promo_markup)
                    last_promo_date_session = promo_key

            # ৪. সেশন শেষের ঠিক ২ মিনিট পর (৭:৩৭, ২:৩৭, ৮:৩৭) -> পরবর্তী সেশনের টাইমিংয়ের মেসেজ
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

        await asyncio.sleep(1)

async def send_ready_alert(app, session_name, markup):
    """সেশন শুরু হওয়ার ৫ মিনিট আগে তিন ভাষায় অ্যালার্ট পাঠাবে"""
    alert_msg = (
        f"🚨 🔥 <b>ATTENTION: {session_name} IS ABOUT TO START!</b> 🔥 🚨\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 <b>Get ready & prepare your account! / तैयार हो जाइए! / সবাই রেডি থাকুন!</b>\n\n"
        
        f"🇬🇧 <b>ENGLISH:</b>\n"
        f"• <b>Maintain Balance:</b> Follow safe <b>10-Level Martingale</b>.\n"
        f"• <b>No Illegal Bets:</b> Do NOT place Big & Small together.\n"
        f"• <b>No Red/Green Mix:</b> Do not bet on Red & Green simultaneously.\n"
        f"• <b>Single Device:</b> Do not use 2 accounts on 1 phone.\n"
        f"• <b>Network:</b> Avoid public Wi-Fi.\n\n"

        f"🇮🇳 <b>हिंदी (HINDI):</b>\n"
        f"• <b>बैलेंस बनाए रखें:</b> सुरक्षित <b>10-लेवल मार्टिंगेल</b> फॉलो करें।\n"
        f"• <b>कोई अवैध शर्त नहीं:</b> Big और Small एकसाथ न लगाएं।\n"
        f"• <b>रेड/ग्रीन मिक्स न करें:</b> एकसाथ दोनों पर बेट न लगाएं।\n"
        f"• <b>एक डिवाइस नियम:</b> एक फोन में दो आईडी लॉगिन न करें।\n"
        f"• <b>नेटवर्क चेतावनी:</b> पब्लिक वाई-फाई का उपयोग न करें।\n\n"

        f"🇧🇩 <b>বাংলা (BANGLA):</b>\n"
        f"• <b>ব্যালেন্স মেইনটেইন করুন:</b> নিরাপদ <b>১০ লেভেল মার্টিনগেল</b> ফলো করুন।\n"
        f"• <b>ইল্লিগাল বেট নিষেধ:</b> বিগ এবং স্মল একসঙ্গে কেউ করবেন না।\n"
        f"• <b>রেড-গ্রীন একসঙ্গে নয়:</b> রেড ও গ্রীনে একসাথে বেট লাগাবেন না।\n"
        f"• <b>এক ফোনে এক আইডি:</b> একটা ফোনে দুটো আইডি লগইন করবেন না।\n"
        f"• <b>ওয়াইফাই সতর্কবার্তা:</b> ওয়াইফাই প্লে বা পাবলিক নেটওয়ার্ক এড়িয়ে চলুন।\n\n"
        f"⚠️ <i>Follow company rules strictly to protect your account! / कंपनी के नियमों का पालन करें! / কোম্পানির রুলস ফলো করুন!</i>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    await app.bot.send_message(
        chat_id=CHANNEL_ID,
        text=alert_msg,
        parse_mode=ParseMode.HTML,
        reply_markup=markup
    )

async def send_referral_promo(app, markup):
    """সেশন শেষের ১ মিনিট পর বাংলা, হিন্দি এবং ইংরেজিতে রেফারেল ও টিম তৈরির মেসেজ পাঠাবে"""
    promo_msg = (
        f"🌟 🔥 <b>MAXIMIZE YOUR EARNINGS WITH BDG WIN!</b> 🔥 🌟\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🇬🇧 <b>ENGLISH:</b>\n"
        f"<i>Build your powerful team and generate passive daily income! Earn lifetime commissions, daily salaries, and referral bonuses. Share your link now!</i>\n\n"
        f"🇮🇳 <b>हिंदी (HINDI):</b>\n"
        f"<i>अपनी खुद की मजबूत टीम बनाएं और रोजाना पैसिव इनकम कमाएं! लाइफटाइम कमीशन, डेली सैलरी और रेफरल बोनस पाएं। अभी अपना लिंक शेयर करें!</i>\n\n"
        f"🇧🇩 <b>বাংলা (BANGLA):</b>\n"
        f"<i>একটি শক্তিশালী টিম তৈরি করুন এবং প্রতিদিন প্যাসিভ ইনকাম করুন! লাইফটাইম কমিশন, ডেইলি স্যালারি এবং রেফারেল বোনাস উপভোগ করুন। এখনই শেয়ার করুন!</i>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    await app.bot.send_message(
        chat_id=CHANNEL_ID,
        text=promo_msg,
        parse_mode=ParseMode.HTML,
        reply_markup=markup
    )

async def send_next_session_info(app, next_session_name, next_time_str):
    """সেশন শেষের ২ মিনিট পর পরবর্তী সেশনের সময় জানিয়ে মেসেজ পাঠাবে"""
    next_msg = (
        f"⏰ 🔔 <b>NEXT SESSION UPDATE</b> 🔔 ⏰\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 <b>Upcoming Session:</b> <code>{next_session_name}</code>\n"
        f"🕒 <b>Start Time:</b> <code>{next_time_str} Sharp</code>\n\n"
        f"💡 <i>Prepare your funds, recharge your account, and stay active on the channel before time! Don't miss out on high profits.</i> 🚀\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    next_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 Play BDG Win 🏆", url="https://bdgwin.com")],
        [InlineKeyboardButton("📢 Join VIP Channel", url="https://t.me/bdgplayvipwin")]
    ])
    await app.bot.send_message(
        chat_id=CHANNEL_ID,
        text=next_msg,
        parse_mode=ParseMode.HTML,
        reply_markup=next_markup
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
                    
