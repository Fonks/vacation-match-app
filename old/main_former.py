import streamlit as st
from user_input import geocode_city, create_bounding_box
from strava_api import fetch_strava_segments, decode_polyline
from osm_api import fetch_osm_data
import pandas as pd
from data_cleaning import clean_osm_data, clean_strava_segments
import pydeck as pdk



st.title("🏃‍♂️ Vacation Match: Your Activity Planner")

# User inputs
city = st.text_input("Enter a city or coordinates", "Aschaffenburg")
radius = st.slider("Select radius (km)", 1, 30, 10)
activity_type = st.selectbox("Choose activity type", ["running", "riding"])

if st.button("Explore Segments"):
    try:
        # Geocoding and bounding box
        lat, lon = geocode_city(city)
        bounds = create_bounding_box(lat, lon, radius)




        # Fetch data
        segments = fetch_strava_segments(bounds, activity_type)
        osm_data = fetch_osm_data(bounds)

        # Prepare Strava data
        strava_list = []
        if "segments" in segments and segments["segments"]:
            for seg in segments["segments"]:
                strava_list.append({
                    "Name": seg.get("name"),
                    "Distance (m)": round(seg.get("distance", 0), 1),
                    "Avg Grade (%)": seg.get("avg_grade"),
                    "Elevation Difference": seg.get("elev_difference"),
                    "Start Lat/Lon": seg.get("start_latlng"),
                    "End Lat/Lon": seg.get("end_latlng")
                })
            df_strava = pd.DataFrame(strava_list)
            st.subheader("📈 Strava Segments")
            st.dataframe(df_strava)
        else:
            st.info("No Strava segments found.")

        # Prepare OSM data
        osm_list = []
        elements = osm_data.get("elements", [])
        for el in elements:
            tags = el.get("tags", {})
            lat_osm = el.get("lat") or el.get("center", {}).get("lat")
            lon_osm = el.get("lon") or el.get("center", {}).get("lon")
            osm_list.append({
                "Type": el.get("type"),
                "Amenity": tags.get("amenity", "n/a"),
                "Name": tags.get("name", "n/a"),
                "Lat": lat_osm,
                "Lon": lon_osm
            })
        if osm_list:
            df_osm = pd.DataFrame(osm_list)
            st.subheader("🗺️ OSM Features")
            st.dataframe(df_osm)
        else:
            st.info("No OSM data found in this area.")

    except Exception as e:
        st.error(f"Error: {e}")
