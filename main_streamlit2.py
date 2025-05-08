import streamlit as st

# Konfiguration der Streamlit-Seite
st.set_page_config(page_title="Vacation Match", layout="wide")
st.title("🏞️ Vacation Match – Your Activity Planner")

# Platzhalter für spätere Inhalte
selected_poi_groups = []
cities = []
activity = None
poi_filter = []
strava_segments = []
osm_pois = []

# ----------------------------
# 1. Sidebar – Gruppierung von POIs und Settings
# ----------------------------
try:
    from ui.sidebar import SidebarController
    sidebar = SidebarController()
    selected_poi_groups = sidebar.select_poi_categories()
except Exception as e:
    st.warning(f"⚠️ Sidebar konnte nicht geladen werden: {e}")

# ----------------------------
# 2. User Input – Städte, Aktivitäten, POI-Auswahl
# ----------------------------
try:
    from ui.user_input import UserInputHandler
    user_input = UserInputHandler()
    cities = user_input.get_selected_cities()
    activity = user_input.get_selected_activity()
    poi_filter = user_input.get_selected_poi_subcategories(selected_poi_groups)
except Exception as e:
    st.warning(f"⚠️ User Input nicht verfügbar: {e}")

# ----------------------------
# 3. Daten holen – Strava + OSM pro Region
# ----------------------------
try:
    from data.fetcher import DataFetcher
    fetcher = DataFetcher()
    strava_segments = fetcher.fetch_strava_for_cities(cities, activity)
    osm_pois = fetcher.fetch_osm_for_cities(cities, poi_filter)
except Exception as e:
    st.warning(f"⚠️ Daten konnten nicht geladen werden: {e}")

# ----------------------------
# 4. Interaktion: Button zum Start
# ----------------------------
if st.button("🔍 Explore your region"):
    # ----------------------------
    # 5. Karte anzeigen
    # ----------------------------
    try:
        from map.visualizer import MapVisualizer
        visualizer = MapVisualizer()
        visualizer.display_map(strava_segments, osm_pois)
    except Exception as e:
        st.warning(f"⚠️ Karte konnte nicht dargestellt werden: {e}")

    # ----------------------------
    # 6. Tabellen anzeigen
    # ----------------------------
    try:
        from ui.table_display import TableDisplay
        table = TableDisplay()
        table.show_segment_table(strava_segments)
        table.show_poi_table(osm_pois)
    except Exception as e:
        st.warning(f"⚠️ Tabellenanzeige fehlgeschlagen: {e}")
