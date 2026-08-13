import os
import random
from datetime import datetime
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8752459278:AAEFYk3jP1FOT-G3k3JgBwWwkzOIUnroGgg"

user_data = {}

def get_current_30s_period():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    total_seconds = (now.hour * 3600) + (now.minute * 60) + now.second
    interval_index = (total_seconds // 30) + 1
    date_str = now.strftime('%Y%m%d')
    period_number = f"{date_str}1000{interval_index:04d}"
    return period_number

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("predict", predict))
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
