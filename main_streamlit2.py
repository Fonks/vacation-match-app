import streamlit as st

st.set_page_config(page_title="Vacation Match", layout="wide")
st.title("🏞️ Vacation Match – Your Activity Planner")

# Initiale Platzhalter
selected_poi_groups = []
cities = []
activity = None
poi_filter = []
strava_segments = []
osm_pois = []

# 1. Sidebar – Gruppierung von POIs und Settings
try:
    from ui.sidebar import SidebarController
    sidebar = SidebarController()
    selected_poi_groups = sidebar.select_poi_categories()
except Exception as e:
    st.warning("⚠️ Sidebar-Funktion nicht geladen.")

# 2. User Input – Städte, Aktivitäten, POI-Auswahl
try:
    from ui.user_input import UserInputHandler
    user_input = UserInputHandler()
    cities = user_input.get_selected_cities()
    activity = user_input.get_selected_activity()
    poi_filter = user_input.get_selected_poi_subcategories(selected_poi_groups)
except Exception as e:
    st.warning("⚠️ User Input-Komponente nicht verfügbar.")

# 3. Daten holen – Strava + OSM pro Region
try:
    from data.fetcher import DataFetcher
    fetcher = DataFetcher()
    strava_segments = fetcher.fetch_strava_for_cities(cities, activity)
    osm_pois = fetcher.fetch_osm_for_cities(cities, poi_filter)
except Exception as e:
    st.warning("⚠️ Datenabruf nicht verfügbar.")

# 4. Button Interaktion
if st.button("🔍 Explore your region"):
    # 5. Kartenvisualisierung
    try:
        from map.visualizer import MapVisualizer
        visualizer = MapVisualizer()
        visualizer.display_map(strava_segments, osm_pois)
    except Exception as e:
        st.warning("⚠️ Kartenanzeige nicht geladen.")

    # 6. Tabelle anzeigen
    try:
        from ui.table_display import TableDisplay
        table = TableDisplay()
        table.show_segment_table(strava_segments)
        table.show_poi_table(osm_pois)
    except Exception as e:
        st.warning("⚠️ Tabellenmodul nicht geladen.")
