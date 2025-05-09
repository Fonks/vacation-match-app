import streamlit as st
from user_input import geocode_city, create_bounding_box
from data_fetcher import DataFetcher
from strava_api import fetch_strava_segments
from osm_api import fetch_osm_data, group_osm_tags
from OSM_categories_selection import OSMFeatureSelector
from cache_manager import CacheManager
import pandas as pd
import pydeck as pdk
import polyline


# ===============================================
# ===============================================


# === Streamlit App Layout ===

st.set_page_config(layout="wide")
st.title("🏃‍♂️ Vacation Match: Your Activity Planner")

st.markdown("Find the best Strava segments and OSM features for your next vacation!")

# -----------------------------------------------


# === Initialisiere SessionState bzw Cache ===

    ## Hier wird der Cache initialisiert, um die Daten zwischen den Interaktionen zu speichern.
    ## Ihr findet die Cache-Manager-Klasse in der Datei cache_manager.py.
CacheManager.initialize_cache()


#---------------------------------------------------

# === Eingabemöglichkeiten für den User ===

city = st.text_input("Enter a city or coordinates", "Aschaffenburg")
radius = st.slider("Select radius (km)", 1, 30, 10)
activity_type = st.selectbox("Choose activity type", ["running", "riding"])

#---------------------------------------------------


# === Strava-Segmente + OSM Daten abrufen ===

    ## Hier wird die Klasse DataFetcher aufgerufen, um die Daten von Strava und OSM abzurufen.
    ## Die Klasse DataFetcher findet ihr in der Datei data_fetcher.py.
    ## Diese Methode berechnet, welchen Part der Karte wir uns anschauen wollen. und malt uns die Anfangspunkte und die Segmente auf die Karte.
    ## in der Datei data_fetcher.py können wir auch die Farben der Segmente anpassen.
if st.button("Explore Segments"):
    data_fetcher = DataFetcher(city, radius, activity_type)
    data_fetcher.fetch_data(geocode_city, create_bounding_box)
    st.session_state.osm_data_cache = data_fetcher.get_osm_data()

#---------------------------------------------------


# === Zeige Strava-Tabelle ===
if st.session_state.df_strava_cache is not None:
    st.subheader("📈 Strava Segments")
    st.dataframe(st.session_state.df_strava_cache)


#---------------------------------------------------


# === Zeige OSM-Auswahl ===


if st.session_state.osm_data_cache:
    osm_selector = OSMFeatureSelector(
        osm_data_cache=st.session_state.osm_data_cache,
        selected_osm_ids=st.session_state.selected_osm_ids
    )
    osm_selector.display_osm_features()



#---------------------------------------------------


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
