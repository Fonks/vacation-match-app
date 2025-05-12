import pandas as pd
import pydeck as pdk
import streamlit as st
from osm_api import group_osm_tags

    ## Hier wird die Klasse MapRenderer definiert, die für das Rendern der Karte verantwortlich ist.

    ## Die Klasse MapRenderer verwendet die pydeck-Bibliothek, um eine interaktive Karte zu erstellen.

    ## Die Karte zeigt Strava-Segmente und OSM-POIs an, die vom Benutzer ausgewählt wurden.

    ## Die Methode _get_selected_points extrahiert die ausgewählten OSM-Punkte basierend auf der Benutzerauswahl.  

class MapRenderer:
    def __init__(self, view_state_cache, strava_layers_cache, osm_data_cache, selected_osm_ids):
        self.view_state_cache = view_state_cache
        self.strava_layers_cache = strava_layers_cache
        self.osm_data_cache = osm_data_cache
        self.selected_osm_ids = selected_osm_ids

    def _get_selected_points(self):
        """Extract selected OSM points based on user selection."""
        selected_points = []
        if self.osm_data_cache:
            grouped_osm = group_osm_tags(self.osm_data_cache.get("elements", []))
            for category, items in grouped_osm.items():
                for el in items:
                    el_id = f"{category}_{el.get('id')}"
                    if el_id in self.selected_osm_ids:
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
        return selected_points

    def render_map(self):
        """Render the interactive map with Strava and OSM layers."""
        if not self.view_state_cache or not self.strava_layers_cache:
            # st.warning("Map data is not available.")
              #habe das hier auskommentiert, weil der sonst unnötigerweise eine Warnung ausgibt, wenn die Daten noch nicht eingegeben wurden.	
            return

        # Mit Strava Ebenen beginnen
        layers = self.strava_layers_cache.copy()

        # Fügt die OSM-POIs hinzu, wenn sie ausgewählt sind
        selected_points = self._get_selected_points()
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

        # Render die Karte
        st.subheader("🗺️ Karte mit Strava-Segmenten & OSM-POIs")
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=self.view_state_cache,
            layers=layers,
            tooltip={"text": "{name}"}
        ))