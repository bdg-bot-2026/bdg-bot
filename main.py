import os
import random
from datetime import datetime
import pytz
import asyncio
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder

# Web server for Render
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is running perfectly!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

# 🔴 আপনার নতুন Token ও Channel ID
TOKEN = "8752459278:AAGk160ZREsFuDUk0Hp45cz4MiF6TFv27Is"
CHANNEL_ID = "@bdgplayvipwin"

def get_current_30s_period():
    try:
        ist = pytz.timezone('Asia/Kolkata')
        now = datetime.now(ist)
    except Exception:
        now = datetime.utcnow()
        
    total_seconds = (now.hour * 3600) + (now.minute * 60) + now.second
    interval_index = (total_seconds // 30) + 1
    date_str = now.strftime('%Y%m%d')
    return f"{date_str}1000{interval_index:04d}"

async def send_auto_prediction(app):
    await asyncio.sleep(5)
    while True:
        try:
            period_num = get_current_30s_period()
            
            prediction_type = random.choice(["SMALL 🔴", "BIG 🟢"])
            result_type = random.choice(["✅ WIN", "❌ LOSS"])
            
            msg = (
                f"🏆 BDG WIN 30 SEC 🏆\n\n"
                f"🔷 PERIOD: {period_num}\n"
                f"🎯 PREDICTION: {prediction_type}\n"
                f"📊 RESULT: {result_type}"
            )
            
            await app.bot.send_message(
                chat_id=CHANNEL_ID, 
                text=msg
            )
            print(f"Message sent for period {period_num}")
            
        except Exception as e:
            print(f"Error sending auto message: {e}")
            
        # প্রতি ৩০ সেকেন্ড পর পর মেসেজ পাঠাবে
        await asyncio.sleep(30)

async def post_init(app):
    asyncio.create_task(send_auto_prediction(app))

def main():
    threading.Thread(target=run_web, daemon=True).start()
    
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    print("Starting bot polling...")
    app.run_polling()

if __name__ == '__main__':
    main()
    
