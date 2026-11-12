import time
import requests
import sqlite3
import asyncio
from datetime import datetime, timezone
import pytz
from telegram import Bot

# ==========================================
# ⚙️ Configurations & Setup
# ==========================================
TOKEN = "8937609482:AAFpxFnCk7ZI38QYnUNbUST2A6eZHnWuAHQ"
CHANNEL_ID = "@RexiWinAIPrediction"
DB_NAME = "raxi_master_final.db"

bot = Bot(token=TOKEN)
API_URL = "https://api.ar-lottery01.com/api/Energy/GetPanel?gameCode=WinGo_1M&language=en"
BEARER_TOKEN = "YOUR_BEARER_TOKEN_HERE"  # আপনার আসল টোকেন এখানে বসাবেন

# স্থায়ী Async Event Loop তৈরি
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

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
# 🕒 Time & Period Generator
# ==========================================
def get_current_1min_period():
    try:
        bd_tz = pytz.timezone('Asia/Dhaka')
        now_bd = datetime.now(bd_tz)
        date_str = now_bd.strftime("%Y%m%d")
        total_minutes = (now_bd.hour * 60) + now_bd.minute
        period_count = 10000 + total_minutes + 1
        return f"{date_str}1000{period_count}"
    except Exception:
        now_utc = datetime.now(timezone.utc)
        date_str = now_utc.strftime("%Y%m%d")
        total_minutes_utc = (now_utc.hour * 60) + now_utc.minute
        period_count = 10000 + total_minutes_utc + 1
        return f"{date_str}1000{period_count}"

# ==========================================
# 🧠 Advanced Market Trend & Statistical Evaluator
# ==========================================
def advanced_market_trend_evaluator():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # শুধুমাত্র যাচাইকৃত ফলাফলগুলো নিয়ে বিশ্লেষণ (সর্বোচ্চ ১০০ রাউন্ড)
    cursor.execute("SELECT actual_result FROM game_history WHERE actual_result IN ('BIG', 'SMALL') ORDER BY rowid DESC LIMIT 100")
    rows = cursor.fetchall()
    conn.close()

    total_records = len(rows)
    
    # ডেটা কালেকশন মোড: পর্যাপ্ত ডেটা (অন্তত ২০টি রেকর্ড) না হলে প্রেডিকশন দেবে না, শুধু ডেটা জমাবে
    if total_records < 20:
        return None, f"DATA_COLLECTION_ONLY ({total_records}/20 Records)"

    results = [row[0] for row in rows] # results[0] হলো সবচেয়ে সাম্প্রতিক ফলাফল
    
    votes = {"BIG": 0, "SMALL": 0}
    detected_trends = []

    # ১. DRAGON TREND DETECTION (টানা ৪ বা তার বেশি একই ফল আসলে তা ট্র্যাক করা)
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

    # ২. ZIGZAG / ALTERNATE CLUSTER DETECTION (বিকল্প ফলাফল আসা যেমন: BIG, SMALL, BIG, SMALL)
    is_zigzag = True
    for i in range(min(5, len(results) - 1)):
        if results[i] == results[i+1]:
            is_zigzag = False
            break
            
    if is_zigzag:
        next_zigzag = "SMALL" if results[0] == "BIG" else "BIG"
        votes[next_zigzag] += 3.0
        detected_trends.append("ZigZag_Alternate")

    # ৩. TWO BY TWO ZONE DETECTION (যেমন: BIG, BIG, SMALL, SMALL)
    if len(results) >= 4:
        if results[0] == results[1] and results[2] == results[3] and results[0] != results[2]:
            t22_target = "SMALL" if results[0] == "BIG" else "BIG"
            votes[t22_target] += 2.5
            detected_trends.append("TwoByTwo_Zone")

    # ৪. FREQUENCY BALANCING (সামগ্রিক ফ্রিকোয়েন্সি ও পার্সেন্টেজ চেক)
    total_big = results.count('BIG')
    total_small = results.count('SMALL')
    big_pct = round((total_big / total_records) * 100, 2)
    
    if big_pct > 58:
        votes["SMALL"] += 2.0
        detected_trends.append(f"Freq_Overbought(Big {big_pct}%)")
    elif big_pct < 42:
        votes["BIG"] += 2.0
        detected_trends.append(f"Freq_Oversold(Big {big_pct}%)")

    # যদি স্পেশাল কোনো ট্রেন্ড সক্রিয় না থাকে, তবে জেনারেল ফ্রিকোয়েন্সি ব্যালেন্স কাজ করবে
    if not detected_trends:
        fallback = "SMALL" if total_big >= total_small else "BIG"
        votes[fallback] += 1.0
        detected_trends.append("General_Frequency_Balance")

    # সর্বোচ্চ ভোটপ্রাপ্ত প্রেডিকশন নির্বাচন
    final_prediction = max(votes, key=votes.get)
    combined_strategy = " + ".join(detected_trends)

    return final_prediction, combined_strategy

def get_performance_stats():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM game_history WHERE status IN ('WIN', 'LOSS')")
    completed = cursor.fetchone()[0]
    if completed == 0:
        return 0.0, 0, 0
    cursor.execute("SELECT COUNT(*) FROM game_history WHERE status = 'WIN'")
    wins = cursor.fetchone()[0]
    conn.close()
    accuracy = round((wins / completed) * 100, 2)
    return accuracy, wins, completed

# ==========================================
# 🚀 Execution & Telegram Loop
# ==========================================
async def send_telegram(message):
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="HTML")
    except Exception as e:
        print(f"Telegram Error: {e}")

def run_master_bot():
    print("🚀 Raxi Win Advanced Trend Analysis Bot Started...")
    active_period = ""

    while True:
        try:
            headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
            response = requests.get(API_URL, headers=headers, timeout=10)
            
            if response.status_code == 200:
                payload = response.json()
                
                # পিরিয়ড মিসম্যাচ রোধ করতে API থেকে আসা পিরিয়ড নিশ্চিত করা
                api_period = payload.get("period")
                actual_result = payload.get("result") 
                
                if api_period and api_period != active_period:
                    timestamp_str = datetime.now(timezone.utc).isoformat()

                    # ১. আগের রাউন্ডের ফলাফল যাচাই ও উইন/লস আপডেট
                    if actual_result and active_period:
                        conn = sqlite3.connect(DB_NAME)
                        cursor = conn.cursor()
                        cursor.execute("SELECT prediction FROM game_history WHERE period = ?", (active_period,))
                        row = cursor.fetchone()
                        
                        if row:
                            predicted_val = row[0]
                            if predicted_val:  # যদি ভ্যালিড প্রেডিকশন থাকে তবেই উইন/লস হিসাব করবে
                                match_status = "WIN" if predicted_val == actual_result else "LOSS"
                                cursor.execute(
                                    "UPDATE game_history SET actual_result = ?, status = ?, result_time = ? WHERE period = ?", 
                                    (actual_result, match_status, timestamp_str, active_period)
                                )
                                conn.commit()
                                
                                # একুরেসি হিসাব
                                acc, wins, total = get_performance_stats()
                                result_msg = (
                                    f"📊 <b>TREND PERFORMANCE UPDATE</b>\n\n"
                                    f"🔹 <b>Period:</b> {active_period}\n"
                                    f"🎯 <b>Prediction:</b> {predicted_val} | 🟢 <b>Actual:</b> {actual_result}\n"
                                    f"Status: {'✅ WIN' if match_status == 'WIN' else '❌ LOSS'}\n\n"
                                    f"📈 <b>Model Accuracy:</b> {acc}% ({wins}/{total} Wins)"
                                )
                                loop.run_until_complete(send_telegram(result_msg))
                            else:
                                # ডেটা কালেকশন মোডে প্রেডিকশন None থাকলেও আসল ফলাফল সেভ করে রাখা হবে
                                cursor.execute(
                                    "UPDATE game_history SET actual_result = ?, result_time = ? WHERE period = ?", 
                                    (actual_result, timestamp_str, active_period)
                                )
                                conn.commit()
                        else:
                            # যদি আগের পিরিয়ড ডেটাবেসে না থাকে, তবে নতুন এন্ট্রি হিসেবে সেভ হবে
                            cursor.execute(
                                "INSERT OR IGNORE INTO game_history (period, actual_result, status, created_at) VALUES (?, ?, 'SKIPPED', ?)",
                                (active_period, actual_result, timestamp_str)
                            )
                            conn.commit()
                        conn.close()

                    # ২. অ্যাডভান্সড ট্রেন্ড এভালুয়েটর রান করা
                    next_prediction, chosen_strategy = advanced_market_trend_evaluator()

                    # ৩. ডেটাবেসে পিরিয়ড ও প্রেডিকশন সেভ করা
                    conn = sqlite3.connect(DB_NAME)
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT OR IGNORE INTO game_history (period, prediction, strategy, created_at) VALUES (?, ?, ?, ?)",
                        (api_period, next_prediction, chosen_strategy, timestamp_str)
                    )
                    conn.commit()
                    conn.close()

                    # ৪. টেলিগ্রামে সিগন্যাল পাঠানো (যদি প্রেডিকশন এভেইলেবল থাকে)
                    if next_prediction:
                        signal_msg = (
                            f"💎 <b>RAXI WIN TREND AI SIGNAL</b> 💎\n\n"
                            f"🔹 <b>PERIOD:</b> {api_period}\n`"
                            f"🎯 <b>PREDICTION:</b> <b>{next_prediction}</b>\n"
                            f"📈 <b>ACTIVE MARKET TREND:</b> {chosen_strategy}"
                        )
                        loop.run_until_complete(send_telegram(signal_msg))
                    else:
                        print(f"Period {api_period}: Collecting historical data -> {chosen_strategy}")

                    active_period = api_period

        except Exception as e:
            print(f"Runtime Exception: {e}")

        time.sleep(10)

if __name__ == "__main__":
    run_master_bot()
    
