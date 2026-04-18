import pandas as pd
import requests
import polyline 
from datetime import datetime

KANTOR = (-7.2542405669271846, 112.7032013746073)

def get_real_route(coords):
    # Mengirim titik ke OSRM untuk mendapatkan rute jalan riil
    coords_str = ";".join([f"{lon},{lat}" for lat, lon in coords])
    url = f"http://router.project-osrm.org/route/v1/driving/{coords_str}?overview=full"
    r = requests.get(url)
    if r.status_code == 200:
        res = r.json()
        return res["routes"][0]["distance"], res["routes"][0]["geometry"]
    return 0, None

def run_pipeline():
    # 1. Load data mentah dari 'CRM'
    df = pd.read_csv("raw_crm_data.csv")
    final_report = []

    for sales_id in df['Sales_ID'].unique():
        sales_subset = df[df['Sales_ID'] == sales_id]
        
        # Susun rute: Kantor -> Toko 1..5 -> Kantor
        route_points = [KANTOR] + list(zip(sales_subset['Lat'], sales_subset['Long'])) + [KANTOR]
        
        # 2. Hitung Jarak Riil
        dist_m, geometry = get_real_route(route_points)
        total_km = dist_m / 1000
        
        # 3. Transformasi untuk Power BI (WKT Format)
        if geometry:
            decoded = polyline.decode(geometry)
            wkt_line = f"LINESTRING({', '.join([f'{c[1]} {c[0]}' for c in decoded])})"
        else:
            wkt_line = ""
        
        final_report.append({
            "Sales_ID": sales_id,
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Total_KM": round(total_km, 2),
            "Fuel_Cost": round((total_km / 12) * 13000, 2),
            "Store_Visited_Count": len(sales_subset),
            "Sample_Requests": sales_subset['Sample_Request'].sum(),
            "Route_Geometry": wkt_line
        })

    # 4. Simpan hasil akhir untuk Power BI
    pd.DataFrame(final_report).to_csv("monitoring_sales_surabaya.csv", index=False)
    print("Pipeline Selesai: monitoring_sales_surabaya.csv siap digunakan di Power BI")

run_pipeline()
