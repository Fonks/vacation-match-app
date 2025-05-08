import requests

OVERPASS_URL = "http://overpass-api.de/api/interpreter"

def fetch_osm_pois(south, west, north, east, tags=["tourism", "leisure", "amenity"]):
    """
    Holt POIs aus OSM anhand einer Bounding Box (south, west, north, east).
    """
    tag_filters = "".join(f'node[{tag}](%f,%f,%f,%f);' % (south, west, north, east) for tag in tags)
    query = f"""
    [out:json];
    (
        {tag_filters}
    );
    out center;
    """

    response = requests.get(OVERPASS_URL, params={"data": query})
    response.raise_for_status()
    elements = response.json().get("elements", [])

    # Absicherung: Überprüfen, ob der 'type'-Tag existiert, bevor er abgefragt wird
    return [
        e for e in elements if 'tags' in e and 'type' in e['tags']
    ]


