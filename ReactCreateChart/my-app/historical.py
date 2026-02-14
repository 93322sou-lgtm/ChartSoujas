import requests
import time
import json
from datetime import datetime

SYMBOL = "BTCUSD"
RESOLUTION = "5m"
SECONDS = 300
MAX_CANDLES = 200
URL = "https://api.india.delta.exchange/v2/history/candles"

def wait_for_close():
    now = int(time.time())
    sleep = SECONDS - (now % SECONDS)
    time.sleep(sleep + 1)

def fetch_range(start, end):
    r = requests.get(URL, params={
        "symbol": SYMBOL,
        "resolution": RESOLUTION,
        "start": start,
        "end": end
    }, timeout=10)
    r.raise_for_status()
    return r.json()["result"]

# 1️⃣ Initial load — last 200 candles
end = int(time.time())
start = end - (MAX_CANDLES * SECONDS)
candles = fetch_range(start, end)

candles = candles[-MAX_CANDLES:]

with open("candles.json", "w") as f:
    json.dump({"result": candles}, f, indent=2)

print(f"📥 Loaded {len(candles)} candles")
print(candles)

# 2️⃣ Update on every new candle close
while True:
    wait_for_close()

    last_time = candles[-1]["time"]

    new_candles = fetch_range(last_time + SECONDS, int(time.time()))

    if new_candles:
        for c in new_candles:
            if c["time"] > last_time:
                candles.append(c)

        candles = candles[-MAX_CANDLES:]

        with open("candles.json", "w") as f:
            json.dump({"result": candles}, f, indent=2)

        print(
            f"✅ New candle @ "
            f"{datetime.utcfromtimestamp(candles[-1]['time'])} UTC | "
            f"Total: {len(candles)}"
        )
    else:
        print("⏳ No new candle yet")
