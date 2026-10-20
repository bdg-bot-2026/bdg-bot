import os
import random
from datetime import datetime, timedelta
import pytz
import asyncio
import threading
import requests
from flask import Flask
from telegram.ext import ApplicationBuilder
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

# ==========================================
# 🌐 Flask Web Server
# ==========================================
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot status: ONLINE (Raxi Win Real API 50-Period Trend & Clean Auto-Win/Loss Active)"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)


# ==========================================
# 🤖 Telegram Bot Configurations
# ==========================================
RAW_TOKEN = os.environ.get("BOT_TOKEN", "8937609482:AAEncEd0IY787haa0Pg1Azp2DHVT3Ulz1z14A")
TOKEN = RAW_TOKEN.strip()
CHANNEL_ID = "@RexiWinAIPrediction"


# ==========================================
# ⏰ Time & Live Game Period Synchronization Function
# ==========================================
def get_bd_time():
    try:
        bd_tz = pytz.timezone('Asia/Dhaka')
        return datetime.now(bd_tz)
    except Exception:
        return datetime.utcnow() + timedelta(hours=6)

def get_current_1min_period():
    now_utc = datetime.now(pytz.utc)
    date_str = now_utc.strftime("%Y%m%d")
    
    total_minutes_utc = (now_utc.hour * 60) + now_utc.minute
    period_count = 10000 + total_minutes_utc + 1
    
    return f"{date_str}1000{period_count}"


# ==========================================
# 📊 Real API 50-Period Trend & Win/Loss Checker
# ==========================================
def get_api_history():
    url = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            res_json = response.json()
            return res_json['data']['list']
    except Exception as e:
        print(f"API Fetch Error: {e}")
    return []

def get_high_tech_ai_prediction():
    games_list = get_api_history()
    if not games_list:
        return "BIG"
    
    count = min(50, len(games_list))
    recent_results = []
    
    for i in range(count):
        num = int(games_list[i]['number'])
        bs = "BIG" if num >= 5 else "SMALL"
        recent_results.append(bs)
    
    big_count = recent_results.count("BIG")
    small_count = recent_results.count("SMALL")
    
    print(f"Trend Analysis -> Last {count} Periods | BIG: {big_count}, SMALL: {small_count}")
    
    if big_count > small_count:
        if len(recent_results) >= 3 and recent_results[0] == recent_results[1] == recent_results[2]:
            return "SMALL" if recent_results[0] == "BIG" else "BIG"
        return "BIG"
    elif small_count > big_count:
        if len(recent_results) >= 3 and recent_results[0] == recent_results[1] == recent_results[2]:
            return "BIG" if recent_results[0] == "SMALL" else "SMALL"
        return "SMALL"
    else:
        return "SMALL" if recent_results[0] == "BIG" else "BIG"

def check_period_result(target_period):
    games_list = get_api_history()
    for game in games_list:
        issue_number = str(game['issueNumber'])
        if issue_number == str(target_period):
            num = int(game['number'])
            actual_bs = "BIG" if num >= 5 else "SMALL"
            return actual_bs
    return None


# ==========================================
# 🎨 Smart Color Evaluator Logic (Only Green & Red)
# ==========================================
def get_smart_trend_color(pred_text):
    if pred_text == "BIG":
        return random.choice(["GREEN 🟢", "GREEN 🟢", "RED 🔴"])
    else:
        return random.choice(["RED 🔴", "RED 🔴", "GREEN 🟢"])


# ==========================================
# 📢 Supporting Notice & Message Functions
# ==========================================
async def send_ready_alert(app, session_name, markup):
    alert_msg = (
        f"<b>RAXI WIN VIP PREDICTION 1 Min:</b>\n"
        f"🚨 🔥 <b>ATTENTION: {session_name} IS ABOUT TO START!</b> 🔥 🚨\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 <b>Get ready & prepare your account! / तैयार हो जाइए! / সবাই রেডি থাকুন!</b>\n\n"
        f"🇬🇧 <b>ENGLISH:</b>\n"
        f"💎 <b>Maintain Balance:</b> Follow safe 10-Level Martingale.\n"
        f"🛡️ <b>2x Turnover Rule:</b> Complete 2x betting of your deposit amount before withdrawal.\n"
        f"🚫 <b>No Illegal Bets:</b> Do NOT place Big & Small together.\n"
        f"⚠️ <b>No Red/Green Mix:</b> Do not bet on Red & Green simultaneously.\n"
        f"📱 <b>Single Device:</b> Do not use 2 accounts on 1 phone.\n"
        f"📶 <b>Network:</b> Avoid public Wi-Fi.\n\n"
        f"🇮🇳 <b>हिंदी (HINDI):</b>\n"
        f"💎 <b>बैलेंस बनाए रखें:</b> सुरक्षित 10-लेवल मार्टिंगेल फॉलो करें।\n"
        f"🛡️ <b>2x टर्नओवर नियम:</b> विथड्रॉल से पहले 2x बेटिंग पूरी करें।\n"
        f"🚫 <b>कोई अवैध शर्त नहीं:</b> Big और Small एकसाथ न लगाएं।\n"
        f"⚠️ <b>रेड/ग्रीन मिक्स न करें:</b> एकसाथ दोनों पर बेट न लगाएं।\n"
        f"📱 <b>एक डिवाइस नियम:</b> एक फोन में दो आईडी लॉगिन न करें।\n"
        f"📶 <b>नेटवर्क चेतावनी:</b> पब्लिक वाई-फाई का उपयोग न करें।\n\n"
        f"🇮🇳 <b>বাংলা (BANGLA):</b>\n"
        f"💎 <b>ব্যালেন্স মেইনটেইন করুন:</b> নিরাপদ ১০ লেভেল মার্টিনগেল ফলো করুন।\n"
        f"🛡️ <b>২x টার্নওভার রুল:</b> ডিপোজিটের পর ২x বেটিং কমপ্লিট করুন।\n"
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

async def send_referral_promo(app, markup):
    promo_msg = (
        f"💎 ✨ <b>MAXIMIZE YOUR EARNINGS WITH RAXI WIN!</b> ✨ 💎\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🇬🇧 <b>ENGLISH:</b>\n"
        f"Build your powerful team and generate passive daily income! Earn lifetime commissions, daily salaries, and referral bonuses. Share your link now!\n\n"
        f"🇮🇳 <b>हिंदी (HINDI):</b>\n"
        f"अपनी खुद की मजबूत टीम बनाएं और रोजाना पैसिव इनकम कमाएं! लाइफटाइम कमीशन, डेली सैलरी और रेफरल बोनस पाएं। अभी अपना लिंक शेयर करें!\n\n"
        f"🇮🇳 <b>বাংলা (BANGLA):</b>\n"
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
        f"🇮🇳 🔹 <b>বাংলা (BANGLA):</b>\n"
        f"পরবর্তী ভিআইপি সেশন: {time_str} এ {next_session_name} শুরু হবে। পরবর্তী প্রফিটের জন্য প্রস্তুত থাকুন!\n"
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
# 🚀 Telegram Automation Main Loop
# ==========================================
async def send_auto_prediction(app):
    last_sent_period = ""
    pending_check_msg_id = None
    pending_period = ""
    pending_prediction = ""
    
    last_alert_date_session = ""    
    last_chart_date_session = ""
    last_promo_date_session = ""    
    last_next_date_session = ""     
    last_mid_date_session = ""

    keyboard = [
        [InlineKeyboardButton("🎮 Play Raxi Win 🏆", url="https://raxiwin.com")],
        [InlineKeyboardButton("📊 Join VIP Channel", url="https://t.me/RexiWinAIPrediction")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    print("Raxi Win Automation Loop started successfully with 50-Period API & Simple Win/Loss Tracker...")

    while True:
        try:
            now = get_bd_time()
            hour = now.hour
            minute = now.minute
            current_date_str = now.strftime('%Y-%m-%d')

            alert_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Ready & Deposit", url="https://raxiwin.com")],
                [InlineKeyboardButton("📢 Channel Link", url="https://t.me/RexiWinAIPrediction")]
            ])

            # -------------------------------------------------------------
            # 🔍 ব্যাকগ্রাউন্ড অটো WIN/LOSS ট্র্যাকিং (শুধু WIN অথবা LOSS)
            # -------------------------------------------------------------
            if pending_check_msg_id and pending_period:
                actual_result = check_period_result(pending_period)
                if actual_result:
                    is_win = (actual_result == pending_prediction)
                    result_text = "✅ <b>WIN</b>" if is_win else "❌ <b>LOSS</b>"
                    color_text = get_smart_trend_color(pending_prediction)
                    
                    updated_msg = (
                        f"💎 <b>RAXI WIN ULTRA AI PREDICTION</b> 💎\n"
                        f"💎 <b>RAXI WIN VIP PREDICTION 1 Min</b> 💎\n\n"
                        f"🔹 <b>PERIOD:</b> {pending_period}\n"
                        f"🎯 <b>PREDICTION:</b> {pending_prediction}\n"
                        f"🎨 <b>COLOR:</b> {color_text}\n"
                        f"📊 <b>STATUS:</b> {result_text}\n"
                        f"───────────────────\n"
                        f"💡 <i>Recommended: Safe 1-10 Level Martingale</i>"
                    )
                    try:
                        await app.bot.edit_message_text(
                            chat_id=CHANNEL_ID,
                            message_id=pending_check_msg_id,
                            text=updated_msg,
                            parse_mode=ParseMode.HTML,
                            reply_markup=reply_markup
                        )
                        print(f"Updated Period {pending_period} Result: {result_text}")
                    except Exception as edit_err:
                        print(f"Edit Message Error: {edit_err}")
                    
                    pending_check_msg_id = None
                    pending_period = ""
                    pending_prediction = ""

            # -------------------------------------------------------------
            # 📢 নোটিশ ও অ্যালার্ট মেসেজসমূহ
            # -------------------------------------------------------------
            if hour == 7 and minute == 25:
                alert_key = f"{current_date_str}_MORNING_ALERT"
                if last_alert_date_session != alert_key:
                    await send_ready_alert(app, "Morning Session (7:30 AM)", alert_markup)
                    last_alert_date_session = alert_key

            elif hour == 14 and minute == 25:
                alert_key = f"{current_date_str}_AFTERNOON_ALERT"
                if last_alert_date_session != alert_key:
                    await send_ready_alert(app, "Afternoon Session (2:30 PM)", alert_markup)
                    last_alert_date_session = alert_key

            elif hour == 20 and minute == 25:
                alert_key = f"{current_date_str}_NIGHT_ALERT"
                if last_alert_date_session != alert_key:
                    await send_ready_alert(app, "Night Session (8:30 PM)", alert_markup)
                    last_alert_date_session = alert_key

            if hour == 7 and minute == 27:
                chart_key = f"{current_date_str}_MORNING_CHART"
                if last_chart_date_session != chart_key:
                    await send_level_chart_alert(app, alert_markup)
                    last_chart_date_session = chart_key

            elif hour == 14 and minute == 27:
                chart_key = f"{current_date_str}_AFTERNOON_CHART"
                if last_chart_date_session != chart_key:
                    await send_level_chart_alert(app, alert_markup)
                    last_chart_date_session = chart_key

            elif hour == 20 and minute == 27:
                chart_key = f"{current_date_str}_NIGHT_CHART"
                if last_chart_date_session != chart_key:
                    await send_level_chart_alert(app, alert_markup)
                    last_chart_date_session = chart_key

            if (hour == 8 and minute == 0) or (hour == 15 and minute == 0) or (hour == 21 and minute == 0):
                profit_key = f"{current_date_str}_{hour}_PROFIT_ALERT"
                if last_mid_date_session != profit_key:
                    await send_mid_session_alert(app, alert_markup)
                    last_mid_date_session = profit_key

            promo_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Join & Start Refer", url="https://raxiwin.com")],
                [InlineKeyboardButton("💎 Contact For Support", url="https://t.me/RexiWinAIPrediction")]
            ])

            if (hour == 8 and minute == 6) or (hour == 15 and minute == 6) or (hour == 21 and minute == 6):
                promo_key = f"{current_date_str}_{hour}_PROMO"
                if last_promo_date_session != promo_key:
                    await send_referral_promo(app, promo_markup)
                    last_promo_date_session = promo_key

            if hour == 8 and minute == 7:
                next_key = f"{current_date_str}_MORNING_NEXT"
                if last_next_date_session != next_key:
                    await send_next_session_info(app, "Afternoon Session", "2:30 PM")
                    last_next_date_session = next_key

            elif hour == 15 and minute == 7:
                next_key = f"{current_date_str}_AFTERNOON_NEXT"
                if last_next_date_session != next_key:
                    await send_next_session_info(app, "Night Session", "8:30 PM")
                    last_next_date_session = next_key

            elif hour == 21 and minute == 7:
                next_key = f"{current_date_str}_NIGHT_NEXT"
                if last_next_date_session != next_key:
                    await send_next_session_info(app, "Morning Session", "7:30 AM (Tomorrow)")
                    last_next_date_session = next_key

            # -------------------------------------------------------------
            # 🎯 মূল লাইভ সিগন্যাল পাঠানোর লজিক
            # -------------------------------------------------------------
            is_morning_session = (hour == 7 and minute >= 30) or (hour == 8 and minute <= 5)
            is_afternoon_session = (hour == 14 and minute >= 30) or (hour == 15 and minute <= 5)
            is_night_session = (hour == 20 and minute >= 30) or (hour == 21 and minute <= 5)

            if is_morning_session or is_afternoon_session or is_night_session:
                period_num = get_current_1min_period()
                if period_num != last_sent_period:
                    pred_text = get_high_tech_ai_prediction()
                    color_text = get_smart_trend_color(pred_text)
                    
                    msg = (
                        f"💎 <b>RAXI WIN ULTRA AI PREDICTION</b> 💎\n"
                        f"💎 <b>RAXI WIN VIP PREDICTION 1 Min</b> 💎\n\n"
                        f"🔹 <b>PERIOD:</b> {period_num}\n"
                        f"🎯 <b>PREDICTION:</b> {pred_text}\n"
                        f"🎨 <b>COLOR:</b> {color_text}\n"
                        f"📊 <b>STATUS:</b> ⏳ Waiting for result...\n"
                        f"───────────────────\n"
                        f"💡 <i>Recommended: Safe 1-10 Level Martingale</i>"
                    )
                    
                    sent_msg = await app.bot.send_message(
                        chat_id=CHANNEL_ID,
                        text=msg,
                        parse_mode=ParseMode.HTML,
                        reply_markup=reply_markup
                    )
                    
                    pending_check_msg_id = sent_msg.message_id
                    pending_period = period_num
                    pending_prediction = pred_text
                         print(f"50-Period Signal Sent: {period_num} -> {pred_text}")
                    last_sent_period = period_num

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
    
    print("Raxi Win Ultra AI Bot is running with Simple Win/Loss Tracker...")
    
    await send_auto_prediction(app)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot Stopped.")
