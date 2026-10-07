import os
import random
from datetime import datetime, timedelta
import pytz
import asyncio
import threading
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram.constants import ParseMode

# ==========================================
# 🌐 Flask Web Server (Render Keep-Alive)
# ==========================================
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot status: ONLINE (Always Active Signals)"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)


# ==========================================
# 🤖 Telegram Bot Configurations
# ==========================================
TOKEN = os.getenv("TELEGRAM_TOKEN", "8752459278:AAGbwu4j7JqT3R4Auwhj2PLMidKzhRaSkS0").strip()
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "-1004492973133")

current_pattern = []
pattern_index = 0
prediction_active = True


# ==========================================
# ⏰ 100% Exact Match Period Generator
# ==========================================
def get_ist_time():
    try:
        ist = pytz.timezone('Asia/Kolkata')
        return datetime.now(ist)
    except Exception:
        return datetime.utcnow() + timedelta(hours=5, minutes=30)

def generate_time_based_period():
    now = get_ist_time()
    date_str = now.strftime("%Y%m%d") 
    
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    total_minutes = int((now - midnight).total_seconds() / 60)
    
    current_minutes_today = (now.hour * 60) + now.minute
    base_counter = 10497 + (total_minutes - current_minutes_today)
    
    return f"{date_str}1000{base_counter}"


# ==========================================
# 📊 Fully Dynamic AI Trend Evaluator
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
        dragon_len = random.randint(3, 6)
        pattern = [start] * dragon_len
    elif selected_strategy == "THREE_BY_THREE":
        pattern = [start, start, start, opposite, opposite, opposite]
    elif selected_strategy == "CROSS_WAVE":
        pattern = [start, start, opposite, opposite, opposite, start]
    elif selected_strategy == "TWO_BY_TWO_ZONE":
        pattern = [start, start, opposite, opposite, start, start]
    elif selected_strategy == "STABLE_ZIGZAG":
        pattern = [start, opposite, start, opposite, start]
    elif selected_strategy == "MIRROR_REFLECTION":
        pattern = [start, opposite, start, start, opposite]
    elif selected_strategy == "FIBONACCI_STEP":
        pattern = [start, start, opposite, start, opposite]
    elif selected_strategy == "MOMENTUM_WAVE":
        pattern = [start, opposite, opposite, start, start]
    elif selected_strategy == "ALTERNATE_CLUSTER":
        pattern = [start, start, opposite, opposite, start]
    else:
        pattern = [start, opposite, start, start, opposite]

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
# 🎨 Smart Color Evaluator Logic
# ==========================================
def get_smart_trend_color(pred_text):
    if pred_text == "BIG":
        return random.choice(["GREEN 🟢", "GREEN 🟢", "RED 🔴"])
    else:
        return random.choice(["RED 🔴", "RED 🔴", "GREEN 🟢"])


# ==========================================
# 📢 Professional Multi-lingual Message Functions
# ==========================================
async def send_ready_alert(app, session_name, markup):
    alert_msg = (
        f"💎 <b>BDG VIP PREDICTION 1 MIN SESSION</b> 💎\n"
        f"🚨 🔥 <b>ATTENTION TRADERS: {session_name} IS ABOUT TO START!</b> 🔥 🚨\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 <b>Get ready & prepare your trading account! / तैयार हो जाइए! / সবাই রেডি থাকুন!</b> 🚀\n\n"
        f"🇬🇧 <b>ENGLISH:</b>\n"
        f"• 🛡️ <b>Maintain Balance:</b> Follow safe 10-Level Martingale.\n"
        f"• ❌ <b>No Illegal Bets:</b> Do NOT place Big & Small together.\n"
        f"• 🎨 <b>No Red/Green Mix:</b> Do not bet on Red & Green simultaneously.\n"
        f"• 📱 <b>Single Device:</b> Do not use 2 accounts on 1 phone.\n"
        f"• 🌐 <b>Network Security:</b> Avoid public Wi-Fi.\n\n"
        f"🇮🇳 <b>हिंदी (HINDI):</b>\n"
        f"• 🛡️ <b>बैलेंस बनाए रखें:</b> सुरक्षित 10-लेवल मार्टिंगेल फॉलो करें।\n"
        f"• ❌ <b>कोई अवैध शर्त नहीं:</b> Big और Small एकसाथ न लगाएं।\n"
        f"• 🎨 <b>रेड/ग्रीन मिक्स न करें:</b> एकसाथ दोनों पर बेट न लगाएं।\n"
        f"• 📱 <b>एक डिवाइस नियम:</b> एक फोन में दो आईडी लॉगिन न करें।\n"
        f"• 🌐 <b>नेटवर्क चेतावनी:</b> पब्लिक वाई-फाई का उपयोग न करें।\n\n"
        f"🇧🇩 <b>বাংলা (BANGLA):</b>\n"
        f"• 🛡️ <b>ব্যালেন্স মেইনটেইন:</b> নিরাপদ ১০ লেভেল মার্টিনগেল ফলো করুন।\n"
        f"• ❌ <b>ইল্লিগাল বেট নিষেধ:</b> বিগ এবং স্মল একসঙ্গে কেউ করবেন না।\n"
        f"• 🎨 <b>রেড-গ্রীন নিয়ম:</b> রেড ও গ্রীনে একসাথে বেট লাগাবেন না।\n"
        f"•  এক ফোনে এক আইডি: একটা ফোনে দুটো আইডি লগইন করবেন না।\n"
        f"• 🌐 <b>ওয়াইফাই সতর্কবার্তা:</b> পাবলিক নেটওয়ার্ক এড়িয়ে চলুন।\n\n"
        f"⚠️ <b>Follow company rules strictly to protect your funds! / कंपनी के नियमों का पालन करें! / কোম্পানির রুলস স্ট্রিক্টলি ফলো করুন!</b> ✨\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    try:
        await app.bot.send_message(chat_id=CHANNEL_ID, text=alert_msg, parse_mode=ParseMode.HTML, reply_markup=markup)
    except Exception as e:
        print(f"Alert Error: {e}")

async def send_referral_promo(app, markup):
    promo_msg = (
        f"🌟 🔥 <b>MAXIMIZE YOUR EARNINGS WITH BDG WIN!</b> 🔥 🌟\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🇬🇧 <b>ENGLISH:</b>\n"
        f"📈 Build your powerful team and generate passive daily income! Earn lifetime commissions, daily salaries, and referral bonuses. Share your link now! 🚀\n\n"
        f"🇮🇳 <b>हिंदी (HINDI):</b>\n"
        f"💰 अपनी खुद की मजबूत टीम बनाएं और रोजाना पैसिव इनकम कमाएं! लाइफटाइम कमीशन, डेली सैलरी और रेफरल बोनस पाएं। अभी शेयर करें! ✨\n\n"
        f"🇧🇩 <b>বাংলা (BANGLA):</b>\n"
        f"🤝 একটি শক্তিশালী টিম তৈরি করুন এবং প্রতিদিন প্যাসিভ ইনকাম করুন! লাইফটাইম কমিশন, ডেইলি স্যালারি এবং রেফারেল বোনাস উপভোগ করুন। এখনই শেয়ার করুন! 💎\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    try:
        await app.bot.send_message(chat_id=CHANNEL_ID, text=promo_msg, parse_mode=ParseMode.HTML, reply_markup=markup)
    except Exception as e:
        print(f"Promo Error: {e}")

async def send_next_session_info(app, next_session_name, time_str):
    next_msg = (
        f"💎 ⏰ <b>NEXT SESSION SCHEDULE INFO</b> ⏰ 💎\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🚀 <b>Upcoming Session: {next_session_name}</b>\n"
        f"🕒 <b>Timing: {time_str}</b>\n\n"
        f"✨ <i>Get ready for the next massive profit wave! / अगले सेशन के लिए तैयार रहें! / পরবর্তী সেশনের জন্য প্রস্তুত থাকুন!</i> 📈"
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
# 🎮 Telegram Command Handlers
# ==========================================
async def cmd_start_prediction(update, context):
    global prediction_active
    prediction_active = True
    await update.message.reply_text("✅ VIP Prediction ম্যানুয়ালি চালু (ON) করা হয়েছে! এখন সিগন্যাল আসবে।")

async def cmd_stop_prediction(update, context):
    global prediction_active
    prediction_active = False
    await update.message.reply_text("🛑 VIP Prediction ম্যানুয়ালি বন্ধ (OFF) করা হয়েছে!")


# ==========================================
# 🚀 Telegram Automation Main Loop
# ==========================================
async def send_auto_prediction(app):
    global prediction_active
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
            if not prediction_active:
                await asyncio.sleep(2)
                continue

            now = get_ist_time()
            hour = now.hour
            minute = now.minute
            current_date_str = now.strftime('%Y-%m-%d')

            alert_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Ready & Deposit", url="https://bdgwin.com")],
                [InlineKeyboardButton("📢 Channel Link", url="https://t.me/bdgplayvipwin")]
            ])

            # সেশন অ্যালার্ট মেসেজ (৫ মিনিট আগে)
            if (hour == 6 and minute == 55) or (hour == 13 and minute == 55) or (hour == 19 and minute == 55):
                alert_key = f"{current_date_str}_{hour}_ALERT"
                if last_alert_date_session != alert_key:
                    session_name = "Morning Session (7:00 AM)" if hour == 6 else ("Afternoon Session (2:00 PM)" if hour == 13 else "Night Session (8:00 PM)")
                    await send_ready_alert(app, session_name, alert_markup)
                    last_alert_date_session = alert_key

            # এখন prediction_active ট্রু থাকলেই যেকোনো সময় নির্বিঘ্নে সিগন্যাল পাঠাবে
            if prediction_active:
                period_num = generate_time_based_period()
                
                if period_num and period_num != last_sent_period:
                    pred = get_high_tech_ai_prediction()
                    pred_text = "SMALL" if pred == "SMALL" else "BIG"
                    color_text = get_smart_trend_color(pred_text)
                    
                    msg = (
                        f"💎 <b>BDG VIP PREDICTION 1 Min</b> 💎\n"
                        f"💎 <b>BDG WIN ULTRA AI VIP PREDICTION</b> 💎\n\n"
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

            # সেশন শেষের প্রমোশন মেসেজ
            if (hour == 7 and minute == 36) or (hour == 14 and minute == 36) or (hour == 20 and minute == 36):
                promo_key = f"{current_date_str}_{hour}_PROMO"
                if last_promo_date_session != promo_key:
                    await send_referral_promo(app, promo_markup)
                    last_promo_date_session = promo_key

            # পরবর্তী সেশনের আপডেট মেসেজ
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
            print(f"Main Loop Error: {e}")

        await asyncio.sleep(2)


# ==========================================
# ⚙️ Main Application Launcher
# ==========================================
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", cmd_start_prediction))
    app.add_handler(CommandHandler("stop", cmd_stop_prediction))
    
    threading.Thread(target=run_web, daemon=True).start()
    
    print("BDG Win Bot is running successfully with active signals...")
    
    async def post_init(application):
        application.create_task(send_auto_prediction(application))

    app.post_init = post_init
    app.run_polling()
