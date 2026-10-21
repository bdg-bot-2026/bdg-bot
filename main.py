import os
import random
from datetime import datetime
import pytz
import asyncio
import threading
import time
import requests
from flask import Flask
from telegram.ext import ApplicationBuilder
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot status: ONLINE (Raxi Win Cookie Session Active)"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

RAW_TOKEN = os.environ.get("BOT_TOKEN", "8937609482:AAEncEd0IY787haa0Pg1Azp2DHVT3Ulz1z14A")
TOKEN = RAW_TOKEN.strip()
CHANNEL_ID = "@RexiWinAIPrediction"

def get_current_1min_period():
    now_utc = datetime.now(pytz.utc)
    date_str = now_utc.strftime("%Y%m%d")
    total_minutes_utc = (now_utc.hour * 60) + now_utc.minute
    period_count = 10000 + total_minutes_utc + 1
    return f"{date_str}1000{period_count}"

def get_api_history():
    current_time = int(time.time())
    random_num = random.randint(100000000000, 999999999999)
    
    url = f"https://api.ar-lottery01.com/api/Energy/GetPanel?gameCode=WinGo_1M&language=en&random={random_num}&signature=049C9345B6688083A6A25F71250CA2AD&timestamp={current_time}"
    
    # এখানে আপনার ব্রাউজার থেকে পাওয়া আসল কুকিজ এবং হেডার বসাতে হবে যাতে সেশন ভ্যালিড থাকে
    headers = {
        "Host": "api.ar-lottery01.com",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://raxiwin.com",
        "Referer": "https://raxiwin.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        # "Cookie": "YOUR_ACTUAL_BROWSER_COOKIES_HERE"  <- ব্রাউজার থেকে লগইন থাকা অবস্থায় কুকিজ কপি করে এখানে বসাতে পারেন
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            res_json = response.json()
            if 'data' in res_json:
                data = res_json['data']
                if isinstance(data, dict):
                    if 'snapshot' in data and isinstance(data['snapshot'], dict):
                        snap = data['snapshot']
                        if 'list' in snap and isinstance(snap['list'], list):
                            return snap['list']
                    for key in ['list', 'history', 'games', 'items']:
                        if key in data and isinstance(data[key], list):
                            return data[key]
                elif isinstance(data, list):
                    return data
    except Exception as e:
        print(f"API Fetch Error: {e}")
    return []

def get_high_tech_ai_prediction():
    games_list = get_api_history()
    if not games_list:
        return "BIG"
    recent_results = []
    for item in games_list:
        try:
            num_val = item.get('number') or item.get('num')
            if num_val is not None:
                num = int(num_val)
                bs = "BIG" if num >= 5 else "SMALL"
                recent_results.append(bs)
        except Exception:
            continue
    
    if not recent_results:
        return "BIG"

    big_count = recent_results.count("BIG")
    small_count = recent_results.count("SMALL")
    
    if big_count >= small_count:
        return "SMALL"
    else:
        return "BIG"

def check_period_result(target_period):
    games_list = get_api_history()
    for game in games_list:
        issue_number = str(game.get('issueNumber') or game.get('period') or game.get('issue') or '')
        if issue_number == str(target_period):
            try:
                num_val = game.get('number') or game.get('num')
                if num_val is not None:
                    num = int(num_val)
                    actual_bs = "BIG" if num >= 5 else "SMALL"
                    return actual_bs
            except Exception:
                pass
    return None

def get_smart_trend_color(pred_text):
    if pred_text == "BIG":
        return "GREEN 🟢"
    else:
        return "RED 🔴"

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

    print("Raxi Win Cookie-Session Automation Loop started...")

    while True:
        try:
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
                
                print(f"Signal Sent: {period_num} -> {pred_text}")
                last_sent_period = period_num

        except Exception as e:
            print(f"Loop Error: {e}")

        await asyncio.sleep(3)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    await app.initialize()
    await app.start()
    threading.Thread(target=run_web, daemon=True).start()
    print("Raxi Win Cookie Session Bot is running...")
    await send_auto_prediction(app)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot Stopped.")
    
