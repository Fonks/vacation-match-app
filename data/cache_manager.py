import streamlit as st

 ## Hier wird der Cache initialisiert, um die Daten zwischen den Interaktionen zu speichern.



class CacheManager:
    @staticmethod
    def initialize_cache():
        """Initialize all required session state variables with default values."""
        if "selected_osm_ids" not in st.session_state:
            st.session_state.selected_osm_ids = set()
        if "osm_data_cache" not in st.session_state:
            st.session_state.osm_data_cache = None
        if "layers_cache" not in st.session_state:
            st.session_state.layers_cache = []
        if "view_state_cache" not in st.session_state:
            st.session_state.view_state_cache = None
        if "df_strava_cache" not in st.session_state:
            st.session_state.df_strava_cache = None

