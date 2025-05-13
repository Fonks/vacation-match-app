import streamlit as st

 ## Hier wird der Cache initialisiert, um die Daten zwischen den Interaktionen zu speichern.
## Dies ist wichtig, um die Daten nicht bei jedem Klick neu zu laden und um die Performance zu verbessern.


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

    @staticmethod
    def set_cache(key, value):
        """Set a value in the session state."""
        st.session_state[key] = value

    @staticmethod
    def get_cache(key, default=None):
        """Get a value from the session state, or return a default value if the key doesn't exist."""
        return st.session_state.get(key, default)

    @staticmethod
    def add_to_set(key, value):
        """Add a value to a set in the session state."""
        if key not in st.session_state:
            st.session_state[key] = set()
        st.session_state[key].add(value)

    @staticmethod
    def remove_from_set(key, value):
        """Remove a value from a set in the session state."""
        if key in st.session_state and isinstance(st.session_state[key], set):
            st.session_state[key].discard(value)

    @staticmethod
    def cache_strava_data(df, layers, view_state):
        """Cache Strava data and visualization layers."""
        st.session_state.df_strava_cache = df
        st.session_state.layers_cache = layers
        st.session_state.view_state_cache = view_state