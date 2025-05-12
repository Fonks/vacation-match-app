import pandas as pd
import pydeck as pdk
import polyline
import streamlit as st
from strava_api import fetch_strava_segments
from osm_api import fetch_osm_data

class DataFetcher:

    ## === Was alles in der Klasse enthalten ist ===
    # 1. Initialisierung der Klasse mit den Attributen Stadt, Radius und Aktivitätstyp  
    def __init__(self, city, radius, activity_type):
        self.city = city
        self.radius = radius
        self.activity_type = activity_type
        self.bounds = None
        self.strava_data = None
        self.osm_data = None


    # 2. Methode zum Abrufen der Daten von Strava und OSM
    #    - Geocode die Stadt und erstelle ein Bounding Box  
    def fetch_data(self, geocode_city, create_bounding_box):
        """Fetch Strava segments and OSM data."""
        try:
            # Geocode city and create bounding box
            lat, lon = geocode_city(self.city)
            self.bounds = create_bounding_box(lat, lon, self.radius)

            # Fetch Strava segments
            self.strava_data = self._fetch_strava_segments()

            # Fetch OSM data
            self.osm_data = fetch_osm_data(self.bounds)

        except Exception as e:
            st.error(f"Error: {e}")



    # 3. Methode zum Abrufen der Strava-Daten
    #    - Hier wird die Methode fetch_strava_segments aufgerufen und die Daten verarbeitet 
    def _fetch_strava_segments(self):
        """Fetch and process Strava segments."""
        segments = fetch_strava_segments(self.bounds, self.activity_type)
        strava_list = []
        coords = []
        polyline_paths = []

        #Was Segmenten Dataframe angezeigt werden soll
        #Hier wird die Liste der Segmente erstellt, die wir in der Tabelle anzeigen wollen
        if "segments" in segments and segments["segments"]:
            for seg in segments["segments"]:
                start = seg.get("start_latlng")
                if start and len(start) == 2:
                    coords.append(start)
                strava_list.append({
                    "Name": seg.get("name"),
                    "Distance (m)": round(seg.get("distance", 0), 1),
                    "Avg Grade (%)": seg.get("avg_grade"),
                    "Elevation Difference": seg.get("elev_difference"),
                    "Start Lat/Lon": start,
                    "End Lat/Lon": seg.get("end_latlng")
                })

                polyline_str = seg.get("points")
                if polyline_str:
                    decoded = polyline.decode(polyline_str)
                    path = [[lon, lat] for lat, lon in decoded]
                    polyline_paths.append({
                        "name": seg.get("name", "Unnamed Segment"),
                        "path": path
                    })


            # Cache Strava data, konvertiert die Sessionstate aus Cache_manager.py zu einem DataFrame
            st.session_state.df_strava_cache = pd.DataFrame(strava_list)


            # == Zentrum der Karte berechnen==
            # mit den Koordinaten, die eingegeben wurden oder gefetcht wurden
            lats = [c[0] for c in coords]
            lons = [c[1] for c in coords]
            center_lat = sum(lats) / len(lats)
            center_lon = sum(lons) / len(lons)



            # == Erstellung von Layer für die Karte mit den Strava-Segmenten und Anfangspunkte ==
            #   - hier werden die Farben, Radien und andere Eigenschaften festgelegt

                # = Anfangspunkte als ScatterplotLayer =
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
                # = Strava-Segmente als PathLayer =
                # Hier wird die Polyline der Segmente in einen PathLayer umgewandelt
            strava_paths = pdk.Layer(
                "PathLayer",
                data=polyline_paths,
                get_path="path",
                get_width=20,
                get_color=[255, 0, 0],
                opacity=0.6,
                pickable=True
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
        else:
            st.warning("No Strava segments found.")

        return segments


# == OSM- und Daten abrufen und cachen ==
    def get_strava_data(self):
        """Return cached Strava data."""
        return st.session_state.df_strava_cache

    def get_osm_data(self):
        """Return cached OSM data."""
        return self.osm_data