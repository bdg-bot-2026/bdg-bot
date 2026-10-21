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
    return "Bot status: ONLINE (Raxi Win Smart Live API & Auto-Win/Loss Active)"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

RAW_TOKEN = os.environ.get("BOT_TOKEN", "8937609482:AAEncEd0IY787haa0Pg1Azp2DHVT3Ulz1z14A")
TOKEN = RAW_TOKEN.strip()
CHANNEL_ID = "@RexiWinAIPrediction"

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

def get_api_history():
    global historical_db
    url = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            res_json = response.json()
            if 'data' in res_json and 'list' in res_json['data']:
                fetched_list = res_json['data']['list']
                for game in fetched_list:
                    issue = str(game['issueNumber'])
                    if not any(str(item['issueNumber']) == issue for item in historical_db):
                        historical_db.insert(0, game)
                if len(historical_db) > 200:
                    historical_db = historical_db[:200]
                return historical_db
    except Exception as e:
        print(f"API Fetch Error: {e}")
    return historical_db

# স্মার্ট ও ডাইনামিক প্রেডিকশন লজিক (একটানা একই সিগন্যাল আসা রোধ করতে রিভার্সাল ফিক্স)
def get_smart_ai_prediction():
    games_list = get_api_history()
    if not games_list or len(games_list) < 5:
        return random.choice(["BIG", "SMALL"])
    
    recent_results = []
    for i in range(min(20, len(games_list))):
        num = int(games_list[i]['number'])
        bs = "BIG" if num >= 5 else "SMALL"
        recent_results.append(bs)
    
    # যদি শেষ ৩টি একই ফলাফল হয়, তবে ট্রেন্ড ভেঙে বিপরীত সিগন্যাল দেবে
    if len(recent_results) >= 3 and recent_results[0] == recent_results[1] == recent_results[2]:
        return "SMALL" if recent_results[0] == "BIG" else "BIG"
    
    big_count = recent_results.count("BIG")
    small_count = recent_results.count("SMALL")
    
    if big_count >= small_count:
        return "SMALL"
    else:
        return "BIG"

def check_period_result(target_period):
    games_list = get_api_history()
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

async def send_auto_prediction(app):
    last_sent_period = ""
    pending_check_msg_id = None
    pending_period = ""
    pending_prediction = ""

    keyboard = [
        [InlineKeyboardButton("🎮 Play Raxi Win 🏆", url="https://raxiwin.com")],
        [InlineKeyboardButton("📊 Join VIP Channel", url="https://t.me/RexiWinAIPrediction")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    print("Raxi Win Live Smart Tracker Started Successfully...")

    while True:
        try:
            get_api_history()

            # আগের পিরিয়ডের রেজাল্ট চেক করে Win/Loss আপডেট করার লজিক
            if pending_check_msg_id and pending_period:
                actual_result = check_period_result(pending_period)
                if actual_result:
                    is_win = (actual_result == pending_prediction)
                    result_text = "✅ <b>WIN</b>" if is_win else "❌ <b>LOSS</b>"
                    color_text = get_smart_trend_color(pending_prediction)
                    
                    updated_msg = (
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

            period_num = get_current_1min_period()
            if period_num != last_sent_period:
                pred_text = get_smart_ai_prediction()
                color_text = get_smart_trend_color(pred_text)
                
                msg = (
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
                
                print(f"Signal Sent: {period_num} -> {pred_text}")
                last_sent_period = period_num

        except Exception as e:
            print(f"Loop Error: {e}")

        await asyncio.sleep(5)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    await app.initialize()
    await app.start()
    threading.Thread(target=run_web, daemon=True).start()
    print("Raxi Win Bot Live Tracker is Running...")
    await send_auto_prediction(app)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot Stopped.")
                
