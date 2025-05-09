import streamlit as st
from user_input import geocode_city, create_bounding_box
from strava_api import fetch_strava_segments
from osm_api import fetch_osm_data, group_osm_tags
from cache_manager import CacheManager
import pandas as pd
import pydeck as pdk
import polyline

# === Streamlit App Layout ===
st.set_page_config(layout="wide")
st.title("🏃‍♂️ Vacation Match: Your Activity Planner")

st.markdown("Find the best Strava segments and OSM features for your next vacation!")

# === Initialisiere SessionState bzw Cache ===
    ## Hier wird der Cache initialisiert, um die Daten zwischen den Interaktionen zu speichern.
    ## Ihr findet die Cache-Manager-Klasse in der Datei cache_manager.py.
CacheManager.initialize_cache()




# === Eingabemöglichkeiten für den User ===
city = st.text_input("Enter a city or coordinates", "Aschaffenburg")
radius = st.slider("Select radius (km)", 1, 30, 10)
activity_type = st.selectbox("Choose activity type", ["running", "riding"])




# === Strava-Segmente + OSM Daten abrufen ===
if st.button("Explore Segments"):
    data_fetcher = DataFetcher(city, radius, activity_type)
    data_fetcher.fetch_data(geocode_city, create_bounding_box)


# === Zeige Strava-Tabelle ===
if st.session_state.df_strava_cache is not None:
    st.subheader("📈 Strava Segments")
    st.dataframe(st.session_state.df_strava_cache)

# === Zeige OSM-Auswahl ===

if st.session_state.osm_data_cache:
    grouped_osm = group_osm_tags(st.session_state.osm_data_cache.get("elements", []))
    st.subheader("🗺️ OSM Features by Category")

    for category, items in grouped_osm.items():
        with st.expander(f"{category} ({len(items)})", expanded=False):
            rows = []

            # Alle IDs dieser Kategorie
            category_ids = [f"{category}_{el.get('id')}" for el in items if el.get("lat") or el.get("center")]
            currently_selected = [cid for cid in category_ids if cid in st.session_state.selected_osm_ids]
            all_selected = len(currently_selected) == len(category_ids)

            # Checkbox zur Steuerung aller in Kategorie
            select_all = st.checkbox(
                f"Alle auswählen ({category})",
                value=all_selected,
                key=f"{category}_select_all"
            )

            for el in items:
                el_id = f"{category}_{el.get('id')}"
                tags = el.get("tags", {})
                lat_osm = el.get("lat") or el.get("center", {}).get("lat")
                lon_osm = el.get("lon") or el.get("center", {}).get("lon")
                if not (lat_osm and lon_osm):
                    continue

                # Auswahlstatus setzen
                if select_all and el_id not in st.session_state.selected_osm_ids:
                    st.session_state.selected_osm_ids.add(el_id)
                elif not select_all and el_id in st.session_state.selected_osm_ids:
                    st.session_state.selected_osm_ids.discard(el_id)

                # Einzelne Checkbox
                checked = el_id in st.session_state.selected_osm_ids
                checked = st.checkbox(
                    label=tags.get("name", "n/a"),
                    key=el_id,
                    value=checked
                )

                if checked:
                    st.session_state.selected_osm_ids.add(el_id)
                    rows.append({
                        "Name": tags.get("name", "n/a"),
                        "Amenity": tags.get("amenity", "n/a"),
                        "Latitude": lat_osm,
                        "Longitude": lon_osm
                    })
                else:
                    st.session_state.selected_osm_ids.discard(el_id)

            # if rows:
            #     df = pd.DataFrame(rows)
            #     st.dataframe(df, use_container_width=True)

# === Interaktive Karte mit Strava + OSM ===
if st.session_state.view_state_cache and st.session_state.strava_layers_cache:
    layers = st.session_state.strava_layers_cache.copy()
    selected_points = []

    if st.session_state.osm_data_cache:
        grouped_osm = group_osm_tags(st.session_state.osm_data_cache.get("elements", []))
        for category, items in grouped_osm.items():
            for el in items:
                el_id = f"{category}_{el.get('id')}"
                if el_id in st.session_state.selected_osm_ids:
                    tags = el.get("tags", {})
                    lat_osm = el.get("lat") or el.get("center", {}).get("lat")
                    lon_osm = el.get("lon") or el.get("center", {}).get("lon")
                    if lat_osm and lon_osm:
                        selected_points.append({
                            "name": tags.get("name", "n/a"),
                            "category": tags.get("amenity", "n/a"),
                            "lat": lat_osm,
                            "lon": lon_osm
                        })

    if selected_points:
        df_osm_selected = pd.DataFrame(selected_points)
        osm_layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_osm_selected,
            get_position='[lon, lat]',
            get_fill_color='[0, 128, 255, 160]',
            get_radius=80,
            pickable=True
        )
        layers.append(osm_layer)
        st.subheader("📍 Gewählte POIs")
        st.dataframe(df_osm_selected)

    # Karte rendern
    st.subheader("🗺️ Karte mit Strava-Segmenten & OSM-POIs")
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=st.session_state.view_state_cache,
        layers=layers,
        tooltip={"text": "{name}"}
    ))
