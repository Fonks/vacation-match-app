import requests

def geocode_city(city_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "sport-match-app/1.0"
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    if data:
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        return lat, lon
    else:
        raise ValueError(f"City not found: {city_name}")

def create_bounding_box(lat, lon, radius_km):
    # Approximate conversion: 1 degree latitude ~ 111 km
    delta_deg = radius_km / 111
    south = lat - delta_deg
    north = lat + delta_deg
    west = lon - delta_deg
    east = lon + delta_deg
    return south, west, north, east
