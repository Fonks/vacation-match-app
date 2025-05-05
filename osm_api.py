# This module will handle OSM queries, e.g. via Overpass API
# Developer note: Requires implementation using Overpass API or another OSM source

import requests

def fetch_osm_data(bounding_box):
    """
    Fetch all OSM elements with an 'amenity' tag within the given bounding box.
    
    bounding_box: tuple in the format (south, west, north, east)
    Returns: JSON response from Overpass API
    """
    west, south, east, north = bounding_box[1], bounding_box[0], bounding_box[3], bounding_box[2]
    url = "https://overpass-api.de/api/interpreter"

    # Overpass QL query
    query = f"""
    [out:json][timeout:25];
    (
      node["amenity"]({south},{west},{north},{east});
      way["amenity"]({south},{west},{north},{east});
      relation["amenity"]({south},{west},{north},{east});
    );
    out center;
    """

    headers = {
        "User-Agent": "vacation-match-app/1.0"
    }

    response = requests.post(url, data={"data": query}, headers=headers)
    response.raise_for_status()
    return response.json()
