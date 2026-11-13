import time
import requests
import sqlite3
from datetime import datetime, timezone
import pytz
import os
from flask import Flask
import threading

# ==========================================
# ⚙️ Configurations & Setup
# ==========================================
TOKEN = os.environ.get("TOKEN", "8937609482:AAFpxFnCk7ZI38QYnUNbUST2A6eZHnWuAHQ")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "@RexiWinAIPrediction")
DB_NAME = "raxi_master_final.db"

API_URL = "https://api.ar-lottery01.com/api/Energy/GetPanel?gameCode=WinGo_1M&language=en"
BEARER_TOKEN = os.environ.get("BEARER_TOKEN", "YOUR_BEARER_TOKEN_HERE")

# ==========================================
# 🌐 Flask Server for Render Port Binding
# ==========================================
app = Flask(__name__)

@app.route('/')
def home():
    return "Raxi Win AI Prediction Bot is Live and Running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ==========================================
# 🗄️ Database Initialization
# ==========================================
def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_history (
            period TEXT PRIMARY KEY,
            actual_result TEXT,
            prediction TEXT,
            strategy TEXT,
            status TEXT DEFAULT 'PENDING',
            created_at TEXT,
            result_time TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ==========================================
# 📨 Direct Telegram Sender with Logs
# ==========================================
def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": CHANNEL_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=payload, timeout=10)
        print("TELEGRAM STATUS:", response.status_code)
        print("TELEGRAM RESPONSE:", response.text)
    except Exception as e:
        print(f"Telegram Exception: {e}")

# ==========================================
# 🧠 Advanced Market Trend Evaluator
# ==========================================
def advanced_market_trend_evaluator():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT actual_result FROM game_history WHERE actual_result IN ('BIG', 'SMALL') ORDER BY rowid DESC LIMIT 100")
    rows = cursor.fetchall()
    conn.close()

    total_records = len(rows)
    print(f"Database Total Verified Records: {total_records}")
    
    if total_records < 3:
        return None, f"DATA_COLLECTION_ONLY ({total_records}/3 Records)"

    results = [row[0] for row in rows]
    votes = {"BIG": 0, "SMALL": 0}
    detected_trends = []

    dragon_count = 1
    for i in range(1, len(results)):
        if results[i] == results[0]:
            dragon_count += 1
        else:
            break
            
    if dragon_count >= 4:
        reversal_target = "SMALL" if results[0] == "BIG" else "BIG"
        votes[reversal_target] += 3.5
        detected_trends.append(f"Dragon_Break({dragon_count}x {results[0]})")

    is_zigzag = True
    for i in range(min(5, len(results) - 1)):
        if results[i] == results[i+1]:
            is_zigzag = False
            break
            
    if is_zigzag:
        next_zigzag = "SMALL" if results[0] == "BIG" else "BIG"
        votes[next_zigzag] += 3.0
        detected_trends.append("ZigZag_Alternate")

    if len(results) >= 4:
        if results[0] == results[1] and results[2] == results[3] and results[0] != results[2]:
            t22_target = "SMALL" if results[0] == "BIG" else "BIG"
            votes[t22_target] += 2.5
            detected_trends.append("TwoByTwo_Zone")

    total_big = results.count('BIG')
    total_small = results.count('SMALL')
    big_pct = round((total_big / total_records) * 100, 2)
    
    if big_pct > 58:
        votes["SMALL"] += 2.0
        detected_trends.append(f"Freq_Overbought(Big {big_pct}%)")
    elif big_pct < 42:
        votes["BIG"] += 2.0
        detected_trends.append(f"Freq_Oversold(Big {big_pct}%)")

    if not detected_trends:
        fallback = "SMALL" if total_big >= total_small else "BIG"
        votes[fallback] += 1.0
        detected_trends.append("General_Frequency_Balance")

    final_prediction = max(votes, key=votes.get)
    combined_strategy = " + ".join(detected_trends)

    return final_prediction, combined_strategy

# ==========================================
# 🚀 Execution & Main Bot Loop
# ==========================================
def run_master_bot():
    print("🚀 Raxi Win Advanced Trend Analysis Bot Started (Debug Mode)...")
    active_period = ""

    while True:
        try:
            headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
            print("API REQUEST STARTED")
            response = requests.get(API_URL, headers=headers, timeout=15)
            
            print("API STATUS:", response.status_code)
            print("API RESPONSE TIME:", response.elapsed.total_seconds())
            print("API RESPONSE:", response.text[:1000])

            if response.status_code == 200:
                payload = response.json()
                api_period = payload.get("period")
                actual_result = payload.get("result") 
                
                if api_period and api_period != active_period:
                    timestamp_str = datetime.now(timezone.utc).isoformat()

                    if actual_result and active_period:
                        conn = sqlite3.connect(DB_NAME)
                        cursor = conn.cursor()
                        cursor.execute("SELECT prediction FROM game_history WHERE period = ?", (active_period,))
                        row = cursor.fetchone()
                        
                        if row:
                            predicted_val = row[0]
                            if predicted_val:
                                match_status = "WIN" if predicted_val == actual_result else "LOSS"
                                cursor.execute(
                                    "UPDATE game_history SET actual_result = ?, status = ?, result_time = ? WHERE period = ?", 
                                    (actual_result, match_status, timestamp_str, active_period)
                                )
                                conn.commit()
                                
                                result_msg = (
                                    f"📊 <b>TREND PERFORMANCE UPDATE</b>\n\n"
                                    f"🔹 <b>Period:</b> {active_period}\n"
                                    f"🎯 <b>Prediction:</b> {predicted_val} | 🟢 <b>Actual:</b> {actual_result}\n"
                                    f"Status: {'✅ WIN' if match_status == 'WIN' else '❌ LOSS'}"
                                )
                                send_telegram(result_msg)
                            else:
                                cursor.execute(
                                    "UPDATE game_history SET actual_result = ?, result_time = ? WHERE period = ?", 
                                    (actual_result, timestamp_str, active_period)
                                )
                                conn.commit()
                        else:
                            cursor.execute(
                                "INSERT OR IGNORE INTO game_history (period, actual_result, status, created_at) VALUES (?, ?, 'SKIPPED', ?)",
                                (active_period, actual_result, timestamp_str)
                            )
                            conn.commit()
                        conn.close()

                    next_prediction, chosen_strategy = advanced_market_trend_evaluator()

                    conn = sqlite3.connect(DB_NAME)
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT OR IGNORE INTO game_history (period, prediction, strategy, created_at) VALUES (?, ?, ?, ?)",
                        (api_period, next_prediction, chosen_strategy, timestamp_str)
                    )
                    conn.commit()
                    conn.close()

                    if next_prediction:
                        signal_msg = (
                            f"💎 <b>RAXI WIN TREND AI SIGNAL</b> 💎\n\n"
                            f"🔹 <b>PERIOD:</b> {api_period}\n"
                            f"🎯 <b>PREDICTION:</b> <b>{next_prediction}</b>\n"
                            f"📈 <b>ACTIVE MARKET TREND:</b> {chosen_strategy}"
                        )
                        send_telegram(signal_msg)
                    else:
                        print(f"Period {api_period}: Collecting historical data -> {chosen_strategy}")

                    active_period = api_period

        except Exception as e:
            print(f"Runtime Exception: {e}")

        time.sleep(10)

if __name__ == "__main__":
    web_thread = threading.Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()

    run_master_bot()
