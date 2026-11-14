import os
import random
from datetime import datetime, timedelta
import pytz
import asyncio
import threading
from collections import deque
from flask import Flask
from telegram.ext import ApplicationBuilder
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode


# ==========================================
# 🌐 Flask Web Server (For Render / Keep-Alive)
# ==========================================
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot status: ONLINE (Raxi Win Indian Time Schedule & Ultra AI Active)"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)


# ==========================================
# 🤖 Telegram Bot Configurations
# ==========================================
TOKEN = "8937609482:AAFpxFnCk7ZI38QYnUNbUST2A6eZHnWuAHQ"
CHANNEL_ID = "@RexiWinAIPrediction"

current_pattern = []
pattern_index = 0

# 🧠 Stateful Trend Memory Buffer (Stores last 100 predictions for analysis)
prediction_history = deque(maxlen=100)


# ==========================================
# ⏰ Time & Live Game Period Synchronization (Indian Standard Time)
# ==========================================
def get_ist_time():
    try:
        ist_tz = pytz.timezone('Asia/Kolkata')
        return datetime.now(ist_tz)
    except Exception:
        return datetime.utcnow() + timedelta(hours=5, minutes=30)

def get_current_1min_period():
    now_utc = datetime.now(pytz.utc)
    date_str = now_utc.strftime("%Y%m%d")
    total_minutes_utc = (now_utc.hour * 60) + now_utc.minute
    period_count = 10000 + total_minutes_utc + 1
    return f"{date_str}1000{period_count}"


# ==========================================
# 📊 Advanced Stateful AI Trend Evaluator (100-Period Memory Analysis)
# ==========================================
def analytical_ai_trend_evaluator():
    recent_big_count = sum(1 for p in prediction_history if p == "BIG")
    recent_small_count = sum(1 for p in prediction_history if p == "SMALL")

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

    if len(prediction_history) >= 5:
        last_five = list(prediction_history)[-5:]
        if all(x == "BIG" for x in last_five) or all(x == "SMALL" for x in last_five):
            strategies_weights["DRAGON_TREND"] += 15

    strategies = list(strategies_weights.keys())
    weights = list(strategies_weights.values())
    selected_strategy = random.choices(strategies, weights=weights, k=1)[0]

    start = random.choice(["BIG", "SMALL"])
    if len(prediction_history) > 5:
        if recent_big_count > recent_small_count + 4:
            start = "SMALL"
        elif recent_small_count > recent_big_count + 4:
            start = "BIG"

    opposite = "SMALL" if start == "BIG" else "BIG"
    pattern = []
    
    if selected_strategy == "DRAGON_TREND":
        dragon_len = random.randint(4, 6)
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
    global current_pattern, pattern_index, prediction_history
    if not current_pattern or pattern_index >= len(current_pattern):
        current_pattern = analytical_ai_trend_evaluator()
        pattern_index = 0
    
    raw_prediction = current_pattern[pattern_index]
    pattern_index += 1
    
    prediction_history.append(raw_prediction)
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
# 📢 Extra Supporting Message Functions
# ==========================================
async def send_ready_alert(app, session_name, markup):
    alert_msg = (
        f"<b>RAXI WIN VIP PREDICTION 1 Min:</b>\n"
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
        f"🇮🇳 <b>বাংলা (BANGLA):</b>\n"
        f"💎 <b>ব্যালেন্স মেইনটেইন করুন:</b> নিরাপদ ১০ লেভেল মার্টিনগেল ফলো করুন।\n"
        f"🛡️ <b>৩x টার্নওভার রুল:</b> ডিপোজিটের পর ৩x বেটিং কমপ্লিট করুন।\n"
        f"🚫 <b>ইল্লিগাল বেট নিষেধ:</b> বিগ এবং স্মল একসঙ্গে কেউ করবেন না।\n"
        f"⚠️ <b>রেড-গ্রীন একসঙ্গে নয়: রেড ও গ্রীনে একসাথে বেট লাগাবেন না।</b>\n"
        f"📱 <b>এক ফোনে এক আইডি:</b> একটা ফোনে দুটো আইডি লগইন করবেন না।\n"
        f"📶 <b>ওয়াইফাই সতর্কবার্তা:</b> ওয়াইফাই প্লে বা পাবলিক নেটওয়ার্ক এড়িয়ে চলুন."
    )
    try:
        await app.bot.send_message(chat_id=CHANNEL_ID, text=alert_msg, parse_mode=ParseMode.HTML, reply_markup=markup)
    except Exception as e:
        print(f"Alert Error: {e}")


async def send_level_chart_alert(app, markup):
    chart_msg = (
        f"💎 <b>RAXI WIN VIP 10-LEVEL MARTINGALE</b> 💎\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🛡️ <b>OFFICIAL MONEY MANAGEMENT CHART</b>\n\n"
        f"🎯 <i>Strictly follow this Martingale plan to protect your capital & maximize daily profits!</i>\n\n"
        f"📊 <b>LEVEL BREAKDOWN:</b>\n"
        f"▫️ <b>Level 1  ➜</b>  ₹1\n"
        f"▫️ <b>Level 2  ➜</b>  ₹3\n"
        f"▫️ <b>Level 3  ➜</b>  ₹7\n"
        f"▫️ <b>Level 4  ➜</b>  ₹16\n"
        f"▫️ <b>Level 5  ➜</b>  ₹40\n"
        f"▫️ <b>Level 6  ➜</b>  ₹85\n"
        f"▫️ <b>Level 7  ➜</b>  ₹200\n"
        f"▫️ <b>Level 8  ➜</b>  ₹420\n"
        f"▫️ <b>Level 9  ➜</b>  ₹900\n"
        f"▫️ <b>Level 10 ➜</b>  ₹2000\n"
        f"▫️ <b>Level 11 ➜</b>  ₹4500\n"
        f"▫️ <b>Level 12 ➜</b>  ₹10000\n\n"
        f"💰 <b>TOTAL REQUIRED BALANCE:</b>\n"
        f"📌 <b>Up to Level 10 Total: ₹3,672</b>\n"
        f"📌 <b>Up to Level 12 Total: ₹18,172</b>"
    )
    try:
        await app.bot.send_message(chat_id=CHANNEL_ID, text=chart_msg, parse_mode=ParseMode.HTML, reply_markup=markup)
    except Exception as e:
        print(f"Level Chart Error: {e}")


async def send_mid_session_alert(app, markup):
    profit_alert_msg = (
        f"💎 🔔 <b>MID-SESSION PROFIT ALERT / हाफ-टाइम प्रॉफिट नोटिस / সেশনের মাঝামাঝি প্রফিট নোটিশ</b> 🔔 💎\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🇬🇧 <b>ENGLISH:</b>\n"
        f"🎯 <b>Are you in Profit?</b> If you have already achieved your targeted win/profit, you can <b>conclude your trading session for today here!</b>\n"
        f"🚫 There is no need to take further risks in the remaining periods. Secure your profit and wait for the next session! 💰✨\n\n"
        f"🇮🇳 <b>हिंदी (HINDI):</b>\n"
        f"🎯 <b>क्या आप प्रॉफिट में हैं?</b> अगर आपने अपना आज का टारगेट प्रॉफिट पूरा कर लिया है, तो आप <b>आज के लिए अपनी ट्रेडिंग यहीं समाप्त कर सकते हैं!</b>\n"
        f"🚫 आगे के पीरियड्स में रिस्क लेने की कोई जरूरत नहीं है। अपना प्रॉफिट सुरक्षित करें और अगले सेशन का इंतजार करें! 💰✨\n\n"
        f"🇮🇳 <b>বাংলা (BANGLA):</b>\n"
        f"🎯 <b>আপনি কি প্রফিটে আছেন?</b> আপনি যদি ইতিমধ্যেই আপনার টার্গেট অনুযায়ী প্রফিট করে ফেলে থাকেন, তবে <b>আজকের মতো সেশনটি এখানেই সমাপ্ত করতে পারেন!</b>\n"
        f"🚫 পরবর্তী পিরিয়ডগুলোতে আর নতুন করে রিস্ক নেওয়ার প্রয়োজন নেই। আপনার প্রফিট নিরাপদ রাখুন এবং পরবর্তী সেশনের জন্য অপেক্ষা করুন! 💰✨\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 <i>Tip: Control your emotions & follow strict Money Management!</i>"
    )
    try:
        await app.bot.send_message(chat_id=CHANNEL_ID, text=profit_alert_msg, parse_mode=ParseMode.HTML, reply_markup=markup)
    except Exception as e:
        print(f"Mid-session Alert Error: {e}")


async def send_team_building_message(app, markup):
    team_msg = (
        f"💎 👥 <b>TEAM BUILDING & DAILY INCOME / टीम बिल्डिंग और इनकम / টিম বিল্ডিং ও ডেইলি ইনকাম</b> 👥 💎\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🇬🇧 <b>ENGLISH:</b>\n"
        f"🎯 <b>Want to maximize your earnings?</b> Build your own VIP prediction team! Refer your friends, create a strong team, and earn massive daily commissions automatically! 🚀💰\n\n"
        f"🇮🇳 <b>हिंदी (HINDI):</b>\n"
        f"🎯 <b>अपनी कमाई बढ़ाना चाहते हैं?</b> अपनी खुद की VIP टीम बनाएं! दोस्तों को रेफर करें और हर दिन शानदार कमिशन और पैसिव इनकम कमाएं! 🚀💰\n\n"
        f"🇮🇳 <b>বাংলা (BANGLA):</b>\n"
        f"🎯 <b>আপনার ইনকাম আরও বাড়াতে চান?</b> আজই আপনার নিজস্ব একটি শক্তিশালী ভিআইপি টিম তৈরি করুন! বন্ধুদের ইনভাইট বা রেফার করুন, টিম বড় করুন এবং প্রতিদিন নিশ্চিত প্যাসিভ ইনকাম উপভোগ করুন! 🚀💰\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔗 <i>Share your referral link now & start building your empire!</i>"
    )
    try:
        await app.bot.send_message(chat_id=CHANNEL_ID, text=team_msg, parse_mode=ParseMode.HTML, reply_markup=markup)
    except Exception as e:
        print(f"Team Building Error: {e}")


async def send_meeting_announcement(app, markup):
    meeting_msg = (
        f"📢 ✨ <b>ডেইলি প্রেডিকশন শিডিউল ঘোষণা</b> ✨ 📢\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🎯 <b>আমাদের প্রতিদিনের প্রেডিকশন শিডিউল ও লাইভ স্ট্রিম নির্দেশনা:</b>\n\n"
        f"🟢 <b>সকাল ৯:০০ টায়:</b> টেলিগ্রাম চ্যানেলে লাইভ স্ট্রিম চালু করা হবে। সবাই সকাল ৯:০০ টায় টেলিগ্রামে জয়েন করবেন।\n"
        f"🟡 <b>দুপুর ৩:০০ টা (ইন্ডিয়ান টাইম):</b> এআই (AI) সিস্টেম থেকে অটোমেটিক প্রেডিকশন আসবে।\n"
        f"🔵 <b>রাত ৮:০০ টায়:</b> টেলিগ্রাম চ্যানেলে লাইভ স্ট্রিম চালু করা হবে। সবাই রাত ৮:০০ টায় টেলিগ্রামে জয়েন করবেন।\n\n"
        f"👉 সবাই নির্দিষ্ট সময়ে টেলিগ্রাম লাইভ স্ট্রিমে ও ভয়েস কলে একটিভ থাকবেন! 🚀\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    try:
        await app.bot.send_message(chat_id=CHANNEL_ID, text=meeting_msg, parse_mode=ParseMode.HTML, reply_markup=markup)
    except Exception as e:
        print(f"Meeting Announcement Error: {e}")


async def send_next_session_info(app, next_session_name, time_str):
    next_msg = (
        f"💎 ⏰ <b>NEXT SESSION INFO / अगली सेशन की जानकारी / পরবর্তী সেশনের তথ্য</b> ⏰ 💎\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🇬🇧 🔹 <b>ENGLISH:</b>\n"
        f"Next Session: {next_session_name} at {time_str}. Get ready for the next profit wave!\n\n"
        f"🇮🇳 🔸 <b>हिंदी (HINDI):</b>\n"
        f"अगला सेशन: {time_str} पर {next_session_name} शुरू होगा।\n\n"
        f"🇮🇳 🔹 <b>বাংলা (BANGLA):</b>\n"
        f"পরবর্তী সেশন: {time_str} এ {next_session_name} শুরু হবে। প্রস্তুত থাকুন!\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 Play Raxi Win 🏆", url="https://raxiwin.com")],
        [InlineKeyboardButton("📊 Join VIP Channel", url="https://t.me/RexiWinAIPrediction")]
    ])
    try:
        await app.bot.send_message(chat_id=CHANNEL_ID, text=next_msg, parse_mode=ParseMode.HTML, reply_markup=markup)
    except Exception as e:
        print(f"Next Session Error: {e}")


# ==========================================
# 🚀 Telegram Automation Main Loop (Indian Time Schedule Active)
# ==========================================
async def send_auto_prediction(app):
    last_sent_period = ""
    last_alert_date_session = ""    
    last_chart_date_session = ""
    last_next_date_session = ""     
    last_mid_date_session = ""
    last_team_date_session = ""
    last_meeting_date_session = ""  
    last_morning_schedule_date = ""
    last_night_schedule_date = ""

    keyboard = [
        [InlineKeyboardButton("🎮 Play Raxi Win 🏆", url="https://raxiwin.com")],
        [InlineKeyboardButton("📊 Join VIP Channel", url="https://t.me/RexiWinAIPrediction")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    print("Raxi Win Indian Time Schedule Loop started...")

    while True:
        try:
            now = get_ist_time()
            hour = now.hour
            minute = now.minute
            second = now.second
            current_date_str = now.strftime('%Y-%m-%d')

            alert_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Ready & Deposit", url="https://raxiwin.com")],
                [InlineKeyboardButton("📢 Channel Link", url="https://t.me/RexiWinAIPrediction")]
            ])

            # ১. সকাল ১০:০০ টা (ইন্ডিয়ান টাইম) - ডেইলি শিডিউল ঘোষণা
            if hour == 10 and minute == 0:
                morning_key = f"{current_date_str}_MORNING_SCHEDULE"
                if last_morning_schedule_date != morning_key:
                    await send_meeting_announcement(app, alert_markup)
                    last_morning_schedule_date = morning_key

            # ২. রাত ৯:০০ টা (ইন্ডিয়ান টাইম) - ডেইলি শিডিউল ঘোষণা
            if hour == 21 and minute == 0:
                night_key = f"{current_date_str}_NIGHT_SCHEDULE"
                if last_night_schedule_date != night_key:
                    await send_meeting_announcement(app, alert_markup)
                    last_night_schedule_date = night_key

            # ৩. দুপুর ২:৫৫ মিনিটে রেডি অ্যালার্ট (ইন্ডিয়ান টাইম)
            if hour == 14 and minute == 55:
                alert_key = f"{current_date_str}_AFTERNOON_ALERT"
                if last_alert_date_session != alert_key:
                    await send_ready_alert(app, "Afternoon Session (Indian Time 3:00 PM)", alert_markup)
                    last_alert_date_session = alert_key

            # ৪. দুপুর ২:৫৭ মিনিটে চার্ট অ্যালার্ট (ইন্ডিয়ান টাইম)
            if hour == 14 and minute == 57:
                chart_key = f"{current_date_str}_AFTERNOON_CHART"
                if last_chart_date_session != chart_key:
                    await send_level_chart_alert(app, alert_markup)
                    last_chart_date_session = chart_key

            # ৫. মূল সেশন সময়: ইন্ডিয়ান টাইম দুপুর ৩:০০ টা থেকে ৩:৩৫ মিনিট পর্যন্ত
            is_afternoon_session = (hour == 15 and minute <= 35)

            if is_afternoon_session:
                period_num = get_current_1min_period()
                if period_num != last_sent_period:
                    pred = get_high_tech_ai_prediction()
                    pred_text = "SMALL" if pred == "SMALL" else "BIG"
                    color_text = get_smart_trend_color(pred_text)
                    
                    # 🛠️ Updated Format: Ultra AI Prediction with clean alignment & zero gap issues
                    msg = (
                        f"💎 RAXI WIN ULTRA AI PREDICTION 💎\n"
                        f"💎 RAXI WIN VIP PREDICTION 1 Min 💎\n\n"
                        f"🔷 PERIOD: {period_num}\n"
                        f"🎯 PREDICTION: {pred_text}\n"
                        f"🎨 COLOR: {color_text}\n\n"
                        f"💡 Recommended: Safe 1-10 Level Martingale"
                    )
                    
                    await app.bot.send_message(
                        chat_id=CHANNEL_ID,
                        text=msg,
                        parse_mode=ParseMode.HTML,
                        reply_markup=reply_markup
                    )
                    
                    print(f"Signal sent successfully with Ultra AI format for period: {period_num}")
                    last_sent_period = period_num

            # ৬. দুপুর ৩:৩০ মিনিটে মিডিলে প্রফিট অ্যালার্ট (ইন্ডিয়ান টাইম)
            if hour == 15 and minute == 30:
                profit_key = f"{current_date_str}_AFTERNOON_PROFIT_ALERT"
                if last_mid_date_session != profit_key:
                    await send_mid_session_alert(app, alert_markup)
                    last_mid_date_session = profit_key

            # ৭. দুপুর ৩:৩৬ মিনিটে টিম বিল্ডিং মেসেজ (ইন্ডিয়ান টাইম)
            if hour == 15 and minute == 36:
                team_key = f"{current_date_str}_AFTERNOON_TEAM"
                if last_team_date_session != team_key:
                    await send_team_building_message(app, alert_markup)
                    last_team_date_session = team_key

            # ৮. দুপুর ৩:৩৭ মিনিটে সেশন শেষে শিডিউল অ্যানাউন্সমেন্ট (ইন্ডিয়ান টাইম)
            if hour == 15 and minute == 37:
                meeting_key = f"{current_date_str}_AFTERNOON_MEETING"
                if last_meeting_date_session != meeting_key:
                    await send_meeting_announcement(app, alert_markup)
                    last_meeting_date_session = meeting_key

            # ৯. দুপুর ৩:৩৮ মিনিটে পরবর্তী সেশন নোটিশ (ইন্ডিয়ান টাইম)
            if hour == 15 and minute == 38:
                next_key = f"{current_date_str}_AFTERNOON_NEXT"
                if last_next_date_session != next_key:
                    await send_next_session_info(app, "Night Live Stream / Voice Prediction", "8:00 PM (Indian Time)")
                    last_next_date_session = next_key

        except Exception as e:
            print(f"Loop Error: {e}")

        await asyncio.sleep(2)


# ==========================================
# ⚙️ Main Application Launcher
# ==========================================
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    await app.initialize()
    await app.start()
    
    threading.Thread(target=run_web, daemon=True).start()
    
    print("Raxi Win Indian Time Bot is fully running and active...")
    
    await send_auto_prediction(app)

if __name__ == "__main__":
    asyncio.run(main())
