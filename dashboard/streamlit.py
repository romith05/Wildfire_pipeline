import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import requests
def is_water_body_osm(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse"
    params = {
        "format": "json",
        "lat": lat,
        "lon": lon,
        "zoom": 14,
        "addressdetails": 1
    }
    headers = {"User-Agent": "wildfire-risk-app"}
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        name = data.get("name", "").lower()
        display_name = data.get("display_name", "").lower()
        keywords = ["lake", "river", "ocean", "creek", "bay", "pond"]
        return any(kw in name or kw in display_name for kw in keywords)
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

        folium.Marker(
            location=[53.5, -113.5],
            tooltip="Click on the map",
            icon=folium.Icon(color="blue")
        ).add_to(m)

        map_data = st_folium(m, width=700, height=500)

    with right_col:
        st.subheader("📈 Prediction Result")

        if map_data and map_data.get("last_clicked"):
            lat = map_data["last_clicked"]["lat"]
            lon = map_data["last_clicked"]["lng"]

            st.markdown(f"**Selected Location:** `{lat:.4f}, {lon:.4f}`")

            if is_water_body_osm(lat, lon):
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
                            color: {'#1f77b4' if is_water else '#d62728'}; 
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
    heat_data = [
        [53.5, -113.5],
        [54.0, -114.0],
        [55.0, -115.5],
        [52.0, -116.0],
        [54.5, -117.2]
    ]

    m = folium.Map(location=[54.0, -115.0], zoom_start=6, min_zoom=6, max_bounds=True)

    HeatMap(heat_data).add_to(m)

    st_folium(m, width=1000, height=600)

# Bottom placeholder section
st.markdown("---")
st.subheader("🔧 Additional Analysis (Coming Soon)")
st.markdown("""
<div style="border: 2px dashed gray; padding: 20px; border-radius: 10px; background-color: #f9f9f9;">
    <em>This section will be added later with more insights or visualizations.</em>
</div>
""", unsafe_allow_html=True)


