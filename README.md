# Election Data Processing and Visualization  

## Overview  
This project analyzes parliamentary election data to identify and visualize potential anomalies. Specifically, it finds polling locations that are geographically close (within a given threshold) but exhibit significant differences in voting percentages. The results are processed and presented in an interactive map for further investigation.

## Workflow Summary  
1. **Data Processing (`Data_Processing.py`)**  
   - Reads election data from an Excel file.  
   - Calculates the geographic distance between polling stations using the **Haversine formula**.  
   - Identifies pairs of locations that:  
     - Are within **1 km proximity** (configurable).  
     - Have a percentage difference in votes of **10% or more** (configurable).  
   - Outputs the identified location pairs and percentage differences to an Excel file.

2. **Data Visualization (`Visualization.py`)**  
   - Reads the processed results and the original election data.  
   - Extracts and verifies geographic coordinates.  
   - Plots the locations on an interactive **Folium** map.  
   - Marks each location with its voting percentage.  
   - Draws lines connecting close locations with high vote percentage differences.  
   - Generates an **HTML map** for visualization.

---

## Installation and Setup  

### 1. Install Dependencies  
Ensure you have Python installed and run:  
```sh
pip install pandas folium openpyxl numpy
```

### 2. Ensure Required Files Exist  
- **Raw election data:** `2024_parliamentary_round_1_proportional_electronic.xlsx`
- **Processed results file:** `close_address_pairs_with_high_percentage_difference.xlsx` (generated by `Data_Processing.py`)

---

## Code Breakdown: How It Works  

### 1. Data Processing (`Data_Processing.py`)  
This script reads election data and applies **two key conditions**:  

#### **Geographic Proximity Condition:**  
- Uses the **Haversine formula** to calculate the great-circle distance between two polling locations based on latitude/longitude.  
- Only considers pairs where the distance is **≤ 1 km** (adjustable).  

#### **Vote Percentage Difference Condition:**  
- Compares the **percentage of votes** at two nearby locations.  
- If the absolute difference is **≥ 10%**, the pair is flagged for investigation.  


#### **Processing Steps:**
1. Load election data from `2024_parliamentary_round_1_proportional_electronic.xlsx`.
2. Iterate over all pairs of polling locations.
3. Extract the **latitude, longitude, and vote percentage** for each location.
4. Compute the **Haversine distance** between the two locations.
5. If the distance is **≤ 1 km** and the percentage difference is **≥ 10%**, save the pair.
6. Store results in `close_address_pairs_with_high_percentage_difference.xlsx`.

### 2. Data Visualization (`Visualization.py`)  
This script takes the processed data and generates an interactive map.  

#### **Visualization Steps:**
1. Load processed election data (`close_address_pairs_with_high_percentage_difference.xlsx`).
2. Parse geographic coordinates for each polling location.
3. Validate and clean the data (handle missing or malformed coordinates).
4. Compute the **center** of all polling locations for proper map scaling.
5. Plot each polling location on a **Folium** map:  
   - Locations are marked with **vote percentages**.  
   - Lines connect close locations with significant vote differences.  
   - Hovering over a line displays **distance and percentage difference**.  
6. Save the map as `map.html` for analysis.

#### **Error Handling in Visualization:**
- **Missing data handling**: If a required file is missing, the script throws an informative error message.
- **Coordinate parsing**: If a coordinate is invalid, it's logged instead of crashing the script.

---

## Running the Project  

### Step 1: Process the Election Data  
Run:  
```sh
python Data_Processing.py
```
This will output:  
- **`close_address_pairs_with_high_percentage_difference.xlsx`** (detected anomalies).

### Step 2: Generate the Map  
Run:  
```sh
python Visualization.py
```
This will create:  
- **`map.html`** (interactive election anomaly visualization).

---

---

## Configuration  

If you need to adjust the thresholds, modify the variables in `Data_Processing.py`:

```python
proximity_threshold_km = 1  # Adjust this for different distance thresholds
percentage_diff_threshold = 10  # Adjust this for stricter or looser percentage differences
```

You can also change the zoom level in `Visualization.py` by adjusting:

```python
m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
```
For a more zoomed-out view, decrease `zoom_start`.

---

## Example Output  

### 1. Data Processing Output (Excel Example)  

| Address 1 (lat, lon) | Address 2 (lat, lon) | Distance (km) | Percentage Difference (%) | Percentage 1 | Percentage 2 |
|----------------------|----------------------|--------------|--------------------------|--------------|--------------|
| (41.71, 44.79) | (41.72, 44.80) | 0.8 km | 12.5% | 45% | 57.5% |
| (41.75, 44.83) | (41.76, 44.82) | 0.9 km | 15.3% | 33% | 48.3% |

### 2. Map Visualization Example (map.html)  
- Red markers display polling locations with vote percentages.  
- Lines between markers indicate detected anomalies.  
- Hovering over a line shows distance and percentage difference.

---

## Potential Use Cases  

- **Election Fraud Detection**: Identify anomalies where similar polling locations have drastically different vote shares.  
- **Geospatial Analysis**: Study how voting patterns change over small geographic distances.  

---

