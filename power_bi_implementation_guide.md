# Power BI Implementation Guide: Sales Monitoring Dashboard

This guide outlines the proper procedures to construct the end-to-end Power BI dashboard utilizing the `monitoring_sales_surabaya.csv` export produced by our script. We will be using **Well-Known Text (WKT)** mappings.

## 1. Importing & Modeling

1. Open Power BI and choose **Get Data > Text/CSV** and import your `monitoring_sales_surabaya.csv`.
2. Do not forget to adjust datatypes:
   - `Total_KM`, `Fuel_Cost`: Decimal Number
   - `Date`: Date Format
   - `Route_Geometry`: Text (Do not summarize this, keep it strictly as string mapping).

> [!IMPORTANT]
> To calculate "Sales Productivity (KM per Store Visit)", create a new Data Analysis Expression (DAX) Measure under your main table:
> ```dax
> Productivity_KM_Per_Store = DIVIDE(SUM('monitoring_sales_surabaya'[Total_KM]), SUM('monitoring_sales_surabaya'[Store_Visited_Count]), 0)
> ```

---

## 2. Rendering Route Polyline using Icon Map

For the best and most accurate polyline mapping of WKT geometries, we highly recommend adding the **Icon Map by James Dales** from the Power BI marketplace.

1. Go to the visuals pane > `Get more visuals`.
2. Search and Add **Icon Map**.
3. With an Icon Map selected on the canvas, map the following fields accordingly:
   - **Category**: `Sales_ID`
   - **Size**: `Total_KM` or `Fuel_Cost`
   - **Objects (WKT / GeoJSON)**: Drag your `Route_Geometry` column here. *(Crucial Step!)*
4. To modify the polylines, navigate into the visual's **Format icon > General / Formatting:**
   - Under `Map Features` or `Objects`, configure the styling (e.g. transparent thickness mapping mapped distinctly by `Sales_ID` colors).
   - This exact configuration immediately drops down your real road route clusters looping around Surabaya area.

---

## 3. Creating The Final Dashboard Requirements

Build the primary views requested:

### A. Total Fuel Budget Spent
- Add a **Card Visual** or **Gauge Visual**.
- Drag in the `Fuel_Cost` metric and set the aggregation to `Sum`.
- *Wait.* You can refine the display unit into Millions (Rp) and give it the format standard of Indonesian currency.

### B. Map of Visit Clusters in Surabaya
- Implement the configured **Icon Map** visual as guided in step 2.
- Since we have different sales associates, set the **Item Color** dynamically referencing the `Sales_ID`. You can then identify the territorial spread (Sales_A covers West Surabaya vs. Sales_B covers Central, etc.) visibly.

### C. Sales Productivity
- Add a **Bar Chart** or **Matrix**.
- Plot `Sales_ID` along the X-axis (or Rows).
- Plot the custom `Productivity_KM_Per_Store` DAX measure along the Y-axis (or Values).
- *Insight:* A higher KM per store metric indicates geographic inefficiency. The lower it runs, the tighter the sequence radius achieved.

> [!TIP]
> Keep the interactivity robust! When clicking a single `Sales_ID` on the Sales Productivity chart, your Icon Map must filter down sequentially showing only their single daily route mapped across the city boundaries.
