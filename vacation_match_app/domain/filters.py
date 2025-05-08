from typing import List
import pandas as pd
from vacation_match_app.domain.segment import Segment
from vacation_match_app.domain.poi import POI

def filter_segments_by_location(segments: List[Segment], bounding_box: dict) -> List[Segment]:
    return [
        s for s in segments
        if bounding_box["south"] <= s.lat <= bounding_box["north"]
        and bounding_box["west"] <= s.lon <= bounding_box["east"]
    ]

def filter_pois_by_location(pois: List[POI], bounding_box: dict) -> List[POI]:
    """
    Gibt nur POIs zurück, die innerhalb der bounding_box liegen.
    """
    return [
        p for p in pois
        if 'lat' in p and 'lon' in p and bounding_box["south"] <= p["lat"] <= bounding_box["north"]
        and bounding_box["west"] <= p["lon"] <= bounding_box["east"]
    ]



def filter_pois_by_type(pois: List[POI], selected_types: List[str]) -> List[POI]:
    """
    Gibt nur POIs zurück, deren Typen in selected_types enthalten sind.
    """
    return [
        p for p in pois if 'type' in p['tags'] and p['tags']['type'] in selected_types
    ]




def filter_data_for_map_strava(data_dict: dict, city: str) -> pd.DataFrame:
    """
    Wandelt Strava-Segment-Daten in DataFrame um.
    """
    segments = data_dict.get(city, [])
    return pd.DataFrame(segments)

def filter_data_for_map_osm(data_dict: dict, selected_types: List[str], city: str) -> pd.DataFrame:
    """
    Wandelt OSM-POIs in DataFrame um, nach Typ gefiltert.
    """
    pois = data_dict.get(city, [])
    filtered = filter_pois_by_type(pois, selected_types)
    return pd.DataFrame(filtered)

def filter_data_for_table(data_dict: dict, selected_types: List[str], cities: List[str]) -> pd.DataFrame:
    """
    Gibt eine tabellarische Übersicht über POI-Typen in allen Städten.
    """
    rows = []
    for city in cities:
        pois = data_dict.get(city, [])
        filtered = filter_pois_by_type(pois, selected_types)
        rows.append({
            "Stadt": city,
            "Anzahl POIs": len(filtered)
        })
    return pd.DataFrame(rows)
