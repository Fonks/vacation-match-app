import streamlit as st
import pandas as pd
import pydeck as pdk

from user_input import geocode_city, create_bounding_box
from strava_api import fetch_strava_segments, decode_polyline, fetch_segment_details
from osm_api import fetch_osm_data
from data_cleaning import clean_osm_data, clean_strava_segments

st.set_page_config(page_title="Vacation Match", layout="wide")
st.title("🏃‍♂️ Vacation Match: Your Activity Planner")

# User inputs
city = st.text_input("Enter a city or coordinates", "Aschaffenburg")
radius = st.slider("Select radius (km)", 1, 30, 10)
activity_type = st.selectbox("Choose activity type", ["running", "riding"])

# OSM-Kategorie-Filter
filter_options = ["cafe", "drinking_water", "toilets", "viewpoint"]
selected_amenities = st.multiselect("Welche Kategorien sollen angezeigt werden?", filter_options, default=filter_options)

# Symbol-URL-Mapping für Icons (PNG oder SVG URLs)
def amenity_icon(amenity):
    return {
        "cafe": "https://cdn-icons-png.flaticon.com/512/2965/2965567.png",
        "drinking_water": "https://cdn-icons-png.flaticon.com/512/727/727790.png",
        "toilets": "https://cdn-icons-png.flaticon.com/512/179/179270.png",
        "viewpoint": "https://cdn-icons-png.flaticon.com/512/684/684908.png",
    }.get(amenity, "https://cdn-icons-png.flaticon.com/512/252/252025.png")

if st.button("Explore Segments"):
    try:
        # Geocoding and bounding box
        lat, lon = geocode_city(city)
        bounds = create_bounding_box(lat, lon, radius)

        # Fetch data
        segments = fetch_strava_segments(bounds, activity_type)
        osm_data = fetch_osm_data(bounds)

        # Clean data
        clean_segments = clean_strava_segments(segments)
        clean_osm = clean_osm_data(osm_data)

        # Fetch Strava segment details (to get polyline "points")
        detailed_segments = []
        for seg in clean_segments:
            seg_id = seg.get("id")
            if seg_id:
                detailed = fetch_segment_details(seg_id)
                if detailed:
                    seg["points"] = detailed.get("map", {}).get("polyline")
                    detailed_segments.append(seg)

        # Filter nach ausgewählten OSM-Kategorien
        filtered_osm = [el for el in clean_osm if el["Amenity"] in selected_amenities]

        # Prepare DataFrames
        strava_list = []
        for seg in detailed_segments:
            strava_list.append({
                "Name": seg.get("name"),
                "Distance (m)": round(seg.get("distance", 0), 1),
                "Avg Grade (%)": seg.get("avg_grade"),
                "Elevation Difference": seg.get("elev_difference"),
                "Start Lat/Lon": seg.get("start_latlng"),
                "End Lat/Lon": seg.get("end_latlng")
            })
        df_strava = pd.DataFrame(strava_list)

        df_osm = pd.DataFrame(filtered_osm)
        if not df_osm.empty:
            df_osm["icon_data"] = df_osm["Amenity"].apply(lambda a: {
                "url": amenity_icon(a),
                "width": 128,
                "height": 128,
                "anchorY": 128
            })

        # Anzeigen
        st.subheader("📈 Strava Segments (bereinigt)")
        st.dataframe(df_strava)
        st.subheader("🗺️ OSM Features (gefiltert)")
        st.dataframe(df_osm)

        # Map: Strava Wege (rot)
        line_layers = []
        for seg in detailed_segments:
            if "points" in seg:
                coords = decode_polyline(seg["points"])
                path = [{"lat": lat, "lon": lon} for lat, lon in coords]
                line_layers.append(
                    pdk.Layer(
                        "PathLayer",
                        [path],
                        get_path="data",
                        get_color=[255, 0, 0],
                        width_scale=2,
                        width_min_pixels=1,
                        width_max_pixels=4,
                        pickable=True,
                        auto_highlight=True,
                    )
                )

        # Map: OSM Icons
        icon_layer = pdk.Layer(
            "IconLayer",
            df_osm,
            get_icon="icon_data",
            get_size=4,
            size_scale=15,
            get_position="[Lon, Lat]",
            pickable=True,
        )

        tooltip = {
            "html": "<b>{Amenity}</b><br/>{Name}",
            "style": {"backgroundColor": "steelblue", "color": "white"}
        }

        # Karte anzeigen
        st.subheader("📍 Interaktive Karte")
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                latitude=lat,
                longitude=lon,
                zoom=13,
                pitch=30,
            ),
            layers=line_layers + [icon_layer],
            tooltip=tooltip
        ))

    except Exception as e:
        st.error(f"Error: {e}")
