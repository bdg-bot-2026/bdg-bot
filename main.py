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
    return "Bot status: ONLINE (Real Period Sync & Red/Green Active)"

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
# ⏰ Real-time Period Synchronization Function
# ==========================================
def get_ist_time():
    try:
        ist = pytz.timezone('Asia/Kolkata')
        return datetime.now(ist)
    except Exception:
        return datetime.utcnow() + timedelta(hours=5, minutes=30)

def get_current_1min_period():
    """
    BDG Win রিয়েল পিরিয়ড ফরম্যাট: YYYYMMDD + 1000 + రోజుর মোট মিনিট সংখ্যা 
    যেমন স্ক্রিনশট অনুযায়ী: 20261006100011016
    """
    now = get_ist_time()
    date_str = now.strftime('%Y%m%d')
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    total_minutes = int((now - start_of_day).total_seconds() // 60)
    
    # গেেমর রিয়েল ফরম্যাট অনুযায়ী বেস এবং মিনিট যোগ করা হলো
    current_period = int(f"{date_str}100000000") + total_minutes
    return str(current_period)


# ==========================================
# 📊 Advanced AI Trend Evaluator (With Multi-Trends)
# ==========================================
def high_tech_ai_trend_evaluator():
    strategies_weights = {
        "DRAGON_TREND": 25,       
        "THREE_BY_THREE": 20,     
        "CROSS_WAVE": 20,         
        "TWO_BY_TWO_ZONE": 15,    
        "STABLE_ZIGZAG": 10,      
        "SMART_MIXED": 10         
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

            # ১. সেশন শুরুর আগের অ্যালার্ট মেসেজ
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


            # ২. মূল সিগন্যাল পাঠানোর অংশ (রিয়েল পیرিয়ড ও রেড/গ্রিন কালার সহ)
            is_morning_session = (hour == 7 and minute <= 35)
            is_afternoon_session = (hour == 14 and minute <= 35)
            is_night_session = (hour == 20 and minute <= 35)

            if is_morning_session or is_afternoon_session or is_night_session:
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
                        f"🎨 <b>SUGGESTED COLOR:</b> {color_text}\n"
                        f"───────────────────\n"
                        f"💡 <i>Rule: Safe 1-10 Level Martingale (Red & Green Trend Active)</i>"
                    )
                    
                    await app.bot.send_message(
                        chat_id=CHANNEL_ID,
                        text=msg,
                        parse_mode=ParseMode.HTML,
                        reply_markup=reply_markup
                    )
                    
                    # ৩. সিগন্যাল রাউন্ড শেষ হওয়ার পরের আপডেট
                    await asyncio.sleep(50)
                    await send_post_signal_message(app, period_num, pred_text, reply_markup)
                    
                    last_sent_period = period_num

            promo_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Join & Start Refer", url="https://bdgwin.com")],
                [InlineKeyboardButton("💎 Contact For Support", url="https://t.me/bdgplayvipwin")]
            ])

            # ৪. সেশন শেষ হওয়ার প্রমোশন মেসেজ
            if (hour == 7 and minute == 36) or (hour == 14 and minute == 36) or (hour == 20 and minute == 36):
                promo_key = f"{current_date_str}_{hour}_PROMO"
                if last_promo_date_session != promo_key:
                    await send_referral_promo(app, promo_markup)
                    last_promo_date_session = promo_key

            # ৫. পরবর্তী সেশনের আপডেট
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
        f"<b>BDG VIP PREDICTION 30s:</b>\n"
        f"🚨 🔥 <b>ATTENTION: {session_name} IS ABOUT TO START!</b> 🔥 🚨\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 <b>Get ready & prepare your account! / तैयार हो जाइए! / সবাই রেডি থাকুন!</b>\n\n"
        f"🇬🇧 <b>ENGLISH:</b>\n"
        f"• Maintain Balance: Follow safe 10-Level Martingale.\n"
        f"• 3x Turnover Rule: Complete 3x betting of your deposit amount before withdrawal.\n"
        f"• No Illegal Bets: Do NOT place Big & Small together.\n"
        f"• No Red/Green Mix: Do not bet on Red & Green simultaneously.\n"
        f"• Single Device: Do not use 2 accounts on 1 phone.\n"
        f"• Network: Avoid public Wi-Fi.\n\n"
        f"🇮🇳 <b>हिंदी (HINDI):</b>\n"
        f"• बैलेंस बनाए रखें: सुरक्षित 10-लेवल मार्टिंगेल फॉलो करें।\n"
        f"• 3x टर्नओवर नियम: विथड्रॉल से पहले डिपॉजिट का 3x बेटिंग पूरा करें।\n"
        f"• कोई अवैध शर्त नहीं: Big और Small एकसाथ न लगाएं।\n"
        f"• रेड/ग्रीन मिक्स न करें: एकसाथ दोनों पर बेट न लगाएं।\n"
        f"• एक डिवाइस नियम: एक फोन में दो आईडी लॉगिन न करें।\n"
        f"• नेटवर्क चेतावनी: पब्लिक वाई-फाई का उपयोग न करें।\n\n"
        f"🇧🇩 <b>বাংলা (BANGLA):</b>\n"
        f"• ব্যালেন্স মেইনটেইন করুন: নিরাপদ ১০ লেভেল মার্টিনগেল ফলো করুন।\n"
        f"• ৩x টার্নওভার রুল: ডিপোজিট করার পর অবশ্যই ৩x বেটিং কমপ্লিট করতে হবে।\n"
        f"• ইল্লিগাল বেট নিষেধ: বিগ এবং স্মল একসঙ্গে কেউ করবেন না।\n"
        f"• রেড-গ্রীন একসঙ্গে নয়: রেড ও গ্রীনে একসাথে বেট লাগাবেন না।\n"
        f"• এক ফোনে এক আইডি: একটা ফোনে দুটো আইডি লগইন করবেন না।\n"
        f"• ওয়াইফাই সতর্কবার্তা: ওয়াইফাই প্লে বা পাবলিক নেটওয়ার্ক এড়িয়ে চলুন।\n\n"
        f"⚠️ <b>Follow company rules strictly to protect your account!</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    await app.bot.send_message(chat_id=CHANNEL_ID, text=alert_msg, parse_mode=ParseMode.HTML, reply_markup=markup)

async def send_post_signal_message(app, period_num, predicted_val, markup):
    post_msg = (
        f"📢 <b>PERIOD RESULT UPDATE</b> 📢\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 <b>Period:</b> {period_num}\n"
        f"🎯 <b>Our Prediction was:</b> {predicted_val}\n"
        f"✅ <i>Check your game history. If Level 1 win, great! If not, proceed safely up to 10-Level Martingale.</i>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    await app.bot.send_message(chat_id=CHANNEL_ID, text=post_msg, parse_mode=ParseMode.HTML, reply_markup=markup)

async def send_referral_promo(app, markup):
    promo_msg = (
        f"🌟 🔥 <b>MAXIMIZE YOUR EARNINGS WITH BDG WIN!</b> 🔥 🌟\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 <b>বিনা ইনভেস্টে টিম বানিয়ে প্রতিদিন প্যাসিভ ইনকাম করুন!</b>\n"
        f"💎 <i>Build your team and generate passive daily income! Earn lifetime commissions and referral bonuses. Share your link now and start earning today!</i>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━"
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
                
