import pandas as pd
import pydeck as pdk
import streamlit as st

class MapLayer:
    @staticmethod
    def create_layers(coords, strava_list, polyline_paths):
        """Create PyDeck layers for Strava data."""
        lats = [c[0] for c in coords]
        lons = [c[1] for c in coords]
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)

        strava_scatter = pdk.Layer(
            "ScatterplotLayer",
            data=pd.DataFrame({
                "lat": lats, "lon": lons,
                "name": [s["Name"] for s in strava_list]
            }),
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

        # = Speichern der Layer und des ViewState in den Sessionstate =
        # Hier werden die Layer und der ViewState in den Sessionstate gespeichert
        st.session_state.strava_layers_cache = [strava_paths, strava_scatter]
        st.session_state.view_state_cache = pdk.ViewState(
            latitude=center_lat,
            longitude=center_lon,
            zoom=11,
            pitch=0
        )

        return [strava_scatter, strava_paths], view_state
    


    