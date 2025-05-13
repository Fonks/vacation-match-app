import streamlit as st
import pandas as pd
from data.cache_manager import CacheManager
from data.pre_processor import PreProcessor
from data.data_fetcher import DataFetcher
from data.post_processor import DataProcessor
from map.map_layers import MapLayer
from map.map_renderer import MapRenderer


from ui.osm_categories_selection import OSMFeatureSelector





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
radius = st.slider("Select radius (km)", 1, 30, 1)
activity_type = st.selectbox("Choose activity type", ["running", "riding"])

#---------------------------------------------------


# === Strava-Segmente + OSM Daten abrufen ===

    ## TODO: comment this out


if st.button("Explore Segments"):


    ## PREPROCESSING
    # Hier wird die Methode geocode_city aufgerufen, um die Stadt zu geokodieren
    pre_processor = PreProcessor(city, radius) # Initialisiere die Klasse PreProcessor mit Stadt und Radius
    pre_processor.geocode_city() # Hier wird die Methode geocode_city aufgerufen, um die Stadt zu geokodieren

    # Hier wird die Methode create_bounding_box aufgerufen, um die Bounding Box zu erstellen
    bounds = pre_processor.create_bounding_box() 
    

    # Hier wird die Methode split_bounds aufgerufen, um die Bounding Box in kleinere Bereiche zu unterteilen
    sub_bounds = pre_processor.split_bounds() 


    # FETCHEN DER STRAVA SEGMENTE
    # Hier wird die Methode fetch_strava_segments aufgerufen und die Daten verarbeitet
    data_fetcher = DataFetcher(bounds, sub_bounds, activity_type, use_cached=True) # Initialisiere die Klasse DataFetcher mit den Bounding Boxen und dem Aktivitätstyp
    strava_data, osm_data = data_fetcher.fetch_data()  # Hier kommen die Daten von Strava und OSM


    # POSTPROCESSING
    # Hier wird die Methode process_strava_data aufgerufen, um die Strava-Segmente zu verarbeiten
    data_processor = DataProcessor() # Initialisiere die Klasse DataProcessor 
    df_strava, coords, polyline_paths = data_processor.process_strava_data(strava_data) # Hier kommt pd.DataFrame(strava_list), coords, polyline_paths






    st.session_state.df_strava_cache = df_strava
    st.session_state.coords_cache = coords
    st.session_state.polyline_paths_cache = polyline_paths
    st.session_state.osm_data_cache = osm_data
    

    # st.session_state.view_state_cache = None    
    # st.session_state.strava_layers_cache = None
    # st.session_state.bounds = bounds
    # st.session_state.sub_bounds = sub_bounds
    # st.session_state.activity_type = activity_type
    # st.session_state.city = city
    # st.session_state.radius = radius
    # st.session_state.lat_radius = pre_processor.lat_radius
    # st.session_state.lon_radius = pre_processor.lon_radius
 




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
    ## Die Klasse OSMFeatureSelector findet ihr in der Datei osm_categories_selection.py.
    

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



if st.session_state.df_strava_cache is not None and st.session_state.osm_data_cache:

    # Aktualisiere Layers bei jeder Interaktion
    layer = MapLayer()
    layers, view_state = layer.create_layers(
        st.session_state.coords_cache,
        st.session_state.df_strava_cache.to_dict("records"),
        st.session_state.polyline_paths_cache,
        osm_data_cache=st.session_state.osm_data_cache,
        selected_osm_ids=st.session_state.selected_osm_ids
    )

    st.session_state.layers_cache = layers
    st.session_state.view_state_cache = view_state

    map_renderer = MapRenderer(
        view_state_cache=view_state,
        layers_cache=layers,
        osm_data_cache=st.session_state.osm_data_cache,
        selected_osm_ids=st.session_state.selected_osm_ids
    )

    map_renderer.render_map()


