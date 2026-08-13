import asyncio
import datetime
import os
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from telegram import Bot

# ১. আপনার আসল বট টোকেনটি এখানে বসাবেন
BOT_TOKEN = "8752459278:AAEFYk3jP1FOT-G3k3JgBwWwkzOIUnroGgg"

# ২. আপনার চ্যানেলের ইউজারনেম
CHANNEL_ID = "@bdgplayvipwin"

bot = Bot(token=BOT_TOKEN)
base_period_count = 52174


# Render সার্ভার চালু রাখার জন্য
class HealthCheckHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active!")


def run_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()


def get_bdg_period_id(counter):
    today = datetime.datetime.now().strftime("%Y%m%d")
    return f"{today}1000{counter}"


async def main():
    global base_period_count
    print("Bot is starting...")

    while True:
        period_id = get_bdg_period_id(base_period_count)
        my_prediction = random.choice(["BIG 🟢", "SMALL 🔴"])

        init_message = (
            f"🏆 **BDG WIN 30 SEC** 🏆\n\n"
            f"🔹 **PERIOD:** `{period_id}`\n"
            f"🎯 **PREDICTION:** **{my_prediction}**\n"
            f"📊 **RESULT:** ⏳ *Waiting...*"
        )

        try:
            sent_msg = await bot.send_message(
                chat_id=CHANNEL_ID, text=init_message, parse_mode="Markdown"
            )
            await asyncio.sleep(30)

            is_win = random.choice([True, False])
            status = "✅ WIN" if is_win else "❌ LOSS"

            final_message = (
                f"🏆 **BDG WIN 30 SEC** 🏆\n\n"
                f"🔹 **PERIOD:** `{period_id}`\n"
                f"🎯 **PREDICTION:** **{my_prediction}**\n"
                f"📊 **RESULT:** **{status}**"
            )

            await bot.edit_message_text(
                chat_id=CHANNEL_ID,
                message_id=sent_msg.message_id,
                text=final_message,
                parse_mode="Markdown",
            )

            base_period_count += 1
            await asyncio.sleep(2)

        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(5)


if __name__ == "__main__":
    threading.Thread(target=run_health_server, daemon=True).start()
    asyncio.run(main())
  
