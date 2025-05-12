import requests

def geocode_city(city_or_coords):
    """
    Accepts either a city name or 'lat,lon' format string.
    Returns latitude and longitude as floats.
    """
    if "," in city_or_coords:
        try:
            lat_str, lon_str = city_or_coords.split(",")
            lat = float(lat_str.strip())
            lon = float(lon_str.strip())
            return lat, lon
        except ValueError:
            raise ValueError("Invalid coordinates. Please enter as 'lat, lon'")
    else:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": city_or_coords,
            "format": "json",
            "limit": 1
        }
        headers = {
            "User-Agent": "vacation-match-app/1.0"
        }
        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        if data:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            return lat, lon
        else:
            raise ValueError(f"City not found: {city_or_coords}")

def create_bounding_box(lat, lon, radius_km):
    """
    Returns a bounding box around (lat, lon) with radius_km.
    Format: [south, west, north, east]
    """
    delta = radius_km / 111  # Roughly 1° latitude ~ 111 km
    return [lat - delta, lon - delta, lat + delta, lon + delta]
