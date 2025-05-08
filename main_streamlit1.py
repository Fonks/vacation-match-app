import streamlit as st
from ui.user_input import UserInputHandler
from data.fetcher import DataFetcher
from map.visualizer import MapVisualizer
from ui.sidebar import SidebarController
from ui.table_display import TableDisplay

# Seitenkonfiguration
st.set_page_config(page_title="Vacation Match", layout="wide")
st.title("🏞️ Vacation Match – Your Activity Planner")

# 1. Sidebar – Gruppierung von POIs und Settings
sidebar = SidebarController()
selected_poi_groups = sidebar.select_poi_categories()

# 2. User Input – Städte, Aktivitäten, POI-Auswahl
user_input = UserInputHandler()
cities = user_input.get_selected_cities()
activity = user_input.get_selected_activity()
poi_filter = user_input.get_selected_poi_subcategories(selected_poi_groups)

# 3. Daten holen – Strava + OSM pro Region
fetcher = DataFetcher()
strava_segments = fetcher.fetch_strava_for_cities(cities, activity)
osm_pois = fetcher.fetch_osm_for_cities(cities, poi_filter)

# 4. Button Interaktion
if st.button("🔍 Explore your region"):
    # 5. Kartenvisualisierung
    visualizer = MapVisualizer()
    visualizer.display_map(strava_segments, osm_pois)

    # 6. Tabelle anzeigen
    table = TableDisplay()
    table.show_segment_table(strava_segments)
    table.show_poi_table(osm_pois)
