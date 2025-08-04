import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import requests
import rasterio
from rasterio.transform import rowcol
from pyproj import Transformer
from folium.plugins import HeatMap
import plotly.express as px
def is_water_body(lat, lon, tiff_path):
    with rasterio.open(tiff_path) as src:
        # Set up coordinate transformer if needed
        if src.crs.to_string() != "EPSG:4326":
            transformer = Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)
            lon, lat = transformer.transform(lon, lat)
        
        try:
            row, col = src.index(lon, lat)
            value = src.read(1, window=((row, row+1), (col, col+1)))[0, 0]
            return value == 1
        except Exception as e:
            print("Error:", e)
            return False

# Layout setup
st.set_page_config(layout="wide")
st.title("Wildfire Risk Prediction Dashboard")
st.markdown("---")

map_mode = st.radio("Select Map View:", ["Click Prediction Map", "Historical Heatmap"], horizontal=True)

if map_mode == "Click Prediction Map":
    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("🗺️ Click to Predict Risk")

        m = folium.Map(location=[54.0, -115.0], zoom_start=6, min_zoom=6, max_bounds=True)

        # folium.Marker(
        #     location=[53.5, -113.5],
        #     tooltip="Click on the map",
        #     icon=folium.Icon(color="blue")
        # ).add_to(m)

        map_data = st_folium(m, width=1000, height=700)

    with right_col:
        st.subheader("📈 Prediction Result")

        if map_data and map_data.get("last_clicked"):
            lat = map_data["last_clicked"]["lat"]
            lon = map_data["last_clicked"]["lng"]

            st.markdown(f"**Selected Location:** `{lat:.4f}, {lon:.4f}`")

            if is_water_body(lat, lon,"dsw-2023-mask.tif"):
                percentage = 0.0
                is_water = True
            else:
                percentage = round(random.uniform(0, 1) * 100, 1)
                is_water = False

            st.markdown(
                f"""
                <div style="font-family: 'Georgia', serif; 
                            font-size: 48px; 
                            font-weight: bold; 
                            color: {"#000000" if is_water else "#000000"}; 
                            text-align: center;
                            margin-top: 30px;">
                    {percentage:.1f}% Risk
                </div>
                """,
                unsafe_allow_html=True
            )

            if is_water:
                st.markdown(
                    f"""
                    <div style="text-align: center; color: gray; font-style: italic;">
                        A water body
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("Click on the map to get wildfire risk prediction.")

elif map_mode == "Historical Heatmap":
    st.subheader("🔥 Historical Wildfire Occurrences Heatmap")

    # Example heatmap data (lat, lon) — replace with real historical wildfire data
    


    

# Bottom placeholder section
st.markdown("---")
st.subheader("🔧 Additional Analysis ")
st.markdown("""
<div style="border: 2px dashed gray; padding: 20px; border-radius: 10px; background-color: #f9f9f9;">
    <em>This section will be added later with more insights or visualizations.</em>
</div>
""", unsafe_allow_html=True)
st.title("🔥 Wildfire Historical Analysis")

# Create 4 columns
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# === 1. HEATMAP ===
with col1:
    st.subheader("🔥 Wildfire Heatmap (Density)")
    map_center = [54.0, -115.0]
    import pandas as pd
    # Replace with your actual file path
    df = pd.read_csv("historical_wildfire.csv")

    # Drop missing values if necessary
    df = df.dropna(subset=['latitude', 'longitude'])


    map_center = [54.0, -115.0]
    m = folium.Map(location=map_center, zoom_start=4, min_zoom=6, max_bounds=True)

    # Create a list of coordinate points
    heat_data = df[['latitude', 'longitude']].values.tolist()

    #  Add heatmap
    HeatMap(heat_data, radius=10).add_to(m)
    st_folium(m, width=700, height=700)
# === 2. BAR CHART: Yearly Wildfires ===
with col2:
    st.subheader("📊 Yearly Wildfire Counts")
    if 'fire_year' in df.columns:
        year_counts = df['fire_year'].value_counts().sort_index()
        st.bar_chart(year_counts)

# === 3. HISTOGRAM: Fire Sizes ===
with col3:
    st.subheader("📏 Distribution of Fire Sizes")
    #st.plotly_chart(px.histogram(df, fire_year="size", nbins=50, title="Histogram of Fire Sizes"))

# === 4. PIE CHART: Proportion by Cause (if available) ===
with col4:
    st.subheader("🧯 Fire Causes (if available)")
    if 'fuel_type' in df.columns:
        cause_counts = df['fuel_type'].value_counts()
        st.plotly_chart(px.pie(names=cause_counts.index, values=cause_counts.values, title="Fire Causes"))
    else:
        st.info("No 'cause' column found in the data.")
