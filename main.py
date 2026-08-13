import os
import random
from datetime import datetime
import pytz
import asyncio
import threading
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder

# Render Port Scanning সমস্যার সমাধানের জন্য ডামি ওয়েব সার্ভার
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is active and running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

# 🔴 আপনার তথ্যসমূহ
TOKEN = "8752459278:AAGojryTHduibUpZaToGzSdmAJI_D6EwJIK"
CHANNEL_ID = "@bdgplayvipwin" 

def get_current_30s_period():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    total_seconds = (now.hour * 3600) + (now.minute * 60) + now.second
    interval_index = (total_seconds // 30) + 1
    date_str = now.strftime('%Y%m%d')
    period_number = f"{date_str}1000{interval_index:04d}"
    return period_number

async def send_auto_prediction(app):
    while True:
        try:
            period_num = get_current_30s_period()
            prediction = random.choice(["BIG", "SMALL"])
            
            msg = (
                f"🎯 **BDG VIP PREDICTION 30s** 🎯\n\n"
                f"📍 **Period:** `{period_num}`\n"
                f"📊 **Prediction:** **{prediction}**\n\n"
                f"👇 *Select result below:* "
            )
            
            keyboard = [
                [
                    InlineKeyboardButton("✅ WIN", callback_data="win"),
                    InlineKeyboardButton("❌ LOSS", callback_data="loss")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # চ্যানেলে অটোমেটিক মেসেজ পাঠাবে
            await app.bot.send_message(
                chat_id=CHANNEL_ID, 
                text=msg, 
                parse_mode="Markdown", 
                reply_markup=reply_markup
            )
            
        except Exception as e:
            print(f"Error sending message: {e}")
            
        # ⏱️ প্রতি ৩০ সেকেন্ড পর পর মেসেজ পাঠাবে
        await asyncio.sleep(30)

async def post_init(app):
    # ব্যাকগ্রাউন্ডে অটোমেটিক মেসেজ লুপ চালু হবে
    asyncio.create_task(send_auto_prediction(app))

def main():
    threading.Thread(target=run_web, daemon=True).start()
    
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
