from .strava_api import fetch_strava_segments
from .osm_api import fetch_osm_pois
from .geo_utils import get_bounding_box

def fetch_data_for_city(city_name):
    """
    Holt Strava-Segmente und OSM-POIs für eine gegebene Stadt.
    """
    south, west, north, east = get_bounding_box(city_name)

    strava_segments = fetch_strava_segments(south, west, north, east)
    osm_pois = fetch_osm_pois(south, west, north, east)

    return strava_segments, osm_pois
