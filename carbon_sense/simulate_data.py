# simulate_data.py
import pandas as pd
import random
import time
from datetime import datetime, timedelta

DATA_FILE = "data/energy.csv"

def generate_energy_value():
    # Random value between 1.0 and 3.0 kWh
    return round(random.uniform(1.0, 3.0), 2)

def append_new_data():
    try:
        df = pd.read_csv(DATA_FILE)
        last_time = pd.to_datetime(df['timestamp'].iloc[-1])
    except:
        # Start from now if file doesn't exist
        last_time = datetime.now() - timedelta(hours=1)
        df = pd.DataFrame(columns=["timestamp", "energy_kwh"])

    new_time = last_time + timedelta(hours=1)
    new_value = generate_energy_value()

    new_row = pd.DataFrame({
        "timestamp": [new_time.strftime('%Y-%m-%d %H:%M:%S')],
        "energy_kwh": [new_value]
    })

    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    print(f"[+] Added new data: {new_row.iloc[0].to_dict()}")

# Keep appending data every minute
if __name__ == "__main__":
    while True:
        append_new_data()
        time.sleep(60)  # Wait 60 seconds
