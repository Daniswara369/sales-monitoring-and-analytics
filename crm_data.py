import pandas as pd
import random
import uuid
from datetime import datetime, timedelta

# Konfigurasi Surabaya Area
SALES_PERSONS = ["Sales_A", "Sales_B", "Sales_C"]
MIN_LAT, MAX_LAT = -7.34, -7.17
MIN_LON, MAX_LON = 112.63, 112.80

# A curated list of 20 unique store icons from Wikimedia Commons in upload.wikimedia format
STORE_ICONS = [
    "https://upload.wikimedia.org/wikipedia/commons/e/ee/Shop.svg",
    "https://upload.wikimedia.org/wikipedia/commons/3/3d/Map-icon-shop.svg",
    "https://upload.wikimedia.org/wikipedia/commons/c/c8/Store_Building_Flat_Icon_Vector.svg",
    "https://upload.wikimedia.org/wikipedia/commons/f/f6/Wikivoyage-icon-supermarket.svg",
    "https://upload.wikimedia.org/wikipedia/commons/d/dc/Font_Awesome_5_solid_store.svg",
    "https://upload.wikimedia.org/wikipedia/commons/e/ee/Font_Awesome_5_solid_store-alt.svg",
    "https://upload.wikimedia.org/wikipedia/commons/e/e0/Iconoir_shop.svg",
    "https://upload.wikimedia.org/wikipedia/commons/d/da/Iconoir_shop-alt.svg",
    "https://upload.wikimedia.org/wikipedia/commons/2/23/Iconoir_small-shop-alt.svg",
    "https://upload.wikimedia.org/wikipedia/commons/5/5f/Icons8_flat_shop.svg",
    "https://upload.wikimedia.org/wikipedia/commons/e/ee/Linearicons_store.svg",
    "https://upload.wikimedia.org/wikipedia/commons/4/4c/Linecons_groceries-store.svg",
    "https://upload.wikimedia.org/wikipedia/commons/1/18/Emojione_1F3EC.svg",
    "https://upload.wikimedia.org/wikipedia/commons/0/02/Emojione_BW_1F3EC.svg",
    "https://upload.wikimedia.org/wikipedia/commons/5/55/Ic_store_48px.svg",
    "https://upload.wikimedia.org/wikipedia/commons/2/22/Store_clip_art.svg",
    "https://upload.wikimedia.org/wikipedia/commons/a/a2/Shop_%281156435%29_-_The_Noun_Project.svg",
    "https://upload.wikimedia.org/wikipedia/commons/8/86/Shop_%2850373%29_-_The_Noun_Project.svg",
    "https://upload.wikimedia.org/wikipedia/commons/e/ec/Two_cellar_loom_shops.svg",
    "https://upload.wikimedia.org/wikipedia/commons/7/76/Side_loomshop.svg"
]

VISIT_TYPES = ["Routine Restock", "New Prospecting", "Complaint Follow-up", "Urgent Delivery", "Market Survey"]

def generate_raw_data():
    data = []
    # Start work at 8 AM today
    base_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    
    icon_index = 0
    
    for sales_id in SALES_PERSONS:
        current_time = base_time
        num_visits = random.randint(5, 6) # 5-6 visits per person
        
        for i in range(1, num_visits + 1):
            current_time += timedelta(hours=random.randint(1, 2), minutes=random.randint(0, 59))
            
            items_sold = random.randint(0, 100)
            revenue = items_sold * random.randint(25000, 200000)
            
            # Select a unique icon for each store using the index loop
            store_icon = STORE_ICONS[icon_index % len(STORE_ICONS)]
            icon_index += 1
            
            data.append({
                "Activity_ID": f"ACT-{uuid.uuid4().hex[:8].upper()}",
                "Sales_ID": sales_id,
                "Store_Name": f"Toko_{sales_id}_{i}",
                "Lat": random.uniform(MIN_LAT, MAX_LAT),
                "Long": random.uniform(MIN_LON, MAX_LON),
                "Visit_Type": random.choice(VISIT_TYPES),
                "Items_Sold": items_sold,
                "Revenue_IDR": revenue,
                "Sample_Request": random.choice([True, False]),
                "Store_Image_URL": store_icon,
                "Timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
    df = pd.DataFrame(data)
    df.to_csv("raw_crm_data.csv", index=False)
    print(f"Successfully generated unique-mapped dataset: raw_crm_data.csv ({len(df)} activities)")

if __name__ == "__main__":
    generate_raw_data()
