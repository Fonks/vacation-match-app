from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def geocode_city(city_name):
    """
    Geokodiert den Stadtnamen zu einem (Latitude, Longitude)-Tupel.
    """
    geolocator = Nominatim(user_agent="vacation_match_app")
    try:
        location = geolocator.geocode(city_name)
        if location:
            return location.latitude, location.longitude
        else:
            raise ValueError(f"Stadt '{city_name}' konnte nicht geokodiert werden.")
    except GeocoderTimedOut:
        raise TimeoutError("Geocoder-Anfrage hat zu lange gedauert.")

def get_bounding_box(city_name, padding=0.05):
    """
    Erstellt eine Bounding Box um eine Stadt mit etwas Puffer.
    Gibt (south, west, north, east) zurück.
    """
    lat, lon = geocode_city(city_name)
    south = lat - padding
    north = lat + padding
    west = lon - padding
    east = lon + padding
    return south, west, north, east
