# 🏗️ Power BI Dashboard Build Guide — Complete Manual Setup
## Sales Monitoring & Geospatial Analytics — Surabaya

> **No MCP required.** This is a 100% manual guide for Power BI Desktop.
> Follow each step in exact order. All DAX formulas are copy-paste ready.

---

## STEP 1: Import Data

1. Open **Power BI Desktop**
2. Click **Home → Get Data → Text/CSV**
3. Navigate to `e:\Project ML AI\sales-monitoring-and-analytics\`
4. Import **`raw_crm_data.csv`** → Click **Load**
5. Repeat: **Get Data → Text/CSV** → Import **`monitoring_sales_surabaya.csv`** → Click **Load**

---

## STEP 2: Fix Data Types (Power Query Editor)

Go to **Home → Transform Data** to open Power Query Editor.

### Table: `raw_crm_data`
| Column | Change To |
|:--|:--|
| `Activity_ID` | Text |
| `Sales_ID` | Text |
| `Store_Name` | Text |
| `Lat` | Decimal Number |
| `Long` | Decimal Number |
| `Visit_Type` | Text |
| `Items_Sold` | Whole Number |
| `Revenue_IDR` | Whole Number |
| `Sample_Request` | True/False |
| `Store_Image_URL` | Text |
| `Timestamp` | Date/Time |

### Table: `monitoring_sales_surabaya`
| Column | Change To |
|:--|:--|
| `Sales_ID` | Text |
| `Date` | Date |
| `Total_KM` | Decimal Number |
| `Fuel_Cost` | Decimal Number |
| `Store_Visited_Count` | Whole Number |
| `Sample_Requests` | Whole Number |
| `Route_Geometry` | Text |

Click **Close & Apply**.

---

## STEP 3: Set Data Categories

Switch to **Data View** (table icon on left sidebar).

### In `raw_crm_data` table:
1. Click the **`Lat`** column header
2. In the top ribbon **Column Tools**:
   - **Summarization** → `Don't Summarize`
   - **Data Category** → `Latitude`
3. Click the **`Long`** column header
   - **Summarization** → `Don't Summarize`
   - **Data Category** → `Longitude`
4. Click the **`Store_Image_URL`** column header
   - **Data Category** → `Image URL`

### In `monitoring_sales_surabaya` table:
1. Click the **`Route_Geometry`** column header
   - **Summarization** → `Don't Summarize`
   - **Data Category** → `Uncategorized` (leave as Text, do NOT set to Address)

---

## STEP 4: Create Relationship

1. Switch to **Model View** (diagram icon on left sidebar)
2. Drag `Sales_ID` from `raw_crm_data` onto `Sales_ID` in `monitoring_sales_surabaya`
3. Double-click the relationship line and set:
   - **Cardinality**: Many to One (Many on `raw_crm_data` side)
   - **Cross filter direction**: Both
4. Click **OK**

---

## STEP 5: Create DAX Measures

Switch to **Report View**. Click on the `monitoring_sales_surabaya` table in the Fields pane.

### Measure 1: Total Fuel Budget
Click **Home → New Measure** and paste:
```dax
Total Fuel Budget = SUM('monitoring_sales_surabaya'[Fuel_Cost])
```
Then in **Measure Tools**: Format → Whole Number, Display Units → Auto

### Measure 2: Total Distance KM
```dax
Total Distance KM = SUM('monitoring_sales_surabaya'[Total_KM])
```
Format → Decimal, 1 decimal place

### Measure 3: Productivity KM Per Store
```dax
Productivity KM Per Store = 
DIVIDE(
    SUM('monitoring_sales_surabaya'[Total_KM]), 
    SUM('monitoring_sales_surabaya'[Store_Visited_Count]), 
    0
)
```
Format → Decimal, 2 decimal places

---

Now click on the `raw_crm_data` table in Fields pane, then **New Measure**:

### Measure 4: Total Revenue
```dax
Total Revenue = SUM('raw_crm_data'[Revenue_IDR])
```
Format → Whole Number, Display Units → Auto

### Measure 5: Total Items Sold
```dax
Total Items Sold = SUM('raw_crm_data'[Items_Sold])
```
Format → Whole Number

### Measure 6: Avg Revenue Per Visit
```dax
Avg Revenue Per Visit = 
DIVIDE(
    [Total Revenue], 
    COUNTROWS('raw_crm_data'), 
    0
)
```
Format → Whole Number, Display Units → Auto

### Measure 7: Sample Request Rate
```dax
Sample Request Rate = 
DIVIDE(
    COUNTROWS(FILTER('raw_crm_data', 'raw_crm_data'[Sample_Request] = TRUE())), 
    COUNTROWS('raw_crm_data'), 
    0
)
```
Format → Percentage, 1 decimal place

---

## STEP 6: Create Calculated Column

In **Data View**, select `raw_crm_data` table.
Click **Table Tools → New Column**:
```dax
Visit_Hour = HOUR('raw_crm_data'[Timestamp])
```

---

## STEP 7: Build Dashboard — Page 1 "Executive Overview"

Right-click the page tab at bottom → **Rename** → `Executive Overview`

### 7A. KPI Cards (Top Row)
Add 4 **Card** visuals across the top of the page:

| Card # | Field / Measure | Title |
|:--|:--|:--|
| 1 | `[Total Fuel Budget]` | 💰 Total Fuel Budget (Rp) |
| 2 | `[Total Items Sold]` | 📦 Total Items Sold |
| 3 | `[Total Revenue]` | 💵 Total Revenue (Rp) |
| 4 | `[Sample Request Rate]` | 📊 Sample Request Rate |

**Formatting for all cards:**
- Font Size: 28-32pt for value
- Background: Semi-transparent dark (e.g., `#1E1E2E` at 80%)
- Border: Rounded, accent color

### 7B. Clustered Bar Chart — Sales Productivity
1. Add a **Clustered Bar Chart**
2. **Y-axis**: `monitoring_sales_surabaya` → `Sales_ID`
3. **X-axis**: `[Productivity KM Per Store]`
4. Turn ON **Data Labels**
5. **Conditional Formatting**: Use Format → Data Colors → fx (rules):
   - If value ≤ 10 → Green `#2ECC71`
   - If value > 15 → Red `#E74C3C`
   - Otherwise → Yellow `#F39C12`
6. **Title**: "KM per Store Visit (Lower = More Efficient)"

### 7C. Stacked Bar Chart — Revenue by Visit Type
1. Add a **Stacked Bar Chart**
2. **Y-axis**: `raw_crm_data` → `Visit_Type`
3. **X-axis**: `[Total Revenue]`
4. **Legend**: `raw_crm_data` → `Sales_ID`
5. **Title**: "Revenue by Visit Type"

### 7D. Matrix — Performance Summary
1. Add a **Matrix** visual
2. **Rows**: `Sales_ID`
3. **Values**: `[Total Distance KM]`, `[Total Fuel Budget]`, `[Total Items Sold]`, `[Total Revenue]`, `[Productivity KM Per Store]`
4. Turn ON **Row subtotals**
5. **Conditional Formatting** on `[Total Revenue]`: Data bars (green)
6. **Conditional Formatting** on `[Productivity KM Per Store]`: Color scale (green→red)
7. **Title**: "Sales Performance Summary"

---

## STEP 8: Build Dashboard — Page 2 "Geospatial Route Analysis"

Right-click page tab → **+ (Add Page)** → Rename to `Geospatial Route Analysis`

### 8A. Install Icon Map Pro
1. In the Visualizations pane → Click `...` (three dots) → **Get more visuals**
2. Search: **"Icon Map"** by James Dales
3. Click **Add** → it appears in your visualization pane

### 8B. Configure Icon Map Pro
1. Add the **Icon Map** visual to the canvas (make it large, ~70% of page width)
2. Map the following fields into the **field wells**:

| Icon Map Pro Bucket | Drag This Field | From Table | Aggregation |
|:--|:--|:--|:--|
| **ID** | `Sales_ID` | `monitoring_sales_surabaya` | — |
| **Longitude (X)** | `Long` | `raw_crm_data` | ⚠️ **Average** |
| **Latitude (Y)** | `Lat` | `raw_crm_data` | ⚠️ **Average** |
| **Destination Longitude** | *(Leave empty)* | — | — |
| **Destination Latitude** | *(Leave empty)* | — | — |
| **Circle Size** | `Items_Sold` | `raw_crm_data` | Sum |
| **Cluster Group** | `Sales_ID` | `raw_crm_data` | — |
| **H3 Weight** | *(Leave empty)* | — | — |
| **Heatmap Weight** | `Revenue_IDR` | `raw_crm_data` | Sum |
| **WKT / Image** | `Route_Geometry` | `monitoring_sales_surabaya` | — |
| **Feature Reference** | `Sales_ID` | `monitoring_sales_surabaya` | — |

> ⚠️ **CRITICAL**: For **Latitude** and **Longitude**, click the dropdown arrow `∨` next to the field and change from `Sum` to **`Average`**. Using Sum will break the map.

3. **Format the Map** (click the paint roller icon):
   - **Map Settings → Map Provider**: OpenStreetMap
   - **Map Settings → Auto Zoom**: ON
   - **Layer Settings → Line Width**: 3 or 4
   - **Layer Settings → Opacity**: 70%

### 8C. Add Slicer Panel (Left Side)
Add 3 **Slicer** visuals on the left sidebar (~20% width):

**Slicer 1 — Sales Person:**
- Field: `Sales_ID`
- Style: **Tile / Button** (Format → Slicer Settings → Style)

**Slicer 2 — Visit Type:**
- Field: `Visit_Type`
- Style: **Dropdown** or **List**

**Slicer 3 — Date:**
- Field: `Date`
- Style: **Between** (date range)

### 8D. Add a Small Table (Bottom of Map)
1. Add a **Table** visual below the map
2. Columns: `Sales_ID`, `[Total Distance KM]`, `[Total Fuel Budget]`, `Store_Visited_Count`
3. Title: "Route Summary"

---

## STEP 9: Apply Theme & Polish

### Color Palette for Sales Persons
Use **conditional formatting** across all visuals:
| Sales Person | Color | Hex |
|:--|:--|:--|
| Sales_A | Deep Blue | `#3498DB` |
| Sales_B | Vivid Orange | `#E67E22` |
| Sales_C | Emerald Green | `#2ECC71` |

### Dashboard Theme
1. Go to **View → Themes → Customize current theme**
2. Set background to dark: `#0D1117`
3. Set card backgrounds to: `#161B22` at 90% opacity
4. Text color: `#E6EDF3`
5. Accent colors: Use the palette above

### Final Touches
- Add a **Text Box** at the very top: `"Sales Monitoring Dashboard — Surabaya Region"`
- Font: Segoe UI Semibold, 24pt, White
- Add your company logo if available (Insert → Image)

---

## STEP 10: Enable Cross-Filtering

1. Go to **Format → Edit Interactions** (in the top ribbon)
2. Click on the **Productivity Bar Chart**
3. For the Icon Map, ensure the filter icon (funnel) is selected — NOT the blocked icon
4. Repeat for all visuals — every chart should cross-filter the map

**Result**: Clicking "Sales_A" on any chart will zoom the Icon Map to show only Sales_A's route!

---

## 🎉 Dashboard Complete!

Your dashboard should now have:
- ✅ 4 KPI cards with key metrics
- ✅ Productivity analysis per salesperson
- ✅ Revenue breakdown by visit type
- ✅ Performance matrix with conditional formatting
- ✅ **Geospatial route map** showing real road paths across Surabaya
- ✅ Interactive slicers for filtering
- ✅ Full cross-filtering between all visuals
