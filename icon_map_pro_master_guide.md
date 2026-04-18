# Master Guide: Geospatial Analytics with Icon Map Pro

This guide elevates your "Sales Monitoring" dashboard from basic mapping to a professional **Geospatial Intelligence System** using **Icon Map Pro**. 

---

## 🚀 Field Mapping Reference (Cheat Sheet)
Use this table to drag and drop your fields into the **Icon Map Pro** field wells:

| Icon Map Pro Bucket | Sales Monitoring Field | Rationale |
| :--- | :--- | :--- |
| **ID** | `Sales_ID` | Identifies the unique route or salesperson entity. |
| **Longitude** | `Long` | (For Point Layer) The store's horizontal coordinate. |
| **Latitude** | `Lat` | (For Point Layer) The store's vertical coordinate. |
| **Destination Long / Lat** | *[Leave Blank]* | Used for straight lines (OD); we use WKT for road paths. |
| **Circle Size** | `Items_Sold` | Stores with more sales will appear larger. |
| **Cluster Group** | `Sales_ID` | Groups visit clusters by the assigned salesperson. |
| **Heatmap Weight** | `Revenue_IDR` | Visualizes "Expensive" driving areas with a glow. |
| **WKT / Image** | `Route_Geometry` | **CRITICAL**: Renders the OSRM road polylines. |
| **Feature Reference** | `Sales_ID` | Allows dynamic filtering and high-speed indexing. |

---

## Troubleshooting "WKT Not Rendering"
If your Route lines don't appear:
1. **Case Sensitivity**: Ensure your string starts exactly with `LINESTRING` (uppercase). Our script handles this.
2. **Data Category**: In the Data View, select the `Route_Geometry` column. Go to **Column Tools** > **Data Category** and set it to **Uncategorized** (Do not set to Address).
3. **Aggregation**: For Lat/Long, always use **Average**, never Sum.

> [!TIP]
> Use the **Map Tiles** setting to switch to **OpenStreetMap** or **Mapbox Street**. It provides much better road-level context for building materials logistics than the default Power BI gray map.
