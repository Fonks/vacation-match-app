import streamlit as st
from user_input import geocode_city, create_bounding_box
from strava_api import fetch_strava_segments
from osm_api import fetch_osm_data, group_osm_tags
import pandas as pd
import pydeck as pdk
import polyline  # Zum Dekodieren der Strava-Polylines


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
        coords = []

        if "segments" in segments and segments["segments"]:

            polyline_paths = []

            for seg in segments["segments"]:
                start = seg.get("start_latlng")
                if start and len(start) == 2:
                    coords.append(start)  # Liste für Map

                strava_list.append({
                    "Name": seg.get("name"),
                    "Distance (m)": round(seg.get("distance", 0), 1),
                    "Avg Grade (%)": seg.get("avg_grade"),
                    "Elevation Difference": seg.get("elev_difference"),
                    "Start Lat/Lon": start,
                    "End Lat/Lon": seg.get("end_latlng")
                })

                
                # Polylines dekodieren
                polyline_str = seg.get("points")
                if polyline_str:
                    decoded = polyline.decode(polyline_str)  # [(lat, lon), ...]
                    path = [[lon, lat] for lat, lon in decoded]
                    polyline_paths.append({
                        "name": seg.get("name", "Unnamed Segment"),
                        "path": path
                    })


                    df_strava = pd.DataFrame(strava_list)





            # --- 🗺️ Interaktive Karte anzeigen ---
            if coords:
                lats = [c[0] for c in coords]
                lons = [c[1] for c in coords]
                center_lat = sum(lats) / len(lats)
                center_lon = sum(lons) / len(lons)

                data_for_map = pd.DataFrame({
                    "lat": lats,
                    "lon": lons,
                    "name": [s["Name"] for s in strava_list]
                })

                strava_scatter = pdk.Layer(
                    "ScatterplotLayer",
                    data=data_for_map,
                    get_position='[lon, lat]',
                    get_fill_color='[255, 0, 0, 160]',
                    get_radius=100,
                    pickable=True
                )

                strava_paths = pdk.Layer(
                    "PathLayer",
                    data=polyline_paths,
                    get_path="path",
                    get_width=20,
                    get_color=[255, 0, 0],
                    opacity=0.6,
                    pickable=True
                )


                view_state = pdk.ViewState(
                    latitude=center_lat,
                    longitude=center_lon,
                    zoom=11,
                    pitch=0
                )

                st.subheader("🗺️ Karte der Strava-Segmente")
                st.pydeck_chart(pdk.Deck(
                    map_style="mapbox://styles/mapbox/light-v9",
                    initial_view_state=view_state,
                    layers=[strava_paths, strava_scatter],
                    tooltip={"text": "{name}"}
                ))


            # --- Tabelle unter der Karte ---
            st.subheader("📈 Strava Segments")
            st.dataframe(df_strava)

        else:
            st.info("No Strava segments found.")

        

        # Prepare OSM data
        osm_list = []
        elements = osm_data.get("elements", [])

        # Gruppieren nach Kategorien
        grouped_osm = group_osm_tags(elements)

        if grouped_osm:
            st.subheader("🗺️ OSM Features by Category")
            for category, items in grouped_osm.items():
                with st.expander(f"{category} ({len(items)})", expanded=False):
                    rows = []
                    for el in items:
                        tags = el.get("tags", {})
                        lat_osm = el.get("lat") or el.get("center", {}).get("lat")
                        lon_osm = el.get("lon") or el.get("center", {}).get("lon")
                        rows.append({
                            "Name": tags.get("name", "n/a"),
                            "Amenity": tags.get("amenity", "n/a"),
                            "Latitude": lat_osm,
                            "Longitude": lon_osm
                        })
                    df = pd.DataFrame(rows)
                    st.dataframe(df)
        else:
            st.info("No categorized OSM data found in this area.")

    except Exception as e:
        st.error(f"Error: {e}")

