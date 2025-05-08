# vacation_match_app/map/visualizer.py

# Stellt Strava-Segmente und POIs mit Pydeck dar.

import pydeck as pdk
import pandas as pd
from .icons import get_poi_color

def create_segment_layer(segment_df: pd.DataFrame) -> pdk.Layer:
    """
    Erstellt eine ScatterplotLayer für Strava-Segmente.
    """
    return pdk.Layer(
        "ScatterplotLayer",
        data=segment_df,
        get_position='[lon, lat]',
        get_radius=70,
        get_fill_color='[0, 180, 50, 160]',  # grün
        pickable=True
    )

def create_poi_layer(poi_df: pd.DataFrame) -> pdk.Layer:
    """
    Erstellt eine ScatterplotLayer für POIs.
    """
    if "color" not in poi_df.columns:
        poi_df = poi_df.copy()
        poi_df["color"] = poi_df["type"].apply(get_poi_color)

    return pdk.Layer(
        "ScatterplotLayer",
        data=poi_df,
        get_position='[lon, lat]',
        get_fill_color='color',
        get_radius=80,
        pickable=True
    )

def render_map(lat: float, lon: float, segments: pd.DataFrame, pois: pd.DataFrame):
    """
    Zeigt die interaktive Karte mit Segmenten und POIs.
    """
    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=12
    )

    layers = [create_segment_layer(segments), create_poi_layer(pois)]

    return pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=view_state,
        layers=layers,
        tooltip={"text": "{name}"}
    )
