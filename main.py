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

app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot status: ONLINE (Raxi Win Deep 500-Period Trend & 24/7 Auto-Active)"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

RAW_TOKEN = os.environ.get("BOT_TOKEN", "8937609482:AAEncEd0IY787haa0Pg1Azp2DHVT3Ulz1z14A")
TOKEN = RAW_TOKEN.strip()
CHANNEL_ID = "@RexiWinAIPrediction"

# লোকাল ডেটাবেস লিস্ট যেখানে মিনিমাম ৫০০টি পিরিয়ডের ডেটা সেভ ও মেইনটেইন হবে
historical_db = []

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

def get_deep_api_history():
    global historical_db
    url = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            res_json = response.json()
            fetched_list = res_json['data']['list']
            
            # ডেটাবেসে নতুন রেজাল্টগুলো যোগ করা এবং ডুপ্লিকেট এড়ানো
            for game in fetched_list:
                issue = str(game['issueNumber'])
                if not any(str(item['issueNumber']) == issue for item in historical_db):
                    historical_db.insert(0, game)
            
            # ডেটাবেস সাইজ ধরে রাখা যাতে অন্তত ৫০০ বা তার বেশি ডেটা অ্যানালাইসিসের জন্য থাকে
            if len(historical_db) > 1000:
                historical_db = historical_db[:1000]
                
            return historical_db
    except Exception as e:
        print(f"API Deep Fetch Error: {e}")
    return historical_db

def get_deep_ai_prediction():
    games_list = get_deep_api_history()
    if not games_list:
        return "BIG"
    
    # বর্তমান ডেটাবেস থেকে মিনিমাম ৫০০ বা উপলব্ধ ডেটা নিয়ে গভীর অ্যানালাইসিস
    analyze_count = min(500, len(games_list))
    recent_results = []
    
    for i in range(analyze_count):
        num = int(games_list[i]['number'])
        bs = "BIG" if num >= 5 else "SMALL"
        recent_results.append(bs)
        
    big_count = recent_results.count("BIG")
    small_count = recent_results.count("SMALL")
    
    # ডিপ ট্রেন্ড লজিক ও প্যাটার্ন ফিল্টারিং
    if big_count > small_count:
        if len(recent_results) >= 4 and recent_results[0] == recent_results[1] == recent_results[2] == recent_results[3]:
            return "SMALL" if recent_results[0] == "BIG" else "BIG"
        return "BIG"
    elif small_count > big_count:
        if len(recent_results) >= 4 and recent_results[0] == recent_results[1] == recent_results[2] == recent_results[3]:
            return "BIG" if recent_results[0] == "SMALL" else "SMALL"
        return "SMALL"
    else:
        return "SMALL" if recent_results[0] == "BIG" else "BIG"

def check_period_result(target_period):
    games_list = get_deep_api_history()
    for game in games_list:
        issue_number = str(game['issueNumber'])
        if issue_number == str(target_period):
            num = int(game['number'])
            actual_bs = "BIG" if num >= 5 else "SMALL"
            return actual_bs
    return None

def get_smart_trend_color(pred_text):
    if pred_text == "BIG":
        return random.choice(["GREEN 🟢", "GREEN 🟢", "RED 🔴"])
    else:
        return random.choice(["RED 🔴", "RED 🔴", "GREEN 🟢"])

async def send_ready_alert(app, session_name, markup):
    alert_msg = (
        f"<b>RAXI WIN VIP PREDICTION 24/7 Active:</b>\n"
        f"🚨 🔥 <b>ATTENTION: {session_name} IS ABOUT TO START!</b> 🔥 🚨\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 <b>Get ready & prepare your account!</b>\n"
    )
    try:
        await app.bot.send_message(chat_id=CHANNEL_ID, text=alert_msg, parse_mode=ParseMode.HTML, reply_markup=markup)
    except Exception as e:
        print(f"Alert Error: {e}")

async def send_auto_prediction_247(app):
    last_sent_period = ""
    pending_check_msg_id = None
    pending_period = ""
    pending_prediction = ""
    
    keyboard = [
        [InlineKeyboardButton("🎮 Play Raxi Win 🏆", url="https://raxiwin.com")],
        [InlineKeyboardButton("📊 Join VIP Channel", url="https://t.me/RexiWinAIPrediction")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    print("Raxi Win 24/7 Deep 500-Period Automation Loop Started Successfully...")

    while True:
        try:
            # সার্ভার সচল রাখতে এবং টাইমআউট এড়াতে প্রতি সাইকেলে ব্যাকগ্রাউন্ডে ডেটা সিঙ্ক করা
            get_deep_api_history()
            
            now = get_bd_time()
            current_date_str = now.strftime('%Y-%m-%d')

            alert_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Ready & Deposit", url="https://raxiwin.com")],
                [InlineKeyboardButton("📢 Channel Link", url="https://t.me/RexiWinAIPrediction")]
            ])

            # আগের পিরিয়ডের রেজাল্ট চেক করে Win/Loss আপডেট করা
            if pending_check_msg_id and pending_period:
                actual_result = check_period_result(pending_period)
                if actual_result:
                    is_win = (actual_result == pending_prediction)
                    result_text = "✅ <b>WIN</b>" if is_win else "❌ <b>LOSS</b>"
                    color_text = get_smart_trend_color(pending_prediction)
                    
                    updated_msg = (
                        f"💎 <b>RAXI WIN DEEP 500+ AI PREDICTION</b> 💎\n\n"
                        f"🔹 <b>PERIOD:</b> {pending_period}\n"
                        f"🎯 <b>PREDICTION:</b> {pending_prediction}\n"
                        f"🎨 <b>COLOR:</b> {color_text}\n"
                        f"📊 <b>STATUS:</b> {result_text}\n"
                        f"───────────────────\n"
                        f"💡 <i>Analyzed from Deep 500+ Period Database</i>"
                    )
                    try:
                        await app.bot.edit_message_text(
                            chat_id=CHANNEL_ID,
                            message_id=pending_check_msg_id,
                            text=updated_msg,
                            parse_mode=ParseMode.HTML,
                            reply_markup=reply_markup
                        )
                        print(f"Updated Deep Period {pending_period} Result: {result_text}")
                    except Exception as edit_err:
                        print(f"Edit Message Error: {edit_err}")
                    
                    pending_check_msg_id = None
                    pending_period = ""
                    pending_prediction = ""

            # ২৪ ঘণ্টা নন-স্টপ লাইভ সিগন্যাল পাঠানোর লজিক (কোনো টাইম রেস্ট্রিকশন ছাড়াই সবসময় রান করবে)
            period_num = get_current_1min_period()
            if period_num != last_sent_period:
                pred_text = get_deep_ai_prediction()
                color_text = get_smart_trend_color(pred_text)
                
                msg = (
                    f"💎 <b>RAXI WIN DEEP 500+ AI PREDICTION</b> 💎\n\n"
                    f"🔹 <b>PERIOD:</b> {period_num}\n"
                    f"🎯 <b>PREDICTION:</b> {pred_text}\n"
                    f"🎨 <b>COLOR:</b> {color_text}\n"
                    f"📊 <b>STATUS:</b> ⏳ Waiting for result...\n"
                    f"───────────────────\n"
                    f"💡 <i>Analyzed from Deep 500+ Period Database</i>"
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
                
                print(f"Deep 500+ Signal Sent: {period_num} -> {pred_text}")
                last_sent_period = period_num

        except Exception as e:
            print(f"24/7 Loop Error: {e}")

        await asyncio.sleep(5)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    await app.initialize()
    await app.start()
    threading.Thread(target=run_web, daemon=True).start()
    print("Raxi Win 24/7 Bot is running with Deep Database & Timeout Prevention...")
    await send_auto_prediction_247(app)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot Stopped.")
                        
