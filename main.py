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
    return "Bot status: ONLINE (Advanced AI Trend & Lifetime Dynamic Period Active)"

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
# ⏰ Time & Lifetime Period Synchronization Function
# ==========================================
def get_ist_time():
    try:
        ist = pytz.timezone('Asia/Kolkata')
        return datetime.now(ist)
    except Exception:
        return datetime.utcnow() + timedelta(hours=5, minutes=30)

def get_current_1min_period():
    now = get_ist_time()
    # আজকের তারিখটি ডায়নামিকভাবে ফরম্যাট করা (যেমন: 20261007)
    date_str = now.strftime('%Y%m%d')
    
    # আজকের দিনের শুরু (রাত ১২:০০ টা) থেকে বর্তমান সময় পর্যন্ত মোট কত মিনিট হয়েছে তার নিখুঁত হিসাব
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    total_minutes = int((now - start_of_day).total_seconds() // 60)
    
    # গেমের নিয়ম অনুযায়ী প্রতিদিনের পিরিয়ড কাউন্ট যা লাইফটাইম স্বয়ংক্রিয়ভাবে আপডেট হবে
    game_period_count = 10001 + total_minutes
    
    return f"{date_str}1000{game_period_count}"


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
async def send_ready_alert(app, session_name, markup):
    alert_msg = (
        f"<b>BDG VIP PREDICTION 1 Min:</b>\n"
        f"🚨 🔥 <b>ATTENTION: {session_name} IS ABOUT TO START!</b> 🔥 🚨\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 <b>Get ready & prepare your account! / तैयार हो जाइए! / সবাই রেডি থাকুন!</b>\n\n"
        f"🇬🇧 <b>ENGLISH:</b>\n"
        f"💎 <b>Maintain Balance:</b> Follow safe 10-Level Martingale.\n"
        f"🛡️ <b>3x Turnover Rule:</b> Complete 3x betting of your deposit amount before withdrawal.\n"
        f"🚫 <b>No Illegal Bets:</b> Do NOT place Big & Small together.\n"
        f"⚠️ <b>No Red/Green Mix:</b> Do not bet on Red & Green simultaneously.\n"
        f"📱 <b>Single Device:</b> Do not use 2 accounts on 1 phone.\n"
        f"📶 <b>Network:</b> Avoid public Wi-Fi.\n\n"
        f"🇮🇳 <b>हिंदी (HINDI):</b>\n"
        f"💎 <b>बैलेंस बनाए रखें:</b> सुरक्षित 10-लेवल मार्टिंगेल फॉलो करें।\n"
        f"🛡️ <b>3x टर्नओवर नियम:</b> विथड्रॉल से पहले 3x बेटिंग पूरी करें।\n"
        f"🚫 <b>कोई अवैध शर्त नहीं:</b> Big और Small एकसाथ न लगाएं।\n"
        f"⚠️ <b>रेड/ग्रीन मिक्स न करें:</b> एकसाथ दोनों पर बेट न लगाएं।\n"
        f"📱 <b>एक डिवाइस नियम:</b> एक फोन में दो आईडी लॉगिन न करें।\n"
        f"📶 <b>नेटवर्क चेतावनी:</b> पब्लिक वाई-फाई का उपयोग न करें।\n\n"
        f"🇧🇩 <b>বাংলা (BANGLA):</b>\n"
        f"💎 <b>ব্যালেন্স মেইনটেইন করুন:</b> নিরাপদ ১০ লেভেল মার্টিনগেল ফলো করুন।\n"
        f"🛡️ <b>৩x টার্নওভার রুল:</b> ডিপোজিটের পর ৩x বেটিং কমপ্লিট করুন।\n"
        f"🚫 <b>ইল্লিগাল বেট নিষেধ:</b> বিগ এবং স্মল একসঙ্গে কেউ করবেন না।\n"
        f"⚠️ <b>রেড-গ্রীন একসঙ্গে নয়: রেড ও গ্রীনে একসাথে বেট লাগাবেন না।</b>\n"
        f"📱 <b>এক ফোনে এক আইডি:</b> একটা ফোনে দুটো আইডি লগইন করবেন না।\n"
        f"📶 <b>ওয়াইফাই সতর্কবার্তা:</b> ওয়াইফাই প্লে বা পাবলিক নেটওয়ার্ক এড়িয়ে চলুন।"
    )
    try:
        await app.bot.send_message(chat_id=CHANNEL_ID, text=alert_msg, parse_mode=ParseMode.HTML, reply_markup=markup)
    except Exception as e:
        print(f"Alert Error: {e}")

async def send_referral_promo(app, markup):
    promo_msg = (
        f"💎 ✨ <b>MAXIMIZE YOUR EARNINGS WITH BDG WIN!</b> ✨ 💎\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🇬🇧 <b>ENGLISH:</b>\n"
        f"Build your powerful team and generate passive daily income! Earn lifetime commissions, daily salaries, and referral bonuses. Share your link now!\n\n"
        f"🇮🇳 <b>हिंदी (HINDI):</b>\n"
        f"अपनी खुद की मजबूत टीम बनाएं और रोजाना पैसिव इनकम कमाएं! लाइफटाइम कमीशन, डेली सैलरी और रेफरल बोनस पाएं। अभी अपना लिंक शेयर करें!\n\n"
        f"🇧🇩 <b>বাংলা (BANGLA):</b>\n"
        f"একটি শক্তিশালী টিম তৈরি করুন এবং প্রতিদিন প্যাসিভ ইনকাম করুন! লাইফটাইম কমিশন, ডেইলি স্যালারি এবং রেফারেল বোনাস উপভোগ করুন। এখনই শেয়ার করুন!\n"
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
        f"🇬🇧 🔹 <b>ENGLISH:</b>\n"
        f"Next VIP Session: {next_session_name} at {time_str}. Get ready for the next profit wave!\n\n"
        f"🇮🇳 🔸 <b>हिंदी (HINDI):</b>\n"
        f"अगला वीआईपी सेशन: {time_str} पर {next_session_name} शुरू होगा। अगले प्रॉफिट वेव के लिए तैयार रहें!\n\n"
        f"🇧🇩 🔹 <b>বাংলা (BANGLA):</b>\n"
        f"পরবর্তী ভিআইপি সেশন: {time_str} এ {next_session_name} শুরু হবে। পরবর্তী প্রফিটের জন্য প্রস্তুত থাকুন!\n"
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

            # ১. সেশন শুরুর ৫ মিনিটের অ্যালার্ট মেসেজ (৬:৫৫, ১:৫৫, ৭:৫৫)
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


            # ২. মূল সিগন্যাল পাঠানোর অংশ (৭:০০-৭:৩৫, ২:০০-২:৩৫, ৮:০০-৮:৩৫)
            is_morning_session = (hour == 7 and minute <= 35)
            is_afternoon_session = (hour == 14 and minute <= 35)
            is_night_session = (hour == 20 and minute <= 35)

            if is_morning_session or is_afternoon_session or is_night_session:
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

            # ৪. সেশন শেষ হওয়ার পরের প্রমোশন মেসেজ (৭:৩৬, ২:৩৬, ৮:৩৬)
            if (hour == 7 and minute == 36) or (hour == 14 and minute == 36) or (hour == 20 and minute == 36):
                promo_key = f"{current_date_str}_{hour}_PROMO"
                if last_promo_date_session != promo_key:
                    await send_referral_promo(app, promo_markup)
                    last_promo_date_session = promo_key

            # ৫. পরবর্তী সেশনের আপডেট মেসেজ (৭:৩৭, ২:৩৭, ৮:৩৭)
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


# ==========================================
# ⚙️ Main Application Launcher
# ==========================================
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    # ব্যাকগ্রাউন্ডে ফ্লাস্ক সার্ভার রান করার জন্য
    threading.Thread(target=run_web, daemon=True).start()
    
    print("BDG Win Ultra AI Bot (Lifetime Dynamic Period Active) is running...")
    
    # অটো সিগন্যাল ও অ্যালার্ট লুপ স্টার্ট করা
    await send_auto_prediction(app)

if __name__ == "__main__":
    asyncio.run(main())
        
