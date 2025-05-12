import streamlit as st
from user_input import geocode_city, create_bounding_box
from data.data_fetcher import DataFetcher
from strava_api import fetch_strava_segments
from osm_api import fetch_osm_data, group_osm_tags
from OSM_categories_selection import OSMFeatureSelector
from map import MapRenderer
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
    ## Zeigt die Tabelle mit den Strava-Segmenten an, die wir abgerufen haben.
    ## Hier wird die Methode fetch_strava_segments aufgerufen und die Daten verarbeitet.
if st.session_state.df_strava_cache is not None:
    st.subheader("📈 Strava Segments")
    st.dataframe(st.session_state.df_strava_cache)




#---------------------------------------------------



# === Aneige der OSM-Auswahl ===
    ## Hier werden die OSM-Daten in Kategorien gruppiert und angezeigt. Diese kann man da auswählen und es wird dann (hoffentlich) dann in der Karte als Punkte oder Icons angezeigt.
    ## Die Klasse OSMFeatureSelector findet ihr in der Datei OSM_categories_selection.py.
    

if st.session_state.osm_data_cache:
    osm_selector = OSMFeatureSelector(
        osm_data_cache=st.session_state.osm_data_cache,
        selected_osm_ids=st.session_state.selected_osm_ids
    )
    osm_selector.display_osm_features()



#---------------------------------------------------



# === POIs Icons auf der Karte ===
##### PLACEHOLDER
    ## Hier werden die POIs auf der Karte angezeigt. Die Icons werden in der Klasse OSMFeatureSelector verarbeitet und dann hier angezeigt.
    ## Man könnte hier auch die Icons anpassen.
    ## Man könnte die icons einzeln als scatterplotlayer anzeigen.



#---------------------------------------------------


# === Interaktive Karte mit Strava + OSM ===
    ## Die Klasse MapRenderer findet ihr in der Datei map.py.


    # Stellt sicher, dass view_state_cache and strava_layers_cache initialiert werden
    # Findet ihr in cache_manager.py
if "view_state_cache" not in st.session_state:
    st.session_state.view_state_cache = None    # Initialize as None

if "strava_layers_cache" not in st.session_state:
    st.session_state.strava_layers_cache = None     # Initialize as None


    ## Hier wird die Methode render_map aufgerufen, um die Karte anzuzeigen.
    ## Diese Methode ist in der Klasse MapRenderer in der Datei map.py.
map_renderer = MapRenderer(
    view_state_cache=st.session_state.view_state_cache,
    strava_layers_cache=st.session_state.strava_layers_cache,
    osm_data_cache=st.session_state.osm_data_cache,
    selected_osm_ids=st.session_state.selected_osm_ids
)
map_renderer.render_map()

