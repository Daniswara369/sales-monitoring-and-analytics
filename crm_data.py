import pandas as pd
import random
from datetime import datetime

# Konfigurasi Surabaya Area
SALES_PERSONS = ["Sales_A", "Sales_B", "Sales_C"]
MIN_LAT, MAX_LAT = -7.34, -7.17
MIN_LON, MAX_LON = 112.63, 112.80

def generate_raw_data():
    data = []
    for sales_id in SALES_PERSONS:
        for i in range(1, 6): # 5 kunjungan per sales
            data.append({
                "Sales_ID": sales_id,
                "Store_Name": f"Toko_{sales_id}_{i}",
                "Lat": random.uniform(MIN_LAT, MAX_LAT),
                "Long": random.uniform(MIN_LON, MAX_LON),
                "Sample_Request": random.choice([True, False]),
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    df = pd.DataFrame(data)
    df.to_csv("raw_crm_data.csv", index=False)
    print("Successfully simulated CRM export: raw_crm_data.csv")

generate_raw_data()