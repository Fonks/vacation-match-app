import streamlit as st
import pydeck as pdk

class MapVisualizer:
    def display_map(self, segments: list, pois: list):
        if not segments and not pois:
            st.info("Keine Daten zum Anzeigen.")
            return

        layers = []

        if segments:
            segment_layer = pdk.Layer(
                "ScatterplotLayer",
                data=[{"lat": s.lat, "lon": s.lon, "name": s.name} for s in segments],
                get_position='[lon, lat]',
                get_radius=70,
                get_fill_color='[0, 180, 50, 160]',
                pickable=True
            )
            layers.append(segment_layer)

        if pois:
            poi_layer = pdk.Layer(
                "ScatterplotLayer",
                data=[{"lat": p.lat, "lon": p.lon, "name": p.name} for p in pois],
                get_position='[lon, lat]',
                get_radius=80,
                get_fill_color='[0, 100, 250, 160]',
                pickable=True
            )
            layers.append(poi_layer)

        # Bestimme Viewport über den ersten Datensatz (Fallback nötig)
        lat, lon = 48.13, 11.57  # Default: München
        if segments:
            lat, lon = segments[0].lat, segments[0].lon
        elif pois:
            lat, lon = pois[0].lat, pois[0].lon

        view_state = pdk.ViewState(latitude=lat, longitude=lon, zoom=12)

        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=view_state,
            layers=layers,
            tooltip={"text": "{name}"}
        ))
