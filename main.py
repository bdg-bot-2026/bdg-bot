import os
import random
from datetime import datetime
import pytz
import asyncio
import threading
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler

# Render Port Scan ইস্যু সমাধানের জন্য ডামি ওয়েব সার্ভার
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

TOKEN = "8752459278:AAGojryTHduibUpZaToGzSdmAJI_D6EwJIK"
CHANNEL_ID = "@bdgplayvipwin"

def get_current_30s_period():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    total_seconds = (now.hour * 3600) + (now.minute * 60) + now.second
    interval_index = (total_seconds // 30) + 1
    date_str = now.strftime('%Y%m%d')
    return f"{date_str}1000{interval_index:04d}"

async def send_auto_prediction(app):
    await asyncio.sleep(5)  # বট স্টার্ট হওয়ার জন্য ৫ সেকেন্ড ওয়েট
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
            
            await app.bot.send_message(
                chat_id=CHANNEL_ID, 
                text=msg, 
                parse_mode="Markdown", 
                reply_markup=reply_markup
            )
        except Exception as e:
            print(f"Error in auto send: {e}")
            
        await asyncio.sleep(30)

async def predict_command(update, context):
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
    await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=reply_markup)

async def post_init(app):
    asyncio.create_task(send_auto_prediction(app))

def main():
    threading.Thread(target=run_web, daemon=True).start()
    
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("predict", predict_command))
    
    print("Bot is starting...")
    app.run_polling()

if __name__ == '__main__':
    main()
    
