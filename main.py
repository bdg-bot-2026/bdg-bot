import os
import random
from datetime import datetime
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8752459278:AAEFYk3jP1FOT-G3k3"


user_data = {}

def get_current_30s_period():
    # IST Timezone (India/Bangladesh alignment)
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    
    # Calculate 30-second interval index for the day
    total_seconds = (now.hour * 3600) + (now.minute * 60) + now.second
    period_index = (total_seconds // 30) + 1  # Started from 1
    
    date_str = now.strftime("%Y%m%d")
    # BDG WIN 30s format
    return f"{date_str}10005{period_index:04d}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "👋 **BDG WIN 30s Auto-Period Bot!**\n\n"
        "👉 **ব্যবহারের নিয়ম:**\n"
        "শুধু লিখুন `/predict` — বট বর্তমান সময় অনুযায়ী লাইভ পিরিয়ড নম্বর ও প্রেডিকশন দিয়ে দেবে!"
    )
    await update.message.reply_markdown(msg)

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    # Auto generate period number based on current time
    current_period = get_current_30s_period()
    prediction = random.choice(["BIG", "SMALL"])
    
    user_data[chat_id] = {'period': current_period, 'prediction': prediction}
    
    emoji = "🟢" if prediction == "BIG" else "🔴"
    
    keyboard = [
        [
            InlineKeyboardButton("Result was BIG 🟢", callback_data="WIN_BIG"),
            InlineKeyboardButton("Result was SMALL 🔴", callback_data="WIN_SMALL")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    msg = (
        f"🎮 **BDG WIN 30-SEC PREDICTION**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 **Period:** `{current_period}` *(Auto Generated)*\n"
        f"🎯 **Prediction:** **{prediction} {emoji}**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⏳ *৩০ সেকেন্ড পর গেমে আসল রেজাল্ট কী এলো বাটনে চাপ দিন:* "
    )
    
    await update.message.reply_markdown(msg, reply_markup=reply_markup)

async def handle_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat.id
    actual_result = "BIG" if query.data == "WIN_BIG" else "SMALL"
    
    if chat_id not in user_data:
        await query.edit_message_text("❌ কোনো সক্রিয় প্রেডিকশন পাওয়া যায়নি! আবার `/predict` করুন।")
        return

    saved_info = user_data[chat_id]
    predicted = saved_info['prediction']
    
    status_msg = f"🎉 **RESULT: WIN!** ✅" if actual_result == predicted else f"❌ **RESULT: LOSS!** 💔"

    final_text = (
        f"🎮 **BDG WIN 30-SEC RESULT**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 **Period:** `{saved_info['period']}`\n"
        f"{status_msg}\n"
        f"(বটের প্রেডিকশন: {predicted}, আসল রেজাল্ট: {actual_result})\n\n"
        f"🚀 পরবর্তী পিরিয়ডের জন্য আবার `/predict` লিখুন!"
    )
    
    await query.edit_message_text(text=final_text, parse_mode='Markdown')

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("predict", predict))
    app.add_handler(CallbackQueryHandler(handle_result))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
