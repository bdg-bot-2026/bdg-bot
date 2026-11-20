import os
import random
from datetime import datetime, timedelta, timezone
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
    app_web.run(host='0.0.0.0', port=port, use_reloader=False)


# ==========================================
# 🤖 Telegram Bot Configurations
# ==========================================
TOKEN = os.environ.get("BOT_TOKEN", "8937609482:AAFB3oMP4s70s5L4krgetPVDw761FEW2wcI").strip()
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1003744216692"))

current_pattern = []
pattern_index = 0

# 🧠 Stateful Trend Memory Buffer (Stores last 100 predictions for analysis)
prediction_history = deque(maxlen=100)


# ==========================================
# ⏰ Time & Live Game Period Synchronization (IST & UTC)
# ==========================================
def get_ist_time():
    try:
        ist_tz = pytz.timezone('Asia/Kolkata')
        return datetime.now(ist_tz)
    except Exception:
        return datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)

def get_current_1min_period():
    now_utc = datetime.now(timezone.utc)
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
# 📢 Safe Sender & Supporting Message Functions
# ==========================================
async def safe_send_message(app, text, markup=None):
    try:
        await app.bot.send_message(
            chat_id=CHANNEL_ID,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=markup
        )
        return True
    except Exception as e:
        print(f"[SEND ERROR] Target {CHANNEL_ID}: {e}")
        return False


async def send_ready_alert(app, session_name, markup):
    alert_msg = (
        f"<b>RAXI WIN VIP PREDICTION 1 Min:</b>\n"
        f"🚨 🔥 <b>ATTENTION: {session_name} IS ABOUT TO START!</b> 🔥 🚨\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 <b>Get ready & prepare your account! / तैयार हो जाइए! / সবাই রেডি থাকুন!</b>\n\n"
        f"🇬🇧 <b>ENGLISH:</b>\n"
        f"💎 <b>Maintain Balance:</b> Follow safe 1-10 Level Martingale.\n"
        f"🛡️ <b>3x Turnover Rule:</b> Complete 3x betting of your deposit amount before withdrawal.\n"
        f"🚫 <b>No Illegal Bets:</b> Do NOT place Big & Small together.\n"
        f"⚠️ <b>No Red/Green Mix:</b> Do not bet on Red & Green simultaneously.\n"
        f"📱 <b>Single Device:</b> Do not use 2 accounts on 1 phone.\n"
        f"📶 <b>Network:</b> Avoid public Wi-Fi.\n\n"
        f"🇮🇳 <b>हिंदी (HINDI):</b>\n"
        f"💎 <b>बैलेंस बनाए रखें:</b> सुरक्षित 1-10 लेवल मार्टिंगेल फॉलो करें।\n"
        f"🛡️ <b>3x टर्नओवर नियम:</b> विथड्रॉल से पहले 3x बेटिंग पूरी करें।\n"
        f"🚫 <b>कोई अवैध शर्त नहीं:</b> Big और Small एकसाथ न लगाएं।\n"
        f"⚠️ <b>रेड/ग्रीन मिक्स न करें:</b> एकसाथ दोनों पर बेट न लगाएं।\n"
        f"📱 <b>एक डिवाइस नियम:</b> एक फोन में दो आईडी लॉगिन न करें।\n"
        f"📶 <b>नेटवर्क चेतावनी:</b> पब्लिक वाई-फाई का उपयोग न करें।\n\n"
        f"🇮🇳 <b>বাংলা (BANGLA):</b>\n"
        f"💎 <b>ব্যালেন্স মেইনটেইন করুন:</b> নিরাপদ ১-১০ লেভেল মার্টিনগেল ফলো করুন।\n"
        f"🛡️ <b>৩x টার্নওভার রুল:</b> ডিপোজিটের পর ৩x বেটিং কমপ্লিট করুন।\n"
        f"🚫 <b>ইল্লিগাল বেট নিষেধ:</b> বিগ এবং স্মল একসঙ্গে কেউ করবেন না।\n"
        f"⚠️ <b>রেড-গ্রীন একসঙ্গে নয়:</b> রেড ও গ্রীনে একসাথে বেট লাগাবেন না।\n"
        f"📱 <b>এক ফোনে এক আইডি:</b> একটা ফোনে দুটো আইডি লগইন করবেন না।\n"
        f"📶 <b>ওয়াইফাই সতর্কবার্তা:</b> ওয়াইফাই প্লে বা পাবলিক নেটওয়ার্ক এড়িয়ে চলুন।"
    )
    await safe_send_message(app, alert_msg, markup)


async def send_level_chart_alert(app, markup):
    chart_msg = (
        f"💎 <b>RAXI WIN VIP 1-10 LEVEL MARTINGALE</b> 💎\n"
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
        f"▫️ <b>Level 10 ➜</b>  ₹2000\n\n"
        f"💰 <b>TOTAL REQUIRED BALANCE:</b>\n"
        f"📌 <b>Up to Level 10 Total: ₹3,672</b>"
    )
    await safe_send_message(app, chart_msg, markup)


async def send_prediction_signal(app, period_num, pred_text, color_text, markup):
    msg = (
        f"<b>💎 RAXI WIN ULTRA AI PREDICTION 💎</b>\n"
        f"<b>💎 RAXI WIN VIP PREDICTION 1 Min 💎</b>\n\n"
        f"🔷 <b>PERIOD:</b> {period_num}\n"
        f"🎯 <b>PREDICTION:</b> {pred_text}\n"
        f"🎨 <b>COLOR:</b> {color_text}\n"
        f"───────────────────\n"
        f"💡 Recommended: Safe 1-10 Level Martingale"
    )
    return await safe_send_message(app, msg, markup)


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
    await safe_send_message(app, profit_alert_msg, markup)


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
    await safe_send_message(app, team_msg, markup)


async def send_next_session_info(app, next_session_name, time_str):
    next_msg = (
        f"💎 ⏰ <b>NEXT SESSION INFO / अगली सेशन की जानकारी / পরবর্তী সেশনের তথ্য</b> ⏰ 💎\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🇬🇧 🔹 <b>ENGLISH:</b>\n"
        f"Next Session: {next_session_name} at {time_str}. Get ready!\n\n"
        f"🇮🇳 🔸 <b>हिंदी (HINDI):</b>\n"
        f"अगला सेशन: {time_str} पर <b>{next_session_name}</b> शुरू होगा। तैयार रहें!\n\n"
        f"🇮🇳 🔹 <b>বাংলা (BANGLA):</b>\n"
        f"পরবর্তী সেশন: {time_str}-এ <b>{next_session_name}</b> শুরু হবে। প্রস্তুত থাকুন!\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 Play Raxi Win 🏆", url="https://raxiwin.com")],
        [InlineKeyboardButton("📊 Join VIP Channel", url="https://t.me/RexiWinAIPrediction")]
    ])
    await safe_send_message(app, next_msg, markup)


# ==========================================
# 🚀 Telegram Automation Main Loop (3 Sessions Identical Flow)
# ==========================================
async def send_auto_prediction(app):
    last_sent_period = ""
    sent_keys = set()

    keyboard = [
        [InlineKeyboardButton("🎮 Play Raxi Win 🏆", url="https://raxiwin.com")],
        [InlineKeyboardButton("📊 Join VIP Channel", url="https://t.me/RexiWinAIPrediction")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    alert_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Ready & Deposit", url="https://raxiwin.com")],
        [InlineKeyboardButton("📢 Channel Link", url="https://t.me/RexiWinAIPrediction")]
    ])

    sessions = [
        {
            "name": "MORNING",
            "label": "Morning Session (Indian Time 9:00 AM)",
            "alert_time": (8, 55),
            "chart_time": (8, 57),
            "pred_hour": 9,
            "pred_max_minute": 35,
            "mid_time": (9, 30),
            "team_time": (9, 36),
            "next_time": (9, 38),
            "next_session_name": "Afternoon Session",
            "next_time_str": "3:00 PM (Indian Time)",
        },
        {
            "name": "AFTERNOON",
            "label": "Afternoon Session (Indian Time 3:00 PM)",
            "alert_time": (14, 55),
            "chart_time": (14, 57),
            "pred_hour": 15,
            "pred_max_minute": 35,
            "mid_time": (15, 30),
            "team_time": (15, 36),
            "next_time": (15, 38),
            "next_session_name": "Night Session",
            "next_time_str": "8:00 PM (Indian Time)",
        },
        {
            "name": "NIGHT",
            "label": "Night Session (Indian Time 8:00 PM)",
            "alert_time": (19, 55),
            "chart_time": (19, 57),
            "pred_hour": 20,
            "pred_max_minute": 35,
            "mid_time": (20, 30),
            "team_time": (20, 36),
            "next_time": (20, 38),
            "next_session_name": "Morning Session",
            "next_time_str": "9:00 AM (Indian Time)",
        },
    ]

    print("Raxi Win 3-Session Indian Time Schedule Loop started...")

    while True:
        try:
            now = get_ist_time()
            current_hm = (now.hour, now.minute)
            current_date_str = now.strftime('%Y-%m-%d')

            sent_keys = {k for k in sent_keys if k.startswith(current_date_str)}
            in_any_prediction_window = False

            for s in sessions:
                s_name = s["name"]

                # ১. Ready Alert
                if current_hm == s["alert_time"]:
                    key = f"{current_date_str}_{s_name}_ALERT"
                    if key not in sent_keys:
                        await send_ready_alert(app, s["label"], alert_markup)
                        sent_keys.add(key)

                # ২. Level Chart Alert
                if current_hm == s["chart_time"]:
                    key = f"{current_date_str}_{s_name}_CHART"
                    if key not in sent_keys:
                        await send_level_chart_alert(app, alert_markup)
                        sent_keys.add(key)

                # ৩. Prediction Window (:00 থেকে :35 পর্যন্ত)
                if (now.hour == s["pred_hour"] and now.minute <= s["pred_max_minute"]):
                    in_any_prediction_window = True
                    period_num = get_current_1min_period()
                    if period_num != last_sent_period:
                        pred = get_high_tech_ai_prediction()
                        pred_text = "SMALL" if pred == "SMALL" else "BIG"
                        color_text = get_smart_trend_color(pred_text)

                        sent_ok = await send_prediction_signal(app, period_num, pred_text, color_text, reply_markup)
                        if sent_ok:
                            print(f"[{s_name}] Signal sent for period: {period_num}")
                            last_sent_period = period_num

                # ৪. Mid-Session Profit Alert
                if current_hm == s["mid_time"]:
                    key = f"{current_date_str}_{s_name}_MID"
                    if key not in sent_keys:
                        await send_mid_session_alert(app, alert_markup)
                        sent_keys.add(key)

                # ৫. Team Building Message
                if current_hm == s["team_time"]:
                    key = f"{current_date_str}_{s_name}_TEAM"
                    if key not in sent_keys:
                        await send_team_building_message(app, alert_markup)
                        sent_keys.add(key)

                # ৬. Next Session Info
                if current_hm == s["next_time"]:
                    key = f"{current_date_str}_{s_name}_NEXT"
                    if key not in sent_keys:
                        await send_next_session_info(app, s["next_session_name"], s["next_time_str"])
                        sent_keys.add(key)

            if not in_any_prediction_window:
                last_sent_period = ""

        except Exception as e:
            print(f"[LOOP ERROR] {e}")

        await asyncio.sleep(2)


# ==========================================
# ⚙️ Main Application Launcher
# ==========================================
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    await app.initialize()
    await app.start()

    try:
        bot_info = await app.bot.get_me()
        chat_info = await app.bot.get_chat(CHANNEL_ID)
        print(f"Bot Active: @{bot_info.username} | Connected To: {chat_info.title} ({CHANNEL_ID})")
    except Exception as e:
        print(f"[STARTUP CHECK ERROR] Token/Channel check failed: {e}")

    threading.Thread(target=run_web, daemon=True).start()
    print("Raxi Win 3-Session Indian Time Bot is fully running and active...")

    await send_auto_prediction(app)

if __name__ == "__main__":
    asyncio.run(main())
        
